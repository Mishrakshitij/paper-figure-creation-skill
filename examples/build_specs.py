#!/usr/bin/env python3
"""Create original source-linked MAE and Transformer demonstration specs.

All reported numbers are transcribed from the linked papers; no training run is
performed. Run from any directory. Geometry is authored here and remains editable.
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write(name, spec):
    path = HERE / name / "figure.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec, indent=2) + "\n")


def result(key, method, metric, value, source, context, location):
    return dict(id=key, method_id=method, metric_id=metric, value=value,
                source_id=source, comparison=context, source_location=location)


def base(kind, title, subtitle, source, height=3.7):
    return {"version": 1, "kind": kind, "status": "final",
            "figure": {"width_in": 7, "height_in": height,
                       "title": title, "subtitle": subtitle},
            "provenance": {"data_status": "reported", "sources": [source]},
            "evidence": {"metrics": [], "results": [], "claims": []}}


mae_source = {"id": "mae", "kind": "paper",
              "locator": "https://arxiv.org/pdf/2111.06377v3",
              "location": "Table 2, PDF page 5, ViT-L rows; Section 3 and Figure 1"}
mae = base("teaser", "MAE: encode fewer patches, retain recognition quality",
           "ViT-L/16 · ImageNet-1K · 800 epochs · 128 TPU-v3 cores", mae_source, 3.8)
ctx = {"dataset": "ImageNet-1K", "split": "validation",
       "budget": "800 pretraining epochs; 128 TPU-v3 cores; TensorFlow",
       "protocol": "Table 2; 75% masking; decoder width 512; fine-tuned top-1"}
mae["evidence"]["metrics"] = [
    {"id": "acc", "label": "Fine-tuned top-1 accuracy", "direction": "higher", "unit": "percent"},
    {"id": "time", "label": "Pretraining wall-clock time", "direction": "lower", "unit": "hours"}]
rows = [("masked8", "Encoder with mask tokens", 42.4, 84.2, "baseline"),
        ("visible8", "Visible only · 8-block decoder", 15.4, 84.9, "proposed"),
        ("visible1", "Visible only · 1-block decoder", 11.6, 84.8, "baseline")]
for method, label, hours, acc, role in rows:
    for metric, value in [("acc", acc), ("time", hours)]:
        mae["evidence"]["results"].append(result(method + "_" + metric, method, metric,
            value, "mae", ctx, "Table 2, ViT-L row " + method))
mae["evidence"]["claims"] = [
    {"id": "time_gain", "type": "reduction", "baseline_result_id": "masked8_time",
     "proposed_result_id": "visible8_time", "display_value": 63.7, "decimals": 1},
    {"id": "acc_gain", "type": "percentage_point_difference", "baseline_result_id": "masked8_acc",
     "proposed_result_id": "visible8_acc", "display_value": 0.7, "decimals": 1}]
mae["concept"] = {"kind": "token_grid", "title": "Learn from visible patches",
    "input_label": "Illustrative image patch grid", "rows": 4, "cols": 4,
    "selected": [1, 6, 9, 15], "labels": [""] * 16,
    "operation_label": "Keep 25%\nfor the encoder",
    "output_label": "Reconstruct what\nis missing",
    "note": "Mask tokens enter the decoder later."}
mae["charts"] = [{"type": "scatter", "title": "Quality and training time",
    "metric_id": "acc", "x_metric_id": "time", "xlabel": "Pretraining time (hours) ↓",
    "ylabel": "Fine-tuned top-1 (%) ↑", "xlim": [5, 49], "ylim": [84.05, 85.08],
    "legend": False,
    "series": [{"label": label, "role": role, "values": [acc], "result_ids": [m + "_acc"],
                "x_values": [hours], "x_result_ids": [m + "_time"], "point_labels": [label],
                "point_label_offsets": [[-7, 8] if m == "masked8" else [7, -24] if m == "visible1" else [7, 8]]}
               for m, label, hours, acc, role in rows]}]
mae["figure"]["note"] = "Table 2 ablation: 63.7% less time and +0.7 percentage points for the 8-block variant."
write("mae-teaser", mae)

def node(key, label, x, y, w, h, **extra):
    return dict(id=key, label=label, x=x, y=y, w=w, h=h, **extra)

def edge(source, target, **extra):
    return dict(source=source, target=target, **extra)

mae_method = base("method", "MAE: visible-only encoding during pretraining",
    "The decoder reconstructs masked patches; recognition reuses the encoder.", mae_source, 4.5)
mae_method["groups"] = [
    dict(label="PRETRAINING", x=0, y=.43, w=1, h=.57),
    dict(label="RECOGNITION AFTER FINE-TUNING", x=0, y=0, w=1, h=.36)]
mae_method["nodes"] = [
    node("patches", "Image patches", .02, .72, .16, .19,
         representation={"rows": 2, "cols": 4, "selected": [1, 6]}),
    node("visible", "Keep 25%", .23, .74, .14, .15, role="proposed"),
    node("encoder", "Encoder", .42, .74, .16, .15, role="proposed", detail="visible only"),
    node("decoder", "Decoder", .64, .74, .16, .15, detail="lightweight"),
    node("pixels", "Pixels", .86, .74, .12, .15),
    node("mask", "Mask tokens", .64, .49, .16, .12),
    node("loss", "MSE loss", .85, .49, .14, .12),
    node("full", "All patches", .05, .065, .17, .16,
         representation={"rows": 2, "cols": 4, "selected": list(range(8))}),
    node("reuse", "Encoder", .34, .065, .21, .16, role="proposed", detail="pretrained weights"),
    node("head", "Task head", .68, .065, .20, .16)]
mae_method["edges"] = [
    edge("patches", "visible"), edge("visible", "encoder", role="proposed"),
    edge("encoder", "decoder"), edge("decoder", "pixels"),
    edge("mask", "decoder", source_port="top", target_port="bottom", label="restore positions", label_position=[.72, .675]),
    edge("pixels", "loss", source_port="bottom", target_port="top", kind="training"),
    edge("patches", "loss", source_port="bottom", target_port="left", via=[[.10, .46], [.825, .46], [.825, .55]],
         label="masked-patch targets", label_position=[.35, .46], kind="training"),
    edge("full", "reuse"), edge("reuse", "head")]
mae_method["annotations"] = [dict(x=.98, y=.29, ha="right", text="Decoder removed for recognition.")]
mae_method["figure"]["note"] = "Dashed: loss supervision. Masked-patch loss only. Patch projection and positional embeddings omitted."
write("mae-method", mae_method)

tf_source = {"id": "transformer", "kind": "paper", "locator": "https://arxiv.org/pdf/1706.03762",
             "location": "Table 2, PDF page 8, EN-DE column; Figure 1 and Section 3"}
tf = base("teaser", "Transformer: attention-based translation",
          "WMT 2014 English–German · newstest2014 · reported systems", tf_source, 4.0)
tf["evidence"]["metrics"] = [{"id": "bleu", "label": "BLEU", "direction": "higher", "unit": "BLEU"}]
tfrows = [("bytenet", "ByteNet", 23.75), ("gnmt", "GNMT + RL", 24.6),
          ("convs2s", "ConvS2S", 25.16), ("moe", "MoE", 26.03),
          ("gnmt_ensemble", "GNMT + RL (ensemble)", 26.30),
          ("conv_ensemble", "ConvS2S (ensemble)", 26.36),
          ("base", "Transformer base", 27.3), ("big", "Transformer big", 28.4)]
for key, label, score in tfrows:
    tf["evidence"]["results"].append(result(key, key, "bleu", score, "transformer",
        {"dataset": "WMT 2014 English-German", "split": "newstest2014",
         "budget": "Original Table 2 system-specific training budgets; not compute matched",
         "protocol": "Published comparison; ensemble status explicitly labeled"}, "Table 2, " + label + ", EN-DE"))
tf["concept"] = {"kind": "custom", "title": "Tokens share context", "input_label": "Illustrative source sentence",
    "nodes": [node("t1", "The", .03, .70, .25, .16), node("t2", "cat", .36, .70, .25, .16),
              node("t3", "sat", .69, .70, .25, .16),
              node("attn", "Self-attention", .14, .36, .7, .19, role="proposed"),
              node("out", "Context for each token", .03, .06, .91, .16, shape="text")],
    "edges": [edge(t, "attn", source_port="bottom", target_port="top") for t in ["t1", "t2", "t3"]] +
             [edge("attn", "out", source_port="bottom", target_port="top", role="proposed")],
    "note": "Encoder connectivity, not measured weights."}
tf["charts"] = [{"type": "dot", "title": "Reported translation quality", "metric_id": "bleu",
    "categories": [label for key, label, score in tfrows], "xlabel": "BLEU ↑", "xlim": [23, 29.5], "xticks": list(range(23, 30)),
    "legend": False, "value_labels": True, "value_format": ".2f",
    "series": [{"label": "Reported systems", "values": [score for key,label,score in tfrows],
                "result_ids": [key for key,label,score in tfrows],
                "point_roles": ["proposed" if key in ["base", "big"] else "baseline" for key,label,score in tfrows]}]}]
tf["figure"]["note"] = "Table 2: all EN–DE entries are shown. System budgets differ; no equal-compute claim."
write("transformer-teaser", tf)

tfm = base("method", "Transformer: attention connects source and target sequences",
           "Original post-norm blocks: LayerNorm(x + Sublayer(x)). Residual wiring omitted in this overview.", tf_source, 4.6)
tfm["groups"] = [dict(label="N ENCODER BLOCKS", x=.07, y=.40, w=.34, h=.58),
                 dict(label="N DECODER BLOCKS", x=.51, y=.39, w=.44, h=.59)]
tfm["nodes"] = [
    node("src", "Source tokens", .14, .025, .20, .12),
    node("semb", "Embed + position", .14, .20, .20, .14),
    node("self", "Self-attention", .14, .47, .20, .14, role="proposed"),
    node("eff", "Feed-forward", .14, .75, .20, .14),
    node("tgt", "Previous outputs\n(shifted right)", .54, .015, .20, .14),
    node("temb", "Embed + position", .54, .20, .20, .14),
    node("masked", "Masked\nself-attention", .54, .46, .20, .16, role="proposed"),
    node("cross", "Cross-attention", .54, .74, .20, .14, role="proposed"),
    node("dff", "Feed-\nforward", .77, .74, .16, .14),
    node("logits", "Linear +\nsoftmax", .78, .20, .17, .14),
    node("next", "Next token", .78, .025, .17, .12)]
tfm["edges"] = [edge("src","semb",source_port="top",target_port="bottom"),
    edge("semb","self",source_port="top",target_port="bottom"), edge("self","eff",source_port="top",target_port="bottom"),
    edge("eff","cross",label="keys, values", label_position=[.435,.855]),
    edge("tgt","temb",source_port="top",target_port="bottom"),
    edge("temb","masked",source_port="top",target_port="bottom"),
    edge("masked","cross",source_port="top",target_port="bottom",label="queries",label_position=[.64,.68]),
    edge("cross","dff"), edge("dff","logits",source_port="bottom",target_port="top"),
    edge("logits","next",source_port="bottom",target_port="top")]
tfm["figure"]["note"] = "Schematic. Embeddings and prediction head sit outside repeated blocks. Token feedback omitted."
write("transformer-method", tfm)

if __name__ == "__main__":
    print("Wrote 4 source-linked figure specifications.")
