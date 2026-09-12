#!/usr/bin/env python3
"""Original MAE method illustration; deterministic vector geometry, no model run.

Run: python examples/mae-v2/build_figure.py [--output-dir PATH]
Requires matplotlib, numpy, Pillow and PyMuPDF for the optional print proofs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

INK = "#20343D"
MUTED = "#536A75"
TEAL = "#087F8C"
TEAL_PALE = "#E4F2F0"
BLUE = "#2969A1"
BLUE_PALE = "#EAF0F8"
MASK = "#B57045"
MASK_PALE = "#F3E6D7"
GRID = "#A8BAC2"
VISIBLE = (2, 6, 11, 15)  # one-based patch identities, row-major image order
PACKED = (11, 2, 15, 6)  # an illustrative shuffled visible-token order
W, H = 7, 3.95


def label(ax, x, y, text, size=8.5, color=INK, weight="normal", ha="left", va="center", **kw):
    return ax.text(x, y, text, fontsize=size, color=color, weight=weight,
                   ha=ha, va=va, family="DejaVu Sans", **kw)


def rect(ax, x, y, w, h, fc="white", ec=GRID, lw=.7, radius=0, zorder=2, **kw):
    if radius:
        p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                           facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder, **kw)
    else:
        p = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder, **kw)
    ax.add_patch(p)
    return p


def arrow(ax, start, end, color=MUTED, lw=1.1, style="-|>", zorder=4, **kw):
    p = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=8,
                        linewidth=lw, color=color, zorder=zorder, **kw)
    ax.add_patch(p)
    return p


def scene(ax, x, y, s, clip=None, prediction=False, z=2):
    """Procedural vector landscape, intentionally varied for illustrative prediction."""
    p = rect(ax, x, y, s, s, fc="#DDEEF1", ec="none", zorder=z)
    patches = [p]
    patches.append(Circle((x+s*.79, y+s*.79), s*(.105 if prediction else .12),
                          facecolor="#E8BC51", edgecolor="none", zorder=z+.1))
    patches.append(Polygon([(x,y+s*.33),(x+s*.28,y+s*.68),(x+s*.6,y+s*.31)],
                           facecolor="#9AB1C0", edgecolor="none", zorder=z+.1))
    patches.append(Polygon([(x+s*.22,y+s*.26),(x+s*.62,y+s*.58),(x+s,y+s*.23)],
                           facecolor="#BBCACC", edgecolor="none", zorder=z+.2))
    patches.append(Rectangle((x,y),s,s*.27,facecolor="#B6CFA8",edgecolor="none",zorder=z+.3))
    patches.append(Rectangle((x+s*.38,y+s*.15),s*.08,s*.33,
                              facecolor="#896447",edgecolor="none",zorder=z+.4))
    shift = .035 if prediction else 0
    patches.append(Polygon([(x+s*(.15+shift),y+s*.35),(x+s*(.42+shift),y+s*.79),
                            (x+s*(.69+shift),y+s*.35)],
                           facecolor="#367F70" if prediction else "#2C7764",
                           edgecolor="none",zorder=z+.5))
    for p in patches[1:]:
        ax.add_patch(p)
    if clip is not None:
        for p in patches:
            p.set_clip_path(clip)
    return patches


def image_grid(ax, x, y, s, mode="input", show_ids=False):
    scene(ax, x, y, s, prediction=mode=="prediction")
    cell = s/4
    for i in range(16):
        k = i+1; col=i%4; row=i//4
        px=x+col*cell; py=y+(3-row)*cell
        hidden = mode=="visible" and k not in VISIBLE
        if hidden:
            rect(ax,px,py,cell,cell,fc=MASK_PALE,ec="white",lw=.5,zorder=5)
            ax.plot([px+.055,px+cell-.055],[py+.055,py+cell-.055],
                    color="#CBB99F",lw=.6,zorder=6)
        rect(ax,px,py,cell,cell,fc="none",ec="white",lw=.7,zorder=7)
        if mode in ("input","visible") and k in VISIBLE:
            rect(ax,px+.009,py+.009,cell-.018,cell-.018,fc="none",ec=TEAL,lw=1.0,zorder=8)
        if mode=="targets" and k not in VISIBLE:
            rect(ax,px+.01,py+.01,cell-.02,cell-.02,fc="none",ec=MASK,lw=1.0,zorder=8)
        if mode=="targets" and k in VISIBLE:
            rect(ax,px,py,cell,cell,fc="white",ec="#D9E2E5",lw=.5,zorder=8)
        if show_ids and k in VISIBLE:
            rect(ax,px+.013,py+.013,.115,.09,fc="white",ec="none",zorder=9)
            label(ax,px+.07,py+.058,str(k),size=6.2,color=TEAL,weight="bold",ha="center",zorder=10)
    rect(ax,x,y,s,s,fc="none",ec=GRID,lw=.75,zorder=9)


def crop_patch(ax, x, y, s, k):
    row,col=divmod(k-1,4)
    clip=rect(ax,x,y,s,s,fc="white",ec="none",zorder=3)
    scene(ax,x-col*s,y-(3-row)*s,4*s,clip=clip,z=3)
    rect(ax,x,y,s,s,fc="none",ec=TEAL,lw=.85,zorder=9)
    label(ax,x+s+.055,y+s/2,str(k),size=7,color=TEAL,weight="bold",zorder=10)


def latent(ax, x, y, w, h, k=None, mask=False, stripes=True, id_size=7):
    c=MASK if mask else BLUE
    rect(ax,x,y,w,h,fc=MASK_PALE if mask else BLUE_PALE,ec=c,lw=.7,radius=.015,zorder=5)
    if mask:
        # Redundant marking survives grayscale; the learned M token is shared.
        ax.plot([x+w*.15,x+w*.85],[y+h*.15,y+h*.85],color=MASK,lw=.55,zorder=6)
    if stripes and not mask:
        for j in range(3):
            ax.plot([x+.035,x+w-.035],[y+h*(.25+.24*j)]*2,color=c,alpha=.4,lw=.6,zorder=6)
    if k is not None:
        label(ax,x+w/2,y+h/2,str(k),size=id_size,color=c,weight="bold",ha="center",zorder=8,
              bbox=dict(facecolor=MASK_PALE if mask else BLUE_PALE,edgecolor="none",pad=.1))


def transformer_stack(ax, x, y, w, h, depth, color, pale, name):
    # Multiplicity is schematic, not the actual number of Transformer layers.
    for i in reversed(range(depth)):
        rect(ax,x+i*.055,y+i*.04,w,h,fc=pale,ec=color,lw=.75,radius=.025,zorder=2+depth-i)
    for j in range(3):
        rect(ax,x+.085,y+.18+j*(h-.36)/3,w-.17,(h-.36)/3-.035,
             fc="white",ec=color,lw=.5,radius=.012,zorder=10)
    label(ax,x+w/2,y+h+.20,name,size=9.2,color=color,weight="bold",ha="center",zorder=20)


def draw(out):
    matplotlib.rcParams.update({"svg.fonttype":"none", "pdf.fonttype":42,
                                "ps.fonttype":42, "font.size":8.5})
    fig=plt.figure(figsize=(W,H),facecolor="white")
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis("off")

    label(ax,.18,3.74,"MAE",size=11.5,weight="bold")
    label(ax,.68,3.74,"Learn from visible content; reconstruct what is missing",size=10.0)

    for x,w,title in [(.18,2.29,"a  Randomly keep 25%"),(2.63,1.12,"b  Encode"),(4.02,2.8,"c  Reconstruct")]:
        label(ax,x,3.39,title,size=9,weight="bold")
        ax.plot([x,x+w],[3.24,3.24],color="#D5E0E3",lw=.8)

    # One recognisable example remains visible through the whole upper route.
    image_grid(ax,.18,2.10,.99,"input",True)
    image_grid(ax,1.46,2.10,.99,"visible",True)
    arrow(ax,(1.19,2.60),(1.44,2.60),color=TEAL)
    label(ax,1.31,2.95,"mask",size=7.5,color=MASK,ha="center")
    label(ax,.675,1.96,"16 image patches",ha="center")
    label(ax,1.955,1.96,"4 visible",ha="center",color=TEAL,size=8.2)
    label(ax,1.955,1.80,"12 hidden (75%)",ha="center",color=MASK,size=8.2)
    # Packed visible image content is explicit rather than a generic input label.
    for n,k in enumerate(PACKED):
        crop_patch(ax,2.65,2.10+(3-n)*.245,.205,k)
    arrow(ax,(2.47,2.60),(2.61,2.60),color=TEAL)
    arrow(ax,(2.98,2.60),(3.12,2.60),color=TEAL)
    label(ax,2.78,1.93,"4 tokens",size=8,ha="center")
    label(ax,2.78,1.80,"+ pos.",size=8,ha="center")
    transformer_stack(ax,3.15,2.06,.51,.91,3,TEAL,TEAL_PALE,"Encoder")
    label(ax,3.41,1.93,"visible only",size=8,color=TEAL,ha="center")

    # Projected visible latents enter reassembly, then all positions enter decoder.
    arrow(ax,(3.86,2.59),(4.01,2.59),color=BLUE)
    for r in range(4):
        for c in range(4):
            k=r*4+c+1
            latent(ax,4.04+c*.16,2.30+(3-r)*.16,.145,.145,mask=k not in VISIBLE,stripes=False)
    label(ax,4.345,3.13,"Restore",size=8.4,ha="center",weight="bold")
    label(ax,4.345,2.99,"positions",size=8.4,ha="center",weight="bold")
    label(ax,4.345,2.17,"4 latents",size=8.0,ha="center",color=BLUE)
    label(ax,4.345,2.02,"+ 12 masks",size=8.0,ha="center",color=MASK)
    arrow(ax,(4.73,2.59),(5.00,2.59),color=BLUE)
    transformer_stack(ax,5.04,2.28,.43,.53,2,MASK,MASK_PALE,"Decoder")
    label(ax,5.28,2.14,"lightweight",size=8,color=MASK,ha="center")
    arrow(ax,(5.61,2.59),(5.81,2.59),color=MASK)
    image_grid(ax,5.85,2.10,.99,"prediction")
    label(ax,6.345,1.96,"Illustrated",size=8.1,ha="center")
    label(ax,6.345,1.81,"reconstruction",size=8.1,ha="center")

    # The detail inset belongs to the restore operation, not to a second pipeline.
    rect(ax,.18,.52,4.50,1.09,fc="#F6F8FA",ec="#C4D2D9",radius=.045,lw=.7,zorder=1)
    label(ax,.32,1.44,"Inside position restoration",size=9.0,weight="bold")
    label(ax,4.53,1.44,"patch IDs",size=7.2,color=MUTED,ha="right")
    for j,k in enumerate(PACKED):
        latent(ax,.34+j*.255,1.045,.22,.22,k,mask=False,stripes=False,id_size=7.8)
    label(ax,1.44,1.16,"+",size=12,ha="center")
    latent(ax,1.60,1.045,.22,.22,"M",mask=True,stripes=False,id_size=7.8)
    label(ax,1.89,1.155,"× 12",size=8,color=MASK)
    arrow(ax,(2.45,1.155),(2.82,1.155),color=MUTED)
    label(ax,2.95,1.155,"unshuffle",size=8.2)
    for i in range(16):
        latent(ax,.34+i*.263,.70,.235,.22,i+1,mask=i+1 not in VISIBLE,
               stripes=False,id_size=7.4)
    label(ax,2.50,.59,"then add decoder position embeddings",size=7.8,ha="center",color=MUTED)
    ax.plot([4.67,4.74,4.52],[2.30,1.75,1.61],color=GRID,lw=.8,linestyle=(0,(2,2)),zorder=1)

    # Supervision shows the original content at the masked coordinates.
    image_grid(ax,4.98,.67,.70,"targets")
    label(ax,5.33,1.49,"Original targets",size=8.3,weight="bold",ha="center")
    arrow(ax,(5.72,1.02),(5.96,1.02),color=MASK)
    rect(ax,5.99,.79,.85,.45,fc=MASK_PALE,ec=MASK,radius=.04)
    label(ax,6.415,1.075,"MSE",size=9.3,weight="bold",ha="center",color=MASK)
    label(ax,6.415,.91,"masked only",size=7.8,ha="center",color=MASK)
    arrow(ax,(6.34,1.69),(6.34,1.29),color=MASK,lw=.9,linestyle=(0,(3,2)))
    label(ax,5.33,.55,"12 / 16 patches",size=7.8,ha="center",color=MASK)
    # The original-image-to-target relation is named to avoid a long crossing edge.
    label(ax,4.98,.36,"Targets come from the original image.",size=7.5,color=MUTED)

    label(ax,.18,.27,"Scene and reconstruction are illustrative; 16-patch example; no model run.",
          size=7.6,color=MUTED)
    label(ax,.18,.115,"Pretraining only. CLS token, projection layers and internal attention details omitted.",
          size=7.6,color=MUTED)

    fig.canvas.draw()
    # Text must fit the physical canvas; geometric inspection remains manual.
    renderer=fig.canvas.get_renderer()
    bounds=fig.bbox
    clipped=[]
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text(): continue
        b=t.get_window_extent(renderer)
        if b.x0<bounds.x0-.5 or b.y0<bounds.y0-.5 or b.x1>bounds.x1+.5 or b.y1>bounds.y1+.5:
            clipped.append(t.get_text())
    if clipped:
        raise RuntimeError(f"Text outside canvas: {clipped}")
    for ext in ("svg","pdf","png"):
        fig.savefig(out/f"figure.{ext}",dpi=300,facecolor="white")
    plt.close(fig)
    (out/"geometry-check.json").write_text(json.dumps({
        "figure_width_in":W,"figure_height_in":H,"visible_patch_ids":VISIBLE,
        "packed_visible_ids":PACKED,"mask_count":12,"text_outside_canvas":clipped,
        "figure_status":"reviewed example draft; target manuscript unavailable",
        "numerical_experiments":"none; patch counts are an illustrative 16-patch construction"
    },indent=2)+"\n")


def proofs(out):
    from PIL import Image, ImageOps
    im=Image.open(out/"figure.png").convert("RGB")
    ImageOps.grayscale(im).save(out/"figure-grayscale.png")
    try:
        import fitz
    except ImportError:
        return
    # Letter page at actual 7-inch width, rather than fit-to-page enlargement.
    proof=fitz.open(); page=proof.new_page(width=612,height=792)
    src=fitz.open(out/"figure.pdf")
    page.show_pdf_page(fitz.Rect(54,54,558,54+H*72),src,0)
    page.insert_text((54,54+H*72+22),"MAE v2 | 7-inch-wide draft | illustrative vector scene",fontsize=9)
    proof.save(out/"print-proof.pdf")
    page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(out/"print-proof.png")
    proof.close(); src.close()


def storyboards(out):
    """Late layout comparison, authored after the first detailed v2 draft."""
    fig, axes=plt.subplots(3,1,figsize=(7,5.6),facecolor="white")
    descriptions=[
        ("A  Example pipeline + local restoration inset (retained)",
         [(0,.46,.15,.35,"image"),(.20,.46,.15,.35,"visible"),(.41,.44,.11,.39,"encode"),
          (.57,.46,.12,.35,"restore"),(.74,.49,.08,.27,"decode"),(.87,.46,.12,.35,"reconstruct"),
          (.0,.02,.67,.26,"position restoration detail"),(.77,.02,.22,.26,"masked loss")]),
        ("B  U-shaped path around a large worked example",
         [(0,.61,.2,.23,"patch image"),(.30,.61,.22,.23,"visible tokens"),(.62,.61,.2,.23,"encoder"),
          (.80,.24,.18,.22,"decoder"),(.35,.24,.32,.22,"restoration detail"),(.0,.24,.20,.22,"prediction"),
          (.08,.02,.7,.14,"original targets → masked loss")]),
        ("C  Paired full-token / visible-token routes",
         [(0,.53,.14,.27,"image"),(.2,.62,.18,.21,"all tokens"),(.43,.62,.19,.21,"full encoder"),
          (.20,.25,.18,.21,"visible only"),(.43,.25,.19,.21,"MAE encoder"),
          (.67,.25,.15,.21,"restore"),(.86,.25,.13,.21,"decode"),(.2,.02,.79,.13,"local token correspondence + reconstruction")])
    ]
    for ax,(title,objects) in zip(axes,descriptions):
        ax.set_xlim(-.015,1.02);ax.set_ylim(-.03,1.03);ax.axis("off")
        ax.text(0,.98,title,fontsize=9,weight="bold",va="top",color=INK)
        for x,y,w,h,name in objects:
            ax.add_patch(Rectangle((x,y),w,h,facecolor=TEAL_PALE if "visible" in name or "MAE" in name else "#F0F3F5",
                                   edgecolor=GRID,lw=.8))
            ax.text(x+w/2,y+h/2,name,fontsize=7.2,ha="center",va="center",color=INK)
    fig.tight_layout(h_pad=1.3)
    fig.savefig(out/"storyboards.png",dpi=160,facecolor="white")
    fig.savefig(out/"storyboards.svg",facecolor="white")
    plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir",type=Path,default=Path(__file__).resolve().parent)
    args=p.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    draw(args.output_dir); proofs(args.output_dir); storyboards(args.output_dir)
    print(args.output_dir/"figure.png")


if __name__=="__main__":
    main()
