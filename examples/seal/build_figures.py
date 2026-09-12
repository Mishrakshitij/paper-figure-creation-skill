#!/usr/bin/env python3
"""Original SEAL figure redesigns. Rebuilds without network; evidence checked live."""
from pathlib import Path
import argparse, importlib.util, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon, Circle
from matplotlib.path import Path as MPath
from PIL import Image, ImageOps

OUT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(); ap.add_argument('--skill-root',type=Path); ARGS=ap.parse_args()
candidates=[ARGS.skill_root] if ARGS.skill_root else [p/'skills/paper-figure-creation' for p in OUT.parents]
ROOT=next((p for p in candidates if p and (p/'scripts/validate_evidence.py').is_file()),None)
if ROOT is None: raise SystemExit('Use --skill-root PATH to the paper-figure-creation skill.')
ms=importlib.util.spec_from_file_location('evidence',ROOT/'scripts/validate_evidence.py'); ev=importlib.util.module_from_spec(ms); ms.loader.exec_module(ev)
S=json.loads((OUT/'teaser.spec.json').read_text()); M=json.loads((OUT/'method.spec.json').read_text())
for spec,name in [(S,'teaser'),(M,'method')]:
 report=ev.validate_spec(spec); (OUT/(name+'-evidence-review.json')).write_text(json.dumps(report,indent=2)+'\n')
 if not report['valid']: raise SystemExit(report)
R={r['id']:r for r in S['evidence']['results']}
INK='#25323C'; MUTED='#5E6C75'; HAIR='#D4DBDF'; BLUE='#497F9B'; BLUEL='#E9F3F7'; AMBER='#AD6C19'; AMBERL='#FFF0CF'; PURPLE='#7765A8'; PURPLEL='#EFEAF8'; TEAL='#217A70'; TEALL='#E4F3ED'; CORAL='#B84F37'; CORALL='#FBE8E1'; GRAY='#85919A'; LIGHT='#F5F7F8'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED,'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,'axes.linewidth':.55,'savefig.facecolor':'white'})

def canvas(h):
 f=plt.figure(figsize=(7,h),dpi=150); a=f.add_axes([0,0,1,1]); a.set(xlim=(0,7),ylim=(0,h)); a.axis('off'); return f,a

def text(a,x,y,s,size=8.5,ha='left',va='center',color=INK,weight='normal',**kw): return a.text(x,y,s,size=size,ha=ha,va=va,color=color,weight=weight,**kw)
def line(a,points,color=MUTED,lw=.8,style='-',z=2):
 q=np.array(points);a.plot(q[:,0],q[:,1],color=color,lw=lw,ls=style,zorder=z)
def arrow(a,p,q,color=MUTED,lw=.9,rad=0,style='-',z=4):
 a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=8,lw=lw,color=color,connectionstyle=f'arc3,rad={rad}',linestyle=style,shrinkA=0,shrinkB=0,zorder=z))
def route(a,pts,color=MUTED,lw=.9,style='-'):
 if len(pts)>2: line(a,pts[:-1],color,lw,style)
 arrow(a,pts[-2],pts[-1],color,lw,style=style)
def box(a,x,y,w,h,fc='white',ec=HAIR,rounding=.055,lw=.75,z=3,style='-'):
 p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={rounding}',fc=fc,ec=ec,lw=lw,linestyle=style,zorder=z);a.add_patch(p);return p

def document(a,x,y,w,h,title,lines,fc=AMBERL,accent=AMBER,size=8.5):
 # A folded corner identifies a data object, rather than another operation box.
 fold=.13
 a.add_patch(Polygon([(x,y),(x+w,y),(x+w,y+h-fold),(x+w-fold,y+h),(x,y+h)],closed=True,fc=fc,ec=accent,lw=.75,zorder=3))
 line(a,[(x+w-fold,y+h),(x+w-fold,y+h-fold),(x+w,y+h-fold)],accent,.65,z=4)
 text(a,x+.10,y+h-.16,title,size=size,weight='bold',color=accent,zorder=5)
 for i,s in enumerate(lines):text(a,x+.10,y+h-.37-.155*i,s,size=size,zorder=5)

def chip(a,x,y,w,h,label,accent=CORAL,fc=CORALL,small=False):
 # Consistent parameter-chip identity across policy, candidate copies and deployment.
 for xx in np.linspace(x+.13,x+w-.13,4):
  line(a,[(xx,y-.045),(xx,y)],accent,.6); line(a,[(xx,y+h),(xx,y+h+.045)],accent,.6)
 for yy in np.linspace(y+.1,y+h-.1,3):
  line(a,[(x-.045,yy),(x,yy)],accent,.6); line(a,[(x+w,yy),(x+w+.045,yy)],accent,.6)
 box(a,x,y,w,h,fc,accent,rounding=.06,lw=.85)
 text(a,x+w/2,y+h*.60,label,size=10.4 if not small else 9.3,ha='center',zorder=5)
 text(a,x+w/2,y+h*.24,'LM',size=7.6,ha='center',color=accent,zorder=5)

def status(a,x,y,ok=True,r=.10):
 a.add_patch(Circle((x,y),r,fc=TEALL if ok else LIGHT,ec=TEAL if ok else GRAY,lw=.7,zorder=4))
 if ok: line(a,[(x-r*.5,y),(x-r*.1,y-r*.35),(x+r*.5,y+r*.4)],TEAL,1.2,z=5)
 else:
  line(a,[(x-r*.35,y-r*.35),(x+r*.35,y+r*.35)],GRAY,1,z=5);line(a,[(x-r*.35,y+r*.35),(x+r*.35,y-r*.35)],GRAY,1,z=5)

def grid(a,x,y,data,cell=.07,accent=BLUE):
 for j,row in enumerate(data):
  for i,v in enumerate(row):a.add_patch(Rectangle((x+i*cell,y+(len(data)-1-j)*cell),cell*.91,cell*.91,fc=accent if v else '#DFE5E8',ec='none',zorder=4))

def export(f,name):
 f.canvas.draw(); rend=f.canvas.get_renderer(); bounds=f.bbox; clipped=[]
 for t in f.findobj(matplotlib.text.Text):
  if not t.get_visible() or not t.get_text():continue
  b=t.get_window_extent(rend)
  if b.x0<bounds.x0-.5 or b.y0<bounds.y0-.5 or b.x1>bounds.x1+.5 or b.y1>bounds.y1+.5:clipped.append(t.get_text())
 (OUT/(name+'-bounds.json')).write_text(json.dumps({'canvas_inches':list(f.get_size_inches()),'text_outside_canvas':clipped},indent=2)+'\n')
 if clipped: raise RuntimeError(clipped)
 for ext in ['svg','pdf','png']:f.savefig(OUT/(name+'.'+ext),dpi=300)
 f.savefig(OUT/(name+'-print.png'),dpi=100)
 ImageOps.grayscale(Image.open(OUT/(name+'-print.png')).convert('RGB')).save(OUT/(name+'-grayscale.png'))
 plt.close(f)

def teaser_figure():
 f,a=canvas(4.8)
 text(a,.18,4.58,'SEAL',size=15,weight='bold',color=CORAL)
 text(a,.91,4.58,'Learn how to write your own training data',size=12.3,weight='bold')
 text(a,.18,4.30,'(a)  Write, update, recall',size=9.0,weight='bold')
 text(a,2.70,4.30,'(b)  Retain new knowledge',size=9.0,weight='bold')
 line(a,[(2.5,.32),(2.5,4.36)],HAIR,.65)
 # Concrete concept, linked throughout by one small fictional fact.
 document(a,.23,3.37,2.04,.68,'NEW PASSAGE',['Planet Lyra orbits two suns.'],BLUEL,BLUE,8.5)
 arrow(a,(1.25,3.33),(1.25,3.06),CORAL)
 text(a,1.43,3.19,'RL-trained LM',size=7.9,color=CORAL)
 document(a,.23,2.30,2.04,.74,'SELF-EDIT',['Lyra is a planet.','Lyra has two suns.'],size=8.5)
 arrow(a,(1.25,2.27),(1.25,2.02),PURPLE)
 box(a,.26,1.24,1.98,.75,PURPLEL,'#C4B8DC',rounding=.07)
 chip(a,.41,1.38,.50,.39,r'$\theta$');arrow(a,(1.01,1.57),(1.49,1.57),PURPLE)
 chip(a,1.60,1.38,.50,.39,r"$\theta'$",small=True)
 text(a,1.25,1.86,'Train on passage + self-edit',size=8.4,ha='center',color=PURPLE)
 arrow(a,(1.25,1.2),(1.25,.97),BLUE)
 box(a,.23,.47,2.04,.48,BLUEL,'#C1D8E3',rounding=.06)
 text(a,.34,.80,'How many suns does Lyra have?',size=8.1)
 text(a,.35,.60,'Two.',size=9.4,weight='bold',color=TEAL);status(a,.85,.60,True,r=.068)
 text(a,1.13,.60,'Passage absent',size=7.9,color=BLUE)
 route(a,[(.23,.69),(.14,.69),(.14,3.19),(1.14,3.19)],TEAL,.80,style=(0,(3,2)))
 text(a,.08,1.96,'Recall reward · RL training only',size=7.3,ha='center',color=TEAL,rotation=90)
 text(a,.23,.23,'Illustrative example; not a model transcript.',size=7.4,color=MUTED)
 # Dot-table: all source rows, common scale, no hidden unfavorable regimes.
 text(a,2.70,4.08,'Qwen2.5-7B · SQuAD · no-passage accuracy (%) ↑',size=8.3,color=MUTED)
 cols=[4.35,5.30,6.25]; lefts=[3.91,4.86,5.81]; plotw=.66
 for x,(s,ttl,sub) in zip(cols,[('single','1 passage','LoRA'),('cpt200','200 passages','full finetuning'),('cpt2067','2,067 passages','full finetuning')]):
  text(a,x,3.82,ttl,size=7.8,ha='center',weight='bold');text(a,x,3.63,sub,size=7.6,ha='center',color=MUTED)
 ys=[3.29,2.92,2.55,2.18,1.81]
 for i,(mid,y) in enumerate(zip(S['row_order'],ys)):
  color=CORAL if mid=='seal' else PURPLE if mid=='gpt41' else GRAY
  if mid=='seal':box(a,2.65,y-.17,4.16,.33,CORALL,'none',rounding=.035,z=0)
  label={'base':'Base model','passage':'Passage only','synthetic':'Self-generated\n(no RL)','gpt41':'GPT-4.1 data','seal':'SEAL'}[mid]
  text(a,2.72,y,label,size=8.1,weight='bold' if mid=='seal' else 'normal',color=CORAL if mid=='seal' else INK,linespacing=1.02)
  for x,(sid,_,_) in zip(lefts,S['settings']):
   v=R[mid+'_'+sid]['value'];xx=x+v/65*plotw
   line(a,[(x,y),(x+plotw,y)],HAIR,.5,z=1)
   line(a,[(x,y),(xx,y)],color,1.3,z=2)
   a.plot(xx,y,'D' if mid=='seal' else 'o',markersize=3.9 if mid=='seal' else 3.4,color=color,zorder=4)
   text(a,xx+.045,y+.093,f'{v:.1f}',size=7.8,color=color,weight='bold' if v==max(R[m+'_'+sid]['value'] for m in S['row_order']) else 'normal',zorder=5)
 text(a,2.72,1.51,'Bold: column best',size=7.2,color=MUTED)
 for x in lefts:
  text(a,x,1.51,'0',size=7.2,color=MUTED,ha='center');text(a,x+plotw,1.51,'65',size=7.2,color=MUTED,ha='center')
 text(a,2.72,1.24,'(c)  Can learned edits adapt to a new task?',size=9,weight='bold')
 text(a,2.72,1.03,'Filtered ARC · Llama-3.2-1B · success (%) · scale 0–100',size=7.8,color=MUTED)
 # Compact paired summary: all four Table 1 results, oracle explicitly distinct.
 y=.64; bx=[3.02,4.08,5.14,6.30]
 for x,mid in zip(bx,S['arc_order']):
  v=R[mid+'_arc']['value'];color=CORAL if mid=='seal' else GRAY
  text(a,x,.76,f'{v:g}',size=12,ha='center',weight='bold',color=color)
  line(a,[(x-.34,.55),(x+.34,.55)],HAIR,3)
  if v:line(a,[(x-.34,.55),(x-.34+.68*v/100,.55)],color,3)
  a.plot(x-.34+.68*v/100,.55,'D' if mid=='seal' else 'o',markersize=3,color=color)
  text(a,x,.35,{'icl':'ICL','selfedit':'Self-edit, no RL','seal':'SEAL','oracle':'Oracle TTT'}[mid],size=7.7,ha='center',weight='bold' if mid=='seal' else 'normal')
 text(a,2.72,.12,'8 curated evaluation tasks; 5 edits/task. Tables 1–2; uncertainty unreported.',size=7.1,color=MUTED)
 export(f,'seal-teaser')

def method_figure():
 f,a=canvas(5.35)
 text(a,.18,5.12,'SEAL',size=15,weight='bold',color=CORAL)
 text(a,.91,5.12,'Train the editor through the results of adaptation',size=11.7,weight='bold')
 text(a,.18,4.84,'(a)  Training: candidate edits are judged after updating the model',size=9.5,weight='bold')
 # Spatial separation of control, candidate adaptation and evaluation.
 box(a,2.42,2.24,2.20,2.20,PURPLEL,'#D7CEE9',rounding=.10,z=0)
 box(a,4.79,2.24,1.90,2.20,BLUEL,'#C7DDE7',rounding=.10,z=0)
 text(a,.22,4.56,'1  Generate',size=9.3,weight='bold',color=AMBER)
 text(a,2.56,4.56,'2  Adapt each copy',size=9.3,weight='bold',color=PURPLE)
 text(a,4.94,4.56,'3  Test & reward',size=9.3,weight='bold',color=BLUE)
 document(a,.20,3.52,1.03,.63,'CONTEXT C',['Passage or','examples'],BLUEL,BLUE,size=8)
 chip(a,.32,2.75,.79,.51,r'$\theta_t$')
 arrow(a,(.71,3.46),(.71,3.31),BLUE)
 text(a,.72,2.52,'Current policy',size=8.0,ha='center')
 ys=[3.96,3.34,2.72]
 for i,y in enumerate(ys,1):
  # Each branch is a candidate, not a sequential update to the preceding copy.
  arrow(a,(1.15,3.00),(1.48,y),AMBER,rad=.12 if i==1 else -.12 if i==3 else 0)
  document(a,1.49,y-.25,.71,.50,f'EDIT {i}',[],size=7.9)
  for j,ww in enumerate([.43,.33]):line(a,[(1.61,y-.03-.075*j),(1.61+ww,y-.03-.075*j)],'#C49455',.7,z=5)
  arrow(a,(2.24,y),(2.54,y),PURPLE)
  box(a,2.57,y-.21,.73,.42,'white',PURPLE,rounding=.055)
  text(a,2.935,y,'Apply edit\n+ SFT',size=7.7,ha='center',color=PURPLE,linespacing=1.05)
  arrow(a,(3.35,y),(3.57,y),PURPLE)
  chip(a,3.64,y-.23,.67,.46,rf"$\theta'_{{t,{i}}}$",small=True)
  arrow(a,(4.36,y),(4.91,y),BLUE)
  box(a,4.97,y-.19,.91,.38,'white','#91B6C9',rounding=.045)
  text(a,5.425,y,'Task score',size=8.4,ha='center',color=BLUE)
  arrow(a,(5.91,y),(6.17,y),BLUE)
  status(a,6.34,y,ok=i<3,r=.11)
 text(a,3.51,2.36,'Inner loop: gradient-based adaptation',size=7.3,ha='center',color=PURPLE)
 text(a,5.73,2.36,'Rewards shown schematically',size=7.4,ha='center',color=BLUE)
 # A shared held-out task is explicit; adapted models do not evaluate themselves.
 text(a,5.72,4.28,r'Held-out task $\tau$',size=8.0,ha='center',color=BLUE)
 text(a,3.50,4.28,'All copies start from the same '+r'$\theta_t$',size=7.8,ha='center',color=PURPLE)
 # Outer loop has its own direction, color and verb phrase.
 route(a,[(6.50,3.96),(6.83,3.96),(6.83,1.98),(6.74,1.98)],TEAL,1.15)
 for y in ys[1:]:line(a,[(6.50,y),(6.83,y)],TEAL,.7)
 box(a,2.13,1.73,3.36,.50,TEALL,'#A5CDBD',rounding=.065)
 document(a,5.73,1.73,1.00,.50,'RL RECORD',[r'$C,\mathrm{edit}_i,r_i$'],TEALL,TEAL,size=8.0)
 arrow(a,(5.69,1.98),(5.53,1.98),TEAL,1.15)
 text(a,2.27,2.06,'4  Reinforce useful edits',size=9.0,weight='bold',color=TEAL)
 text(a,2.27,1.86,'SFT on selected context–edit pairs',size=7.9,color=TEAL)
 route(a,[(2.08,1.98),(.13,1.98),(.13,3.00),(.26,3.00)],TEAL,1.15)
 text(a,.32,2.17,r'Next policy $\theta_{t+1}$',size=8.5,color=TEAL)
 # Two data representations, not decorative icons, explain what an edit contains.
 line(a,[(.18,1.51),(6.83,1.51)],HAIR,.65)
 text(a,.18,1.32,'(b)  What is a self-edit? Two domain-specific representations',size=9.3,weight='bold')
 document(a,.22,.34,2.78,.75,'KNOWLEDGE → TRAINING TEXT',['Passage: “Planet Lyra orbits two suns.”','Edit: “Lyra is a planet. It has two suns.”'],size=8.1)

 box(a,3.25,.33,3.46,.77,AMBERL,AMBER,rounding=.04)
 text(a,3.38,.93,'FEW-SHOT TASK → TRAINING CONFIG',size=8.2,weight='bold',color=AMBER)
 grid(a,3.40,.44,[[1,0,0],[1,1,0],[0,0,0]],cell=.10)
 arrow(a,(3.76,.58),(3.95,.58),BLUE)
 grid(a,4.01,.44,[[0,1,1],[0,1,0],[0,0,0]],cell=.10)
 line(a,[(4.48,.44),(4.48,.82)],'#D6B37E',.6)
 text(a,3.40,.80,'Augmentation',size=7.4,color=AMBER)
 text(a,4.61,.77,'Controls training:',size=7.5,color=AMBER)
 text(a,4.61,.60,'augment: rotations, flips',size=8.1)
 text(a,4.61,.43,'choose: learning rate, epochs',size=8.1)
 text(a,3.5,.16,'Illustrative passage and grids; schematic rewards. The source paper defines domain-specific selection.',size=7.6,ha='center',color=MUTED)
 export(f,'seal-method')


def composition_alternatives():
 f,a=canvas(3.45)
 text(a,.18,3.22,'Composition alternatives · SEAL redesign',size=12,weight='bold')
 text(a,.18,2.91,'A  Selected: evidence beside concept',size=9,weight='bold',color=TEAL)
 text(a,3.70,2.91,'B  Rejected: wide ribbon above charts',size=9,weight='bold',color=MUTED)
 box(a,.20,1.49,1.01,1.15,AMBERL,AMBER)
 text(a,.70,2.06,'Concrete\nexample\n+ update',size=9,ha='center')
 box(a,1.36,1.86,1.94,.78,BLUEL,BLUE)
 text(a,2.33,2.25,'All methods ×\nall passage settings',size=9,ha='center')
 box(a,1.36,1.49,1.94,.24,CORALL,CORAL)
 text(a,2.33,1.61,'ARC comparison',size=8,ha='center')
 box(a,3.70,2.17,3.05,.47,AMBERL,AMBER)
 text(a,5.225,2.41,'Passage → writer → update → recall',size=8.5,ha='center')
 for x in [3.70,4.76,5.82]:
  box(a,x,1.49,.93,.53,BLUEL,BLUE)
  text(a,x+.465,1.75,'One regime',size=8,ha='center')
 text(a,.20,1.21,'Shared labels keep every comparison readable.',size=8.3,color=TEAL)
 text(a,3.70,1.21,'Repeated legends consume the evidence area.',size=8.3,color=MUTED)
 line(a,[(.18,.99),(6.80,.99)],HAIR,.6)
 text(a,.20,.78,'Method A: parallel candidate lanes + data insets',size=8.8,weight='bold',color=TEAL)
 text(a,3.70,.78,'Method B: a circular four-stage process',size=8.8,weight='bold',color=MUTED)
 text(a,.20,.43,'Chosen to preserve independent weight copies\nand reveal the actual generated objects.',size=8.3,linespacing=1.35)
 text(a,3.70,.43,'Rejected because it hides candidate identity\nand can imply sequential model updates.',size=8.3,linespacing=1.35)
 for ext in ['svg','png']:f.savefig(OUT/('composition-alternatives.'+ext),dpi=180)
 plt.close(f)

if __name__=='__main__':
 teaser_figure();method_figure();composition_alternatives();print('Wrote original SEAL teaser and method; current evidence validated.')
