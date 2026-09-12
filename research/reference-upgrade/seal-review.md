# SEAL: visual reference review

Reviewed 2026-09-12. Paper: [Self-Adapting Language Models](https://arxiv.org/html/2506.10943v2). Actual pixels inspected from the [authors' project page](https://jyopari.github.io/posts/seal), through its public GitHub source. These are project-page versions of the paper's figures, not rasterizations of the supplied PDF.

## Inspected assets

Repository `jyopari/jyopari.github.io`, revision `2b7c60ad3c2c35291149176cb91e0831c07e1042`, directory `posts/Self-Adapting Language Models 20de3cb2605580d291a8d7d8ca7f1604/`:

| File | Content |
| --- | --- |
| `Screenshot_2025-06-09_at_1.28.39_PM.png` | Candidate-edit overview corresponding to Figure 1 |
| `Screenshot_2025-06-09_at_2.04.38_PM.png` | Algorithm 1; inspected as a semantic cross-check |
| `Screenshot_2025-06-09_at_2.15.54_PM.png` | Knowledge-incorporation setup corresponding to Figure 2 |
| `Screenshot_2025-06-09_at_2.16.16_PM.png` | Few-shot setup corresponding to Figure 3 |

## Observations

Three aligned candidate branches expose generation, adaptation and testing. Repeated colored parameter chips distinguish model states; blue context/test objects, amber edits and lavender optimization marks establish correspondence across panels. The knowledge example shows passage and edit contents. The few-shot example uses actual grid structure and configuration fields, making the action space visible. Curved fan-out/fan-in routes and a restrained background contain considerable detail without boxing every phrase. These observations concern the retrieved assets; later paper versions may differ.

## Implications for this skill

The v1 examples often name a representation without showing its informative contents. For a new diagram, select the objects whose internal structure explains the contribution, preserve their identity across transformations, and give repeated alternatives aligned geometry. Separate parameter updates from forward data, and show the thing an optimizing policy actually chooses. One task-specific worked example can explain more than an additional abstract module. Original redraws should transfer those principles, not copy the authors' arrangement or palette.

The new SEAL examples use the paper's v2 tables as the numerical authority. The project page is a visual reference; its result prose must not silently override a newer table.
