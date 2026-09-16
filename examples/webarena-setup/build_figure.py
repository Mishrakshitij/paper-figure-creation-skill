#!/usr/bin/env python3
"""Original WebArena setup illustration. No browser episode or model is executed.

python examples/webarena-setup/build_figure.py [--output-dir PATH] [--thumbnails-only]
Requires matplotlib. SVG text remains editable; PDF embeds TrueType fonts.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

INK="#253442"; MUTED="#556574"; LINE="#B8C8D2"
BLUE="#2E6897"; PALEBLUE="#EDF3F9"; TEAL="#147F78"; PALETEAL="#EAF5F1"
ORANGE="#956327"; PALEORANGE="#FBF4E7"; LIGHT="#F5F7F9"
W,H=7,4.75

def text(ax,x,y,s,fs=8.5,c=INK,weight="normal",ha="left",va="center",**kw):
    return ax.text(x,y,s,fontsize=fs,color=c,fontweight=weight,ha=ha,va=va,**kw)

def box(ax,x,y,w,h,fc="white",ec=LINE,r=.035,lw=.7,**kw):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",
                    facecolor=fc,edgecolor=ec,linewidth=lw,**kw)
    ax.add_patch(p); return p

def arrow(ax,a,b,c=BLUE,style="-|>",lw=1.15,**kw):
    p=FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=8,color=c,linewidth=lw,**kw)
    ax.add_patch(p); return p

def path_arrow(ax,pts,c=BLUE,lw=1.1,dash=None):
    for a,b in zip(pts[:-2],pts[1:-1]):
        ax.plot([a[0],b[0]],[a[1],b[1]],color=c,lw=lw,linestyle=dash or "-",zorder=3)
    return arrow(ax,pts[-2],pts[-1],c=c,lw=lw,linestyle=dash or "-",zorder=3)

def site_icon(ax,x,y,kind,c):
    if kind=="shop":
        ax.add_patch(Polygon([(x-.12,y+.065),(x+.13,y+.065),(x+.09,y-.035),(x-.09,y-.035)],
                             facecolor="none",edgecolor=c,lw=1))
        ax.plot([x-.16,x-.13,x-.10],[y+.115,y+.115,y-.045],c=c,lw=1)
        for dx in [-.06,.065]: ax.add_patch(Circle((x+dx,y-.085),.018,fc=c,ec="none"))
    elif kind=="forum":
        box(ax,x-.14,y-.035,.24,.14,fc="white",ec=c,r=.025,lw=1)
        ax.plot([x-.08,x-.105,x-.04],[y-.035,y-.095,y-.035],c=c,lw=.9)
        box(ax,x-.025,y-.105,.18,.115,fc="white",ec=c,r=.02,lw=.8)
    elif kind=="code":
        ax.plot([x-.08,x-.08,x+.08,x+.08],[y-.10,y+.06,y+.06,y+.11],c=c,lw=1)
        for dx,dy in [(-.08,-.10),(-.08,.10),(.08,.11)]:
            ax.add_patch(Circle((x+dx,y+dy),.027,fc="white",ec=c,lw=1))
    elif kind=="cms":
        box(ax,x-.14,y-.105,.28,.22,ec=c,r=.018,lw=1)
        ax.plot([x-.12,x+.12],[y+.055]*2,c=c,lw=.8)
        for dx in [-.095,-.015,.065]:
            ax.add_patch(Rectangle((x+dx,y-.065),.05,.075,fc=c,ec="none",alpha=.6))

def browser(ax,x,y,w,h,state):
    box(ax,x,y,w,h,fc="white",ec=BLUE if state=="before" else TEAL,r=.045,lw=.85,zorder=4)
    box(ax,x+.01,y+h-.255,w-.02,.245,fc=PALEBLUE if state=="before" else PALETEAL,ec="none",r=.04,zorder=5)
    for i in range(3): ax.add_patch(Circle((x+.10+i*.07,y+h-.125),.018,fc=LINE,ec="none",zorder=6))
    text(ax,x+.35,y+h-.125,"/f/nyc  ·  Forum",fs=8.2,c=MUTED,zorder=6)
    if state=="before":
        text(ax,x+.14,y+h-.43,"New post",fs=8.7,weight="bold",zorder=6)
        text(ax,x+.14,y+.67,"Title",fs=7.9,c=MUTED,zorder=6)
        box(ax,x+.13,y+.35,w-.26,.23,fc=LIGHT,ec=LINE,r=.018,zorder=5)
        text(ax,x+.21,y+.465,"is car necessary in NYC",fs=8.0,zorder=6)
        box(ax,x+w-1.08,y+.065,.94,.235,fc=BLUE,ec=BLUE,r=.022,zorder=6)
        text(ax,x+w-.61,y+.182,"[42] Post",fs=8.2,c="white",weight="bold",ha="center",zorder=7)
        # A semantic cursor calls attention to the action target, not a fake click result.
        ax.add_patch(Polygon([(x+w-.10,y+.13),(x+w-.19,y+.33),(x+w-.25,y+.08)],
                             fc="white",ec=INK,lw=.75,zorder=8))
    else:
        text(ax,x+.14,y+h-.43,"nyc",fs=9.1,weight="bold",c=TEAL,zorder=6)
        ax.add_patch(Polygon([(x+.19,y+.55),(x+.13,y+.46),(x+.25,y+.46)],fc=LINE,ec="none",zorder=6))
        text(ax,x+.38,y+.515,"is car necessary in NYC",fs=8.0,weight="bold",zorder=6)
        text(ax,x+.38,y+.315,"New submission",fs=8,c=MUTED,zorder=6)
        ax.plot([x+.38,x+w-.13],[y+.17]*2,c=LINE,lw=.8,zorder=6)

def setup_figure(out):
    fig=plt.figure(figsize=(W,H),facecolor="white")
    ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,W);ax.set_ylim(0,H);ax.axis("off")
    text(ax,.18,4.55,"WebArena",fs=11.7,weight="bold")
    text(ax,1.30,4.55,"Complete real tasks on self-hosted websites",fs=10.2)
    # Environment context is a site inventory, distinct from the one task below.
    text(ax,.18,4.29,"a  The world",fs=9,weight="bold")
    text(ax,6.82,4.29,"Also: map, calculator, scratchpad and reference sites",fs=8,c=MUTED,ha="right")
    sites=[("shop","Shopping",.18,BLUE),("forum","Forum",1.89,TEAL),
           ("code","Code hosting",3.60,BLUE),("cms","Content admin",5.31,BLUE)]
    for kind,name,x,c in sites:
        width=1.51
        box(ax,x,3.83,width,.335,fc=PALETEAL if kind=="forum" else LIGHT,ec=c if kind=="forum" else LINE,r=.035,lw=.7)
        site_icon(ax,x+.22,3.996,kind,c)
        text(ax,x+.43,3.996,name,fs=8.0,c=c,weight="bold" if kind=="forum" else "normal")
    # Natural-language intent is public; it does not disclose the private evaluator target.
    box(ax,.18,3.34,6.64,.33,fc=PALEBLUE,ec="none",r=.025)
    text(ax,.31,3.505,"Goal",fs=8.6,c=BLUE,weight="bold")
    text(ax,.80,3.505,"Ask a suitable forum whether a car is necessary in New York City.",fs=8.6)
    text(ax,.18,3.13,"b  One interaction",fs=9,weight="bold")
    text(ax,6.82,3.13,"After navigation and typing · schematic UI / actions",fs=8,c=MUTED,ha="right")

    browser(ax,.18,1.73,2.25,1.24,"before")
    browser(ax,4.57,1.73,2.25,1.24,"after")
    text(ax,.18,1.59,"Current page",fs=8.5,c=BLUE)
    text(ax,6.82,1.59,"Website state changes",fs=8.5,c=TEAL,ha="right")
    # The same agent observes and acts; this is an interface contract, not its architecture.
    box(ax,2.92,2.34,1.16,.42,fc=PALEBLUE,ec=BLUE,r=.045,lw=.8,zorder=5)
    text(ax,3.50,2.55,"Any web agent",fs=8.6,weight="bold",ha="center",c=BLUE,zorder=6)
    arrow(ax,(2.45,2.55),(2.90,2.55))
    arrow(ax,(4.10,2.55),(4.55,2.55))
    text(ax,2.675,2.79,"observe",fs=7.7,c=BLUE,ha="center")
    text(ax,4.325,2.79,"act",fs=7.9,c=BLUE,ha="center")
    text(ax,3.50,2.13,"click [42]",fs=9,c=BLUE,ha="center",family="DejaVu Sans Mono")
    text(ax,3.50,1.92,"accessibility target",fs=7.8,c=MUTED,ha="center")
    # The new observation returns to the agent, not to the evaluator or hidden reference.
    path_arrow(ax,[(4.65,1.73),(4.65,1.42),(2.78,1.42),(2.78,2.36),(2.92,2.36)],c=TEAL)
    text(ax,3.73,1.55,"next observation",fs=8.1,c=TEAL,ha="center")

    # Programmatic evaluation is a separate lane and has no feedback edge into the agent.
    ax.plot([.18,6.82],[1.29,1.29],c=LINE,lw=.8,linestyle=(0,(3,3)))
    text(ax,.18,1.14,"c  Functional evaluation",fs=9,weight="bold",c=ORANGE)
    text(ax,6.82,1.14,"At completion · evaluator-only reference checks",fs=8,c=ORANGE,ha="right")
    box(ax,.18,.43,1.66,.53,fc=LIGHT,ec=LINE,r=.035)
    text(ax,.31,.775,"Completed episode",fs=8.4,weight="bold")
    text(ax,.31,.585,"Final URL + post DOM",fs=8.2,c=MUTED)
    arrow(ax,(1.87,.695),(2.13,.695),c=ORANGE)
    box(ax,2.16,.43,2.96,.53,fc=PALEORANGE,ec="#CCAB7D",r=.035)
    text(ax,2.30,.775,"Correct forum: /f/nyc",fs=8.5,c=ORANGE)
    text(ax,2.30,.585,"Post contains the requested question",fs=8.5,c=ORANGE)
    arrow(ax,(5.16,.695),(5.45,.695),c=ORANGE)
    text(ax,5.54,.78,"Success",fs=9.4,c=ORANGE,weight="bold")
    text(ax,5.54,.59,"if both checks pass",fs=8.2,c=ORANGE)
    text(ax,.18,.205,"Task 601, WebArena v0.2.0. UI, element ID and single-step sequence are illustrative; no agent run.",fs=7.9,c=MUTED)
    text(ax,.18,.065,"Observations: URL / tabs + screenshot, HTML or accessibility tree. Target ID [42] illustrates the latter.",fs=7.5,c=MUTED)
    fig.canvas.draw()
    ren=fig.canvas.get_renderer(); bounds=fig.bbox
    outside=[]
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text():continue
        b=t.get_window_extent(ren)
        if b.x0<bounds.x0-.5 or b.y0<bounds.y0-.5 or b.x1>bounds.x1+.5 or b.y1>bounds.y1+.5:outside.append(t.get_text())
    if outside:raise ValueError(f"Text outside canvas: {outside}")
    for ext in ("png","svg","pdf"):
        fig.savefig(out/f"figure.{ext}",dpi=220,facecolor="white")
    fig.savefig(out/"print-proof.png",dpi=110,facecolor="white")
    plt.close(fig)
    (out/"geometry-check.json").write_text(json.dumps({"width_in":W,"height_in":H,
        "text_outside_canvas":outside,"minimum_font_pt":7.5,"primary_font_pt":"8–9.4",
        "main_png_dpi":220,"proof_png_dpi":110,"data_status":"schematic episode, sourced task contract",
        "observed_episode":False,"diagram_kind":"benchmark_environment",
        "limitations":["No layout-overlap solver; rendered figure must also be visually inspected.",
                        "No actual manuscript page supplied; venue-size proof is 7 inches wide."]},indent=2)+"\n")

def thumbnails(out):
    fig,axes=plt.subplots(1,3,figsize=(10.5,2.35),facecolor="white")
    for ax in axes:ax.set_xlim(0,3.4);ax.set_ylim(0,2.1);ax.axis("off")
    for ax,title in zip(axes,["A  World + visible state change","B  Agent surrounded by websites","C  Task / interaction / evaluator lanes"]):
        text(ax,.05,2.00,title,fs=8.7,weight="bold")
    a=axes[0]
    for i,n in enumerate(["Shop","Forum","Code","CMS"]):
        box(a,.05+i*.83,1.57,.75,.22,fc=PALETEAL if i==1 else LIGHT);text(a,.425+i*.83,1.68,n,fs=7,ha="center")
    text(a,.08,1.36,"Ask if a car is needed in NYC",fs=7.5)
    for x,n,c in [(.05,"Composer",BLUE),(1.28,"Agent",BLUE),(2.37,"Posted",TEAL)]:
        box(a,x,.68,.94,.46,fc=PALEBLUE if c==BLUE else PALETEAL);text(a,x+.47,.91,n,fs=8,ha="center",c=c)
    arrow(a,(1,.91),(1.26,.91));arrow(a,(2.23,.91),(2.35,.91))
    text(a,.06,.43,"Private checks → correct forum + text",fs=7.4,c=ORANGE)
    text(a,.05,.12,"CHOSEN · State transition stays concrete",fs=7.2,weight="bold",c=TEAL)
    a=axes[1];box(a,1.25,.87,.84,.44,fc=PALEBLUE);text(a,1.67,1.09,"Agent",fs=8,ha="center")
    for x,y,n in [(.08,1.52,"Forum"),(2.5,1.52,"Shop"),(.08,.40,"Code"),(2.5,.40,"CMS")]:
        box(a,x,y,.75,.32);text(a,x+.375,y+.16,n,fs=7.5,ha="center");arrow(a,(1.67,1.09),(x+.375,y+.16),lw=.65)
    text(a,.06,.09,"Broad context; hides what an action changes",fs=7.0,c=MUTED)
    a=axes[2]
    for y,l,c in [(1.48,"Task  →  start page",BLUE),(.93,"Observe  →  act  →  new page",TEAL),(.38,"Private checks  →  success",ORANGE)]:
        box(a,.08,y,3.15,.34,fc=LIGHT);text(a,.19,y+.17,l,fs=7.7,c=c)
    text(a,.06,.09,"Clear roles; needs more room for a real UI",fs=7,c=MUTED)
    fig.subplots_adjust(left=.015,right=.985,bottom=.03,top=.99,wspace=.12)
    for ext in ("png","svg"):fig.savefig(out/f"composition-thumbnails.{ext}",dpi=140)
    plt.close(fig)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output-dir",type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument("--thumbnails-only",action="store_true");args=ap.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    matplotlib.rcParams.update({"font.family":"DejaVu Sans","svg.fonttype":"none","pdf.fonttype":42,"ps.fonttype":42})
    thumbnails(args.output_dir)
    if not args.thumbnails_only:setup_figure(args.output_dir)
if __name__=="__main__":main()
