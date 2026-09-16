#!/usr/bin/env python3
"""Original Reasoning Gym setup diagram; no model or benchmark run.

python examples/reasoning-gym-setup/build_figure.py [--storyboards-only]
Requires matplotlib, Pillow and PyMuPDF. All geometry is editable vector artwork.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, PathPatch, Rectangle
from matplotlib.path import Path as MplPath
from PIL import Image
import fitz

W, H = 7, 4.15
INK = "#203640"
MUTED = "#566B76"
TEAL = "#137B78"
TEAL_PALE = "#E7F4EF"
BLUE = "#315D9E"
BLUE_PALE = "#EDF3FD"
GOLD = "#92601D"
GOLD_PALE = "#FBF0DD"
LINE = "#BDCDD4"

def label(ax, x, y, s, size=9, color=INK, weight="normal", ha="left", **kw):
    return ax.text(x, y, s, fontsize=size, color=color, weight=weight,
                   ha=ha, va="center", fontfamily="DejaVu Sans", **kw)

def box(ax, x, y, w, h, fill="white", edge=LINE, radius=.045, lw=.85, **kw):
    p = FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={radius}",
                      facecolor=fill,edgecolor=edge,linewidth=lw,**kw)
    ax.add_patch(p); return p

def arrow(ax, a, b, color=MUTED, **kw):
    p=FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,
                     linewidth=1.05,color=color,shrinkA=0,shrinkB=0,**kw)
    ax.add_patch(p); return p

def line(ax, xs, ys, color=MUTED, **kw):
    ax.plot(xs,ys,color=color,lw=kw.pop("lw",1.0),solid_capstyle="round",**kw)

def deer(ax, x, y, scale=.70):
    """Original four-legged deer pictogram; no external icon dependency."""
    s=scale
    ax.add_patch(Ellipse((x+.45*s,y+.45*s),.70*s,.33*s,fc=BLUE,ec="none"))
    ax.add_patch(Ellipse((x+.80*s,y+.72*s),.23*s,.21*s,angle=15,fc=BLUE,ec="none"))
    line(ax,[x+.69*s,x+.76*s],[y+.45*s,y+.70*s],BLUE,lw=7*s)
    for px,lean in [(.18,-.02),(.32,.02),(.57,-.02),(.68,.04)]:
        line(ax,[x+px*s,x+(px+lean)*s],[y+.39*s,y+.09*s],BLUE,lw=2.7*s)
    line(ax,[x+.12*s,x+.03*s],[y+.49*s,y+.64*s],BLUE,lw=2.5*s)
    line(ax,[x+.80*s,x+.73*s,x+.75*s],[y+.80*s,y+.99*s,y+1.08*s],BLUE,lw=1.6*s)
    line(ax,[x+.74*s,x+.65*s],[y+.97*s,y+1.04*s],BLUE,lw=1.6*s)
    line(ax,[x+.81*s,x+.85*s,x+.90*s],[y+.80*s,y+.97*s,y+1.03*s],BLUE,lw=1.6*s)
    ax.add_patch(Circle((x+.85*s,y+.76*s),.012*s,fc="white",ec="none"))

def slug(ax, x, y, scale=.75):
    """Original soft-bodied sea-slug pictogram without a shell or legs."""
    s=scale
    verts=[(x,y+.17*s),(x+.08*s,y+.44*s),(x+.49*s,y+.43*s),
           (x+.72*s,y+.28*s),(x+.98*s,y+.18*s),(x+.83*s,y+.12*s),
           (x+.16*s,y+.10*s),(x,y+.17*s)]
    codes=[MplPath.MOVETO]+[MplPath.CURVE3]*6+[MplPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MplPath(verts,codes),fc=TEAL,ec="none"))
    line(ax,[x+.14*s,x+.11*s],[y+.34*s,y+.56*s],TEAL,lw=2*s)
    line(ax,[x+.27*s,x+.30*s],[y+.37*s,y+.58*s],TEAL,lw=2*s)
    for px in [.43,.55,.67]:
        ax.add_patch(Ellipse((x+px*s,y+.30*s),.10*s,.19*s,angle=20,fc="#62A69A",ec="none"))

def canvas(w=W,h=H):
    fig=plt.figure(figsize=(w,h),facecolor="white")
    ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,w);ax.set_ylim(0,h);ax.axis("off")
    return fig,ax

def storyboards(out):
    """Compare structural options before detailed illustration."""
    fig,ax=canvas(9,2.5)
    titles=["A  Two information lanes", "B  Construction funnel", "C  One-entry magnifier"]
    for i,title in enumerate(titles):
        x=3*i
        label(ax,x+.12,2.29,title,10,weight="bold")
        box(ax,x+.10,.31,2.78,1.77,edge=TEAL if i==0 else LINE,lw=1.6 if i==0 else .8)
    # A: source splits into public question and private reference; only answer crosses.
    for x,y,w,h,txt,col in [(.23,1.0,.53,.67,"Setup",TEAL_PALE),(.99,1.28,.72,.50,"Question",BLUE_PALE),
                           (.99,.54,.72,.42,"Reference",GOLD_PALE),(2.02,1.28,.70,.50,"Model",BLUE_PALE),
                           (2.02,.54,.70,.42,"Verifier",GOLD_PALE)]:
        box(ax,x,y,w,h,col);label(ax,x+w/2,y+h/2,txt,8.5,ha="center")
    arrow(ax,(.77,1.50),(.96,1.50));line(ax,[.86,.86,.96],[1.5,.75,.75]);arrow(ax,(1.74,1.52),(1.99,1.52))
    arrow(ax,(2.37,1.25),(2.37,.99));arrow(ax,(1.74,.75),(1.99,.75))
    line(ax,[.91,2.77],[1.1,1.1],GOLD,ls=(0,(3,3)))
    # B: useful for corpus assembly; less clear separation of the hidden reference.
    for j,txt in enumerate(["Tasks", "Settings", "Seeds"]):
        box(ax,3.24+j*.83,1.50,.71,.35,TEAL_PALE);label(ax,3.595+j*.83,1.675,txt,8.5,ha="center")
        arrow(ax,(3.595+j*.83,1.47),(4.48,1.18))
    box(ax,3.93,.82,1.13,.34,BLUE_PALE);label(ax,4.495,.99,"Task entries",8.5,ha="center")
    arrow(ax,(4.495,.79),(4.495,.66));label(ax,4.495,.49,"Model → verifier",8.5,ha="center")
    # C: maximizes sample area, but obscures generation and scoring interfaces.
    box(ax,6.25,.54,.54,1.20,TEAL_PALE);label(ax,6.52,1.14,"Pool",8.5,ha="center")
    arrow(ax,(6.83,1.15),(7.15,1.15));box(ax,7.19,.56,1.35,1.24,BLUE_PALE)
    label(ax,7.865,1.49,"Question",8.5,ha="center");label(ax,7.865,1.15,"Response",8.5,ha="center")
    label(ax,7.865,.82,"Score",8.5,ha="center")
    label(ax,.13,.13,"Selected A: the information boundary is the central explanation.",9,color=TEAL)
    fig.savefig(out/"storyboards.svg",metadata={"Date":None});fig.savefig(out/"storyboards.png",dpi=110);plt.close(fig)

def draw(out):
    fig,ax=canvas()
    label(ax,.18,3.94,"Reasoning Gym",12,weight="bold")
    label(ax,1.82,3.94,"Generate a problem; verify the answer",11)
    label(ax,.18,3.66,"Procedural benchmark setup · one selected leg-counting example",9,color=MUTED)
    for x,w,title in [(.18,1.45,"a  Configure"),(2.04,2.20,"b  Generate one entry"),(4.69,2.11,"c  Answer and verify")]:
        label(ax,x,3.34,title,9.2,weight="bold");line(ax,[x,x+w],[3.22,3.22],LINE,lw=.7)

    # A real Quickstart configuration, not an invented experimental condition.
    box(ax,.18,.73,1.45,2.34,TEAL_PALE,TEAL)
    label(ax,.32,2.86,"Task generator",9.2,weight="bold",color=TEAL)
    box(ax,.30,2.42,1.20,.28,"white",TEAL,lw=.6)
    label(ax,.90,2.56,"leg_counting",9.2,ha="center")
    for y,l,r in [(2.15,"Seed","42"),(1.83,"Size","10"),(1.51,"Params","defaults")]:
        label(ax,.32,y,l,9,color=MUTED);label(ax,1.49,y,r,9,weight="bold",ha="right")
        line(ax,[.32,1.49],[y-.15,y-.15],"#CFDFD8",lw=.65)
    for k in reversed(range(3)):
        box(ax,.32+k*.04,.91+k*.045,.19,.23,"white",TEAL,lw=.6,radius=.015)
    label(ax,1.06,1.03,"10 entries",9,ha="center",color=TEAL)

    # One generated entry splits into what is shown and what is held by evaluation.
    line(ax,[1.66,1.83,1.83],[2.58,2.58,1.08],TEAL)
    arrow(ax,(1.83,2.58),(2.01,2.58),TEAL)
    arrow(ax,(1.83,1.08),(2.01,1.08),TEAL)
    ax.add_patch(Circle((1.83,2.58),.022,fc=TEAL,ec="none"))
    box(ax,2.04,1.92,2.20,1.15,BLUE_PALE,BLUE)
    label(ax,2.17,2.90,"TEXT QUESTION",8.5,weight="bold",color=BLUE)
    label(ax,2.17,2.68,"How many legs in total?",9.5)
    slug(ax,2.23,2.13,.67);deer(ax,3.28,2.08,.45)
    label(ax,2.55,2.055,"1 sea slug",8.5,ha="center")
    label(ax,3.49,2.055,"1 deer",8.5,ha="center")
    label(ax,3.14,1.79,"Only the question goes to the model",8.5,color=BLUE,ha="center")

    # The answer path has no environment action/observation loop.
    arrow(ax,(4.27,2.58),(4.72,2.58),BLUE)
    box(ax,4.75,2.29,1.92,.61,"white",BLUE)
    for j in range(3):
        box(ax,4.90+j*.034,2.45+j*.045,.28,.19,BLUE_PALE,BLUE,radius=.015,lw=.6)
    label(ax,5.37,2.595,"Reasoning model",9.2,weight="bold")
    arrow(ax,(5.72,2.26),(5.72,2.12),BLUE)
    box(ax,5.05,1.83,1.35,.28,BLUE_PALE,BLUE,lw=.6)
    label(ax,5.19,1.97,"Candidate:",9)
    label(ax,6.22,1.97,"4",12,weight="bold",ha="right",color=BLUE)

    line(ax,[2.00,6.80],[1.59,1.59],GOLD,ls=(0,(4,4)),lw=.8)
    label(ax,2.04,1.43,"HELD BY EVALUATOR",8.5,color=GOLD,weight="bold")
    box(ax,2.04,.73,2.20,.54,GOLD_PALE,GOLD)
    label(ax,2.17,1.11,"Reference answer: 4",9.5,weight="bold",color=GOLD)
    label(ax,2.17,.89,"Metadata: animal counts",8.5,color=MUTED)
    arrow(ax,(4.27,1.00),(4.63,1.00),GOLD)
    # Candidate passes down to the evaluator, never the reference up to the model.
    arrow(ax,(5.72,1.80),(5.72,1.27),BLUE)
    box(ax,4.66,.73,1.43,.52,GOLD_PALE,GOLD)
    label(ax,5.375,1.08,"Task verifier",9.5,weight="bold",color=GOLD,ha="center")
    label(ax,5.375,.88,"score_answer",8.5,ha="center")
    arrow(ax,(6.12,1.00),(6.35,1.00),GOLD)
    ax.add_patch(Circle((6.61,1.0),.22,fc=TEAL_PALE,ec=TEAL,lw=.9))
    label(ax,6.61,1.0,"1.0",10,weight="bold",ha="center",color=TEAL)
    label(ax,6.61,.65,"score",8.5,ha="center",color=MUTED)

    label(ax,.18,.42,"Schematic: drawings explain the text prompt; candidate 4 is illustrative (documented score: 1.0).",8.5,color=MUTED)
    label(ax,.18,.19,"Other tasks use their own verifiers and may accept multiple valid solutions.",8.5,color=MUTED)
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    text_bounds=[]; outside=[]
    for t in ax.texts:
        b=t.get_window_extent(renderer).transformed(fig.dpi_scale_trans.inverted())
        row={"text":t.get_text(),"font_pt":t.get_fontsize(),"bounds_in":[round(v,4) for v in (b.x0,b.y0,b.x1,b.y1)]}
        text_bounds.append(row)
        if b.x0<0 or b.y0<0 or b.x1>W or b.y1>H:outside.append(row)
    out.joinpath("geometry-check.json").write_text(json.dumps({"width_in":W,"height_in":H,"min_font_pt":min(t.get_fontsize() for t in ax.texts),"text_outside_canvas":outside,"text_bounds":text_bounds},indent=2)+"\n")
    assert not outside, outside
    for ext in ("svg","pdf","png"):
        metadata={"Creator":"Original vector study for Paper Figure Creation","CreationDate":None,"ModDate":None} if ext=="pdf" else ({"Date":None} if ext=="svg" else None)
        fig.savefig(out/f"figure.{ext}",dpi=220,metadata=metadata)
    plt.close(fig)
    # Proof the PDF itself, so an export/font issue cannot hide behind the PNG.
    with fitz.open(out/"figure.pdf") as doc:
        page=doc[0]
        page.get_pixmap(matrix=fitz.Matrix(110/72,110/72),alpha=False).save(out/"print-proof.png")
        out.joinpath("export-check.json").write_text(json.dumps({"pdf_pages":len(doc),"pdf_size_pt":[page.rect.width,page.rect.height],"pdf_fonts":[list(f) for f in page.get_fonts()],"proof_dpi":110,"proof_source":"figure.pdf","svg_text_editable":True},indent=2)+"\n")
    with Image.open(out/"print-proof.png") as im:
        im.convert("L").save(out/"grayscale-proof.png")

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output-dir",type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument("--storyboards-only",action="store_true");args=ap.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    matplotlib.rcParams.update({"svg.fonttype":"none","pdf.fonttype":42,"font.size":9,"svg.hashsalt":"reasoning-gym-setup-v1"})
    storyboards(args.output_dir)
    if not args.storyboards_only:draw(args.output_dir)

if __name__=="__main__":main()
