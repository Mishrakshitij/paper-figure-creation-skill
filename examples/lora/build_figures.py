"""Rebuild LoRA publication-scale figures from the adjacent evidence/spec JSON.

Dependencies: Python 3, matplotlib, numpy, Pillow. All geometry is deterministic.
Run create_specs.py, then this script with --skill-root if it is outside the repo.
The skill's live evidence validator supplies all displayed differences.
"""
import json
import argparse
import importlib.util
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
import numpy as np
from PIL import Image, ImageOps

OUT = Path(__file__).resolve().parent
S = json.loads((OUT/'teaser.spec.json').read_text())
M = json.loads((OUT/'method.spec.json').read_text())
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--skill-root',type=Path,help='Directory containing the paper-figure-creation SKILL.md and scripts/')
args=parser.parse_args()
if args.skill_root:
    candidates=[args.skill_root.resolve()/'scripts'/'validate_evidence.py']
else:
    candidates=[]
    for parent in [OUT,*OUT.parents]:
        candidates.extend([parent/'scripts'/'validate_evidence.py',
            parent/'skills'/'paper-figure-creation'/'scripts'/'validate_evidence.py'])
validator_path=next((p for p in candidates if p.is_file()),None)
if validator_path is None:
    raise SystemExit('Cannot locate live evidence validator. Pass --skill-root /path/to/paper-figure-creation.')
module_spec=importlib.util.spec_from_file_location('lora_evidence_validator',validator_path)
validator=importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(validator)
REPORT=validator.validate_spec(S)
METHOD_REPORT=validator.validate_spec(M)
for name,report in [('evidence-review.json',REPORT),('method-evidence-review.json',METHOD_REPORT)]:
    (OUT/name).write_text(json.dumps(report,indent=2)+'\n')
    if not report['valid']:
        raise SystemExit(f'Live evidence validation failed; see {name}.')
R = {r['id']:r for r in S['evidence']['results']}
C = {c['id']:c for c in REPORT['computed_claims']}
INK = '#17232B'
MUTED = '#52616B'
ACC = '#007D8A'
LIGHT = '#E6F2F3'
GRID = '#CBD3D8'
PANEL = '#F5F7F8'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,
    'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,
    'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,
    'axes.edgecolor':MUTED,'axes.linewidth':0.7,'savefig.facecolor':'white'})

def canvas(width,height):
    fig=plt.figure(figsize=(width,height),dpi=150)
    ax=fig.add_axes([0,0,1,1]); ax.set(xlim=(0,width),ylim=(0,height)); ax.axis('off')
    return fig,ax

def txt(ax,x,y,s,size=8.5,ha='left',va='center',color=INK,weight='normal',**kw):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,weight=weight,**kw)

def line(ax,points,color=MUTED,lw=0.9,arrow=False,dashed=False):
    points=np.asarray(points)
    style=(0,(3,2)) if dashed else '-'
    if len(points)>2:
        ax.plot(points[:-1,0],points[:-1,1],color=color,lw=lw,ls=style,zorder=2)
    a=FancyArrowPatch(points[-2],points[-1],arrowstyle='-|>' if arrow else '-',
        mutation_scale=7.8,lw=lw,color=color,linestyle=style,shrinkA=0,shrinkB=0,zorder=2)
    ax.add_patch(a)

def matrix(ax,x,y,w,h,rows,cols,accent=False,dashed=False):
    edge=ACC if accent else MUTED
    ax.add_patch(Rectangle((x,y),w,h,fc=LIGHT if accent else PANEL,ec=edge,lw=1,
        linestyle=(0,(3,2)) if dashed else '-',zorder=3))
    for i in range(1,cols): ax.plot([x+i*w/cols]*2,[y,y+h],color=edge,lw=.25,alpha=.50,zorder=3)
    for i in range(1,rows): ax.plot([x,x+w],[y+i*h/rows]*2,color=edge,lw=.25,alpha=.50,zorder=3)

def box(ax,x,y,w,h,text,accent=False,size=8.5,dashed=False):
    ax.add_patch(Rectangle((x,y),w,h,fc=LIGHT if accent else PANEL,
        ec=ACC if accent else MUTED,lw=.85,linestyle=(0,(3,2)) if dashed else '-',zorder=3))
    txt(ax,x+w/2,y+h/2,text,size=size,ha='center',color=ACC if accent else INK)

def export(fig,name):
    for ext in ('svg','pdf','png'):
        fig.savefig(OUT/f'{name}.{ext}',dpi=300)
    fig.savefig(OUT/f'{name}-print.png',dpi=100)
    image=Image.open(OUT/f'{name}-print.png').convert('RGB')
    ImageOps.grayscale(image).save(OUT/f'{name}-grayscale.png')
    # Check all actual text bounding boxes against the physical figure canvas.
    fig.canvas.draw(); rend=fig.canvas.get_renderer(); bounds=fig.bbox
    clipped=[]
    for text in fig.findobj(matplotlib.text.Text):
        if not text.get_visible() or not text.get_text(): continue
        bb=text.get_window_extent(rend)
        if bb.x0<bounds.x0-.5 or bb.y0<bounds.y0-.5 or bb.x1>bounds.x1+.5 or bb.y1>bounds.y1+.5:
            clipped.append(text.get_text())
    (OUT/f'{name}-bounds.json').write_text(json.dumps({'canvas_inches':list(fig.get_size_inches()),'text_outside_canvas':clipped},indent=2)+'\n')
    assert not clipped, clipped
    plt.close(fig)

def teaser_figure():
    fig,ax=canvas(7,4.1)
    txt(ax,.18,3.89,S['figure']['title'],size=11.2,weight='bold')
    txt(ax,.18,3.49,'a  Task and idea',size=9.6,weight='bold')
    txt(ax,2.52,3.54,'b  GPT-3 175B: reported validation results',size=9.6,weight='bold')
    line(ax,[(2.41,.73),(2.41,3.61)],color=GRID,lw=.7)
    txt(ax,.18,3.18,'Adapt a language model\nto a downstream task.',size=9.0,va='top',linespacing=1.35)
    txt(ax,.18,2.71,'Learn a low-rank weight update',size=8.5,weight='bold')
    matrix(ax,.24,1.99,.65,.56,5,6,dashed=True)
    txt(ax,1.04,2.29,'+',size=14,ha='center')
    matrix(ax,1.20,1.99,.15,.56,5,2,accent=True)
    txt(ax,1.43,2.29,'×',size=12,ha='center')
    matrix(ax,1.53,2.21,.64,.14,2,6,accent=True)
    txt(ax,.57,1.82,r'$W_0$',size=10,ha='center')
    txt(ax,.57,1.61,'frozen',size=8.5,ha='center')
    txt(ax,1.26,1.82,r'$B$',size=10,ha='center',color=ACC)
    txt(ax,1.85,1.82,r'$A$',size=10,ha='center',color=ACC)
    txt(ax,1.67,1.61,'trainable',size=8.5,ha='center',color=ACC)
    txt(ax,.18,1.37,r'$h=W_0x+(\alpha/r)\,B(Ax)$',size=10.0)
    ax.add_patch(Rectangle((.18,.55),2.14,.62,fc=PANEL,ec=GRID,lw=.6))
    txt(ax,.28,1.04,'NL-to-SQL example (schematic)',size=8.0,weight='bold')
    txt(ax,.28,.84,'How many teams?',size=8.5)
    txt(ax,.28,.64,'→  SELECT COUNT(*) FROM teams',size=8.0)

    y0,dy=3.06,.265
    ids=S['row_order']; ys=np.array([y0-i*dy for i in range(len(ids))])
    txt(ax,2.52,3.29,'Method',size=8.3,weight='bold')
    txt(ax,3.45,3.30,'Trainable\n(M) ↓',size=8.0,ha='center',weight='bold',linespacing=1.05)
    for i,mid in enumerate(ids):
        if mid.startswith('lora'):
            ax.add_patch(Rectangle((2.49,ys[i]-.113),4.33,.226,fc=LIGHT,ec='none',zorder=0))
        txt(ax,2.52,ys[i],S['method_labels'][mid],size=8.3,
            weight='bold' if mid.startswith('lora') else 'normal',color=ACC if mid.startswith('lora') else INK)
        # All parameter values use the reported one-decimal precision.
        txt(ax,3.70,ys[i],f"{R[mid+'_params']['value']:,.1f}",size=8.1,ha='right',color=ACC if mid.startswith('lora') else INK)
    line(ax,[(2.52,3.17),(6.82,3.17)],color=GRID,lw=.6)
    bottom,top=.92,3.18
    for metric,x,w,title,ticks in [('wiki',3.95,1.29,'WikiSQL',[65,70,75]),('mnli',5.56,1.25,'MNLI-m',[89,90,91,92])]:
        chart=fig.add_axes([x/7,bottom/4.1,w/7,(top-bottom)/4.1],facecolor='none')
        chart.set_xlim(*S['layout']['axis_limits'][metric]); chart.set_ylim(bottom,top)
        chart.set_xticks(ticks); chart.set_yticks([])
        chart.tick_params(axis='x',labelsize=8,length=3,pad=3)
        for side in ['left','right','top']: chart.spines[side].set_visible(False)
        chart.grid(axis='x',color=GRID,lw=.5,zorder=0)
        chart.set_axisbelow(True)
        chart.set_title(title,fontsize=8.5,weight='bold',pad=6)
        for mid,y in zip(ids,ys):
            proposed=mid.startswith('lora'); val=R[f'{mid}_{metric}']['value']
            chart.plot(val,y,marker='D' if proposed else 'o',ms=4.3 if proposed else 4.0,
                mfc=ACC if proposed else 'white',mec=ACC if proposed else MUTED,mew=.9,zorder=3)
            chart.annotate(f'{val:.1f}',(val,y),xytext=(4,0),textcoords='offset points',
                fontsize=8.0,va='center',color=ACC if proposed else INK)
    txt(ax,5.37,.62,'Accuracy (%) ↑; separate scales',size=8.2,ha='center')
    delta_w=C['wiki_delta']['value']; delta_m=C['mnli_delta']['value']
    txt(ax,2.52,.40,f'4.7M LoRA vs full FT:  {delta_w:+.1f} pp WikiSQL;  {delta_m:+.1f} pp MNLI-m',size=8.4,weight='bold')
    txt(ax,.18,.18,'Table 4, Hu et al. (2021), v2. Typical seed SD: WikiSQL ≈0.5 pp; MNLI-m ≈0.1 pp. No per-entry intervals.',size=8.0)
    export(fig,'lora-teaser')

def method_figure():
    fig,ax=canvas(7,4.6)
    txt(ax,.18,4.38,M['figure']['title'],size=11.2,weight='bold')
    txt(ax,.18,4.12,'One adapted projection; repeated Transformer computation is omitted.',size=8.5,color=MUTED)
    ax.add_patch(Rectangle((.18,1.56),6.64,2.32,fc='white',ec=GRID,lw=.7))
    txt(ax,.33,3.69,'a  Training',size=9.7,weight='bold')
    txt(ax,2.02,3.69,r'$W_0\in\mathbb{R}^{d\times k}$  • frozen',size=8.8,ha='center')
    matrix(ax,1.41,3.00,1.22,.48,4,9,dashed=True)
    txt(ax,.46,2.79,r'$x\in\mathbb{R}^{k}$',size=10,ha='center')
    # Both branches receive the same input x. A junction indicates a split.
    line(ax,[(.75,2.79),(.93,2.79)],arrow=False)
    ax.add_patch(Circle((.93,2.79),.025,fc=MUTED,ec='none',zorder=4))
    line(ax,[(.93,2.79),(.93,3.24),(1.41,3.24)],arrow=True)
    line(ax,[(2.63,3.24),(5.05,3.24),(5.05,2.93)],arrow=True)
    txt(ax,3.79,3.43,r'$W_0x\in\mathbb{R}^{d}$',size=9,ha='center')
    line(ax,[(.93,2.79),(.93,2.26),(1.41,2.26)],color=ACC,arrow=True)
    matrix(ax,1.41,2.16,.92,.20,2,8,accent=True)
    txt(ax,1.87,2.57,r'$A\in\mathbb{R}^{r\times k}$',size=9,ha='center',color=ACC)
    txt(ax,1.87,1.96,'trainable; Gaussian init.',size=8.0,ha='center')
    matrix(ax,3.05,1.96,.24,.60,6,2,accent=True)
    txt(ax,3.17,2.76,r'$B\in\mathbb{R}^{d\times r}$',size=9,ha='center',color=ACC)
    txt(ax,3.17,1.84,'trainable; zero init.',size=8.0,ha='center')
    line(ax,[(2.33,2.26),(3.05,2.26)],color=ACC,arrow=True)
    txt(ax,2.67,2.43,r'$Ax\in\mathbb{R}^{r}$',size=8.5,ha='center')
    box(ax,4.02,2.02,.64,.48,r'$\times\,\alpha/r$',accent=True,size=10)
    line(ax,[(3.29,2.26),(4.02,2.26)],color=ACC,arrow=True)
    txt(ax,3.67,2.46,r'$BAx$',size=8.8,ha='center')
    line(ax,[(4.66,2.26),(5.05,2.26),(5.05,2.65)],color=ACC,arrow=True)
    ax.add_patch(Circle((5.05,2.79),.14,fc='white',ec=INK,lw=1,zorder=4))
    txt(ax,5.05,2.79,'+',size=13,ha='center',zorder=6)
    line(ax,[(5.19,2.79),(5.80,2.79)],arrow=True)
    txt(ax,6.12,2.79,r'$h\in\mathbb{R}^{d}$',size=10,ha='center')
    txt(ax,5.82,2.43,'to remaining LM',size=8.3,ha='center',color=MUTED)
    txt(ax,.33,1.65,'Task loss updates A and B; W₀ remains frozen.',size=8.3)
    txt(ax,.33,1.40,r'$h=W_0x+sB(Ax),\quad s=\alpha/r,\quad r\ll\min(d,k)$',size=10)
    ax.add_patch(Rectangle((.18,.28),6.64,.93,fc=PANEL,ec=GRID,lw=.7))
    txt(ax,.33,1.02,'b  Merged inference',size=9.7,weight='bold')
    txt(ax,.65,.61,r'$x$',size=11,ha='center')
    line(ax,[(.93,.61),(2.13,.61)],arrow=True)
    box(ax,2.13,.35,2.72,.52,r'$W_{\mathrm{merged}}=W_0+sBA$',size=10)
    line(ax,[(4.85,.61),(5.84,.61)],arrow=True)
    txt(ax,6.15,.61,r'$h$',size=11,ha='center')
    txt(ax,.18,.12,'Merge once for a fixed task; inference uses a single dense projection. No separate LoRA branch remains.',size=8.1)
    export(fig,'lora-method')

def storyboards():
    fig,ax=canvas(7,4)
    txt(ax,.2,3.78,'Composition alternatives considered before detailed rendering',size=10,weight='bold')
    for y,label,right in [(2.3,'Teaser A • selected','Aligned rows: method / parameters / two dot plots'),(.85,'Teaser B','Two quality–parameter scatterplots + legend')]:
        txt(ax,.2,y+1.1,label,size=9,weight='bold')
        box(ax,.2,y,2.1,.86,'Task example\n+ low-rank matrix idea',accent=True,size=9)
        box(ax,2.48,y,4.32,.86,right,size=8.8)
    txt(ax,.2,.25,'Method A (selected): training residual lane above merged inference. Method B: residual + merge note.',size=8.0)
    for ext in ('svg','png'): fig.savefig(OUT/f'composition-alternatives.{ext}',dpi=150)
    plt.close(fig)

if __name__=='__main__':
    storyboards(); teaser_figure(); method_figure()
    print('Built editable SVG, embedded-font PDF, 300dpi PNG and print/grayscale reviews for both figures.')
