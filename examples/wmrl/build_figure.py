"""Original, source-grounded WMRL method diagram; deterministic editable vectors.

Run: python examples/wmrl/build_figure.py
Requires matplotlib and Pillow. Scientific sources and scope: brief.md.
The code sample is illustrative; no empirical chart or invented reward is drawn.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Circle, Polygon
from PIL import Image, ImageOps

OUT=Path(__file__).resolve().parent
C={'ink':'#172933','muted':'#526472','line':'#BAC5CC','blue':'#17628E',
   'blue_bg':'#EAF3F8','orange':'#A95022','orange_bg':'#FAF0E8',
   'green':'#287552','green_bg':'#EAF5EE','purple':'#7053A0','purple_bg':'#F0EBF7'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'svg.fonttype':'none',
    'pdf.fonttype':42,'ps.fonttype':42,'mathtext.fontset':'dejavusans','text.color':C['ink'],
    'savefig.facecolor':'white'})
fig=plt.figure(figsize=(7,3.92),dpi=150)
ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,7),ylim=(0,3.92));ax.axis('off')
texts=[]

def text(x,y,s,size=7.5,color=None,ha='left',weight='normal',va='center',**kw):
    t=ax.text(x,y,s,fontsize=size,color=color or C['ink'],ha=ha,va=va,
              weight=weight,zorder=8,**kw);texts.append(t);return t

def box(x,y,w,h,face='white',edge=None,rounding=.06,lw=.7,z=3):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={rounding}',
      facecolor=face,edgecolor=edge or C['line'],lw=lw,zorder=z);ax.add_patch(p);return p

def line(points,color=None,lw=.85,arrow=True,dash=False,z=2,rad=0):
    color=color or C['muted'];ls=(0,(3,2)) if dash else '-'
    if len(points)>2:
        ax.plot([p[0] for p in points[:-1]],[p[1] for p in points[:-1]],color=color,lw=lw,ls=ls,zorder=z)
    p=FancyArrowPatch(points[-2],points[-1],arrowstyle='-|>' if arrow else '-',
       mutation_scale=7,lw=lw,color=color,linestyle=ls,shrinkA=0,shrinkB=0,
       connectionstyle=f'arc3,rad={rad}',zorder=z);ax.add_patch(p)

def heading(x,n,label,w):
    ax.add_patch(Circle((x+.095,3.7),.095,fc=C['ink'],ec='none',zorder=3))
    text(x+.095,3.697,str(n),7.2,'white',ha='center',weight='bold')
    text(x+.25,3.7,label,8.5,weight='bold')
    ax.plot([x,x+w],[3.5,3.5],color=C['line'],lw=.65,zorder=1)

def robot(x,y,s=.18,color=None):
    color=color or C['blue']
    box(x-s*.57,y-s*.40,s*1.14,s*.82,'white',color,rounding=.035,lw=.85,z=5)
    for dx in [-.25,.25]:ax.add_patch(Circle((x+dx*s,y+.01*s),s*.08,fc=color,ec='none',zorder=6))
    ax.plot([x,x],[y+s*.42,y+s*.65],color=color,lw=.75,zorder=5)
    ax.add_patch(Circle((x,y+s*.68),s*.09,fc=color,ec='none',zorder=6))
    ax.plot([x-s*.16,x+s*.16],[y-s*.20,y-s*.20],color=color,lw=.65,zorder=5)

def terminal(x,y,w,h,color):
    box(x,y,w,h,'white',color,.035,.75,z=5)
    ax.plot([x,x+w],[y+h-.12,y+h-.12],color=color,lw=.6,zorder=6)
    for dx in [.065,.12,.175]:ax.add_patch(Circle((x+dx,y+h-.06),.013,fc=color,ec='none',zorder=6))
    text(x+.07,y+h-.24,'>_',7.5,color,weight='bold')

def globe(x,y,r=.10):
    ax.add_patch(Circle((x,y),r,fc='white',ec=C['green'],lw=.8,zorder=5))
    ax.plot([x-r,x+r],[y,y],color=C['green'],lw=.6,zorder=6)
    for off in [-.045,.045]:
        line([(x+off,y-r*.86),(x+off,y+r*.86)],C['green'],lw=.55,arrow=False,z=6,rad=.45 if off<0 else -.45)

def token(x,y,s,color,fill,w=.40,h=.30,size=11):
    box(x,y,w,h,fill,color,.045,.7,z=5);text(x+w/2,y+h/2,s,size,color,ha='center')

heading(.15,1,'Sample candidate groups',1.87)
heading(2.22,2,'Use anchors to calibrate',2.42)
heading(4.9,3,'Fuse gradient sums',1.93)

# Concrete task and a typed illustrative candidate, rather than anonymous input boxes.
box(.18,2.98,1.8,.40,C['blue_bg'],None,.05,.6)
text(.29,3.19,'Research question',8.5,C['blue'],weight='bold')
text(.29,3.055,'Improve a classifier',7.5)
line([(.58,2.98),(.58,2.72)],C['blue'])
robot(.58,2.57,.24)
text(.94,2.63,'Agent policy',8.5,weight='bold')
text(.94,2.46,r'$\pi_\theta$',10,C['blue'])
line([(.58,2.45),(.58,2.24)],C['blue'])

# Stacked code sheets expose what is generated. All candidates remain symbolic.
for off in [.09,.045,0]:box(.30+off,1.47+off,1.54,.70,'#F8FBFD',C['line'],.045,.6)
box(.30,1.47,1.54,.70,'white',C['blue'],.045,.75,z=5)
text(.39,2.055,'Candidate solution',8.0,C['blue'],weight='bold')
ax.plot([.30,1.84],[1.96,1.96],color=C['line'],lw=.6,zorder=6)
text(.39,1.82,'fit(X_train, y_train)',6.5,family='DejaVu Sans Mono')
text(.39,1.64,'score(X_val, y_val)',6.5,family='DejaVu Sans Mono')
text(1.07,1.32,'Illustrative code',7.0,C['muted'],ha='center',
     bbox={'facecolor':'white','edgecolor':'none','pad':1})

# Multiplicity is an explicit method object, with groups distinct from turns.
for i,(x,label) in enumerate([(.30,r'$G_1$'),(.86,r'$G_2$'),(1.42,r'$G_m$')]):
    for off in [.05,0]:box(x+off,.63+off,.40,.38,C['blue_bg'],C['blue'],.03,.55,z=3)
    text(x+.20,.82,label,10,C['blue'],ha='center')
text(1.33,.81,'…',10,C['muted'],ha='center')
line([(1.07,1.43),(1.07,1.07)],C['blue'])
text(1.08,.43,r'$n\geq2$ trajectories per group',7.2,C['muted'],ha='center')
text(1.08,.24,'Multi-turn detail condensed',7.0,C['muted'],ha='center')

# Anchor groups are scored twice. The real reward also directly supplies training.
box(2.22,2.39,2.42,.98,C['orange_bg'],None,.07,.6,z=1)
text(2.36,3.21,'Anchor groups',8.5,C['orange'],weight='bold')
text(4.48,3.21,'~10%',7.5,C['orange'],ha='right',weight='bold')
terminal(2.37,2.68,.29,.35,C['orange'])
text(2.74,2.94,'Real sandbox',8.5,C['orange'],weight='bold')
text(2.74,2.76,'execute candidate',7.0,C['muted'])
token(4.04,2.69,r'$r$',C['orange'],'white',.38,.30)
line([(3.73,2.85),(4.00,2.85)],C['orange'])
globe(2.515,2.53,.085)
text(2.74,2.52,'World model',8.5,C['green'],weight='bold')
token(4.04,2.40,r'$\hat r$',C['green'],'white',.38,.27)
line([(3.73,2.53),(4.00,2.53)],C['green'])

# Real and predicted rewards have shared candidate identity in the calibration pairs.
line([(4.23,2.40),(4.23,2.32)],C['purple'])
line([(4.23,2.69),(4.53,2.69),(4.53,2.34),(4.40,2.34),(4.40,2.32)],C['purple'])
box(2.66,1.84,1.83,.48,C['purple_bg'],C['purple'],.06,.8)
text(2.78,2.17,'Matched reward pairs',8.0,C['purple'],weight='bold')
text(2.80,1.96,r'$\mathcal{P}=\{(\hat r_j,r_j)\}$',10,C['purple'])
line([(3.58,1.84),(3.58,1.65)],C['purple'])
box(2.66,1.23,1.83,.42,'white',C['purple'],.06,1.0)
text(3.56,1.51,r'Fit $\hat f$ from anchor pairs',8.0,C['purple'],weight='bold',ha='center')
text(3.56,1.33,'Online monotone regression',7.0,C['muted'],ha='center')
line([(3.58,1.23),(3.58,1.06)],C['purple'])
box(2.66,.66,1.83,.40,C['purple_bg'],C['purple'],.06,.8)
text(3.56,.94,r'Apply the fitted $\hat f$',8.0,C['purple'],weight='bold',ha='center')
text(3.56,.76,r'$\hat r\ \mapsto\ \hat f(\hat r)$',10.5,C['purple'],ha='center')

# Other groups are cheap-scored only; their corrected reward enters training.
box(2.23,.12,2.41,.42,C['green_bg'],None,.05,.6,z=1)
globe(2.43,.33,.10)
text(2.64,.41,'Other groups',8.0,C['green'],weight='bold')
text(2.64,.23,'World-model reward',7.0)
token(4.02,.19,r'$\hat r$',C['green'],'white',.39,.27)
line([(4.24,.46),(4.24,.58),(4.56,.58),(4.56,.81),(4.50,.81)],C['green'])

# The two training streams keep their separate meanings after calibration.
line([(4.43,2.84),(4.82,2.84),(4.82,3.17),(5.02,3.17)],C['orange'])
box(5.02,2.66,1.68,.72,C['orange_bg'],C['orange'],.065,.7)
text(5.16,3.20,'Trusted stream',8.5,C['orange'],weight='bold')
text(5.17,2.99,r'$r\ \rightarrow\ A\ \rightarrow\ g_E$',12,C['orange'])
text(5.17,2.79,'Sum across anchor groups',7.0,C['muted'])
text(5.87,2.565,'A: group-relative advantage',7.0,C['muted'],ha='center')

line([(4.49,.98),(4.76,.98),(4.76,2.19),(5.02,2.19)],C['purple'])
box(5.02,1.76,1.68,.72,C['green_bg'],C['green'],.065,.7)
text(5.16,2.31,'Calibrated stream',8.5,C['green'],weight='bold')
text(5.17,2.10,r'$\hat f(\hat r)\ \rightarrow\ A\ \rightarrow\ g_{WM}$',11,C['green'])
text(5.17,1.89,'Sum across other groups',7.0,C['muted'])

# Weight annotation is explicit; no fake chart or measured numerical performance.
line([(6.70,3.04),(6.86,3.04),(6.86,1.18),(6.59,1.18)],C['orange'],z=4)
line([(5.83,1.76),(5.83,1.64),(4.93,1.64),(4.93,1.18),(5.10,1.18)],C['green'],z=4)
box(5.03,.60,1.67,.95,C['purple_bg'],C['purple'],.065,1,z=1)
text(5.87,1.44,'Inverse-variance weights',7.8,C['purple'],weight='bold',ha='center')
token(5.10,1.03,r'$\times V_{WM}^{-1}$',C['green'],'white',.60,.29,9.8)
token(5.99,1.03,r'$\times V_E^{-1}$',C['orange'],'white',.60,.29,9.8)
line([(5.42,1.03),(5.74,.84)],C['green'],z=4)
line([(6.28,1.03),(5.98,.84)],C['orange'],z=4)
text(5.87,.77,r'Sum & normalize $\rightarrow\ \hat g$',7.8,C['purple'],ha='center',weight='bold')
line([(5.86,.60),(5.86,.42)],C['purple'])
text(5.85,.26,r'Policy update $\theta\leftarrow\theta+\gamma\hat g$',8.4,C['purple'],ha='center',weight='bold')

# A narrow connector labels the cross-panel object instead of inventing a stage.
line([(1.90,.82),(2.13,.82),(2.13,2.81),(2.23,2.81)],C['blue'])
line([(2.13,.82),(2.13,.33),(2.22,.33)],C['blue'])

fig.canvas.draw();renderer=fig.canvas.get_renderer();bounds=fig.bbox
clipped=[]
for t in texts:
    b=t.get_window_extent(renderer)
    if b.x0<bounds.x0-.5 or b.y0<bounds.y0-.5 or b.x1>bounds.x1+.5 or b.y1>bounds.y1+.5:
        clipped.append(t.get_text())
if clipped:raise SystemExit('Canvas clipping: '+repr(clipped))
for ext in ['svg','pdf','png']:fig.savefig(OUT/f'wmrl-method.{ext}',dpi=300)
fig.savefig(OUT/'wmrl-method-print.png',dpi=110)
ImageOps.grayscale(Image.open(OUT/'wmrl-method-print.png').convert('RGB')).save(OUT/'wmrl-method-grayscale.png')
(OUT/'render-report.json').write_text(json.dumps({'figure_inches':[7,3.92],
    'source':'build_figure.py','canvas_clipping':clipped,'exact_measurement_charts':False,
    'semantic_validation':'Manual source review required; see review.md',
    'svg_text':'live text except math paths generated by matplotlib',
    'pdf_fonttype':42},indent=2)+'\n')
print('Rendered WMRL SVG, PDF, PNG, print and grayscale proofs.')
