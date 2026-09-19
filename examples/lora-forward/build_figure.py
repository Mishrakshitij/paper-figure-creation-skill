#!/usr/bin/env python3
"""Canonical SVG geometry. Build with Python 3 + Inkscape + Poppler."""
from pathlib import Path
from html import escape
import subprocess
from PIL import Image, ImageOps

OUT = Path(__file__).resolve().parent
W,H = 1008,600
INK='#182C3A'; MUTED='#526371'; GREY='#EAF0F4'; G_STROKE='#607787'
ORANGE='#AE5415'; PALE='#FFF4E8'; AMBER='#FFE1BB'; TEAL='#24756C'
p=[]
def raw(s): p.append(s)
def text(x,y,s,size=18,fill=INK,weight='normal',anchor='start',italic=False):
    raw(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"'+(' font-style="italic"' if italic else '')+'>'+s+'</text>')
def rect(x,y,w,h,fill='white',stroke='none',sw=1.8,rx=0):
    raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(coords,color=INK,sw=2,arrow=False):
    raw('<path d="'+' '.join(('M' if i==0 else 'L')+f'{x},{y}' for i,(x,y) in enumerate(coords))+f'" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
def circle(x,y,r,fill='white',stroke=INK,sw=2):
    raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def sub(s): return f'<tspan baseline-shift="sub" font-size="70%">{s}</tspan>'
def sup(s): return f'<tspan baseline-shift="super" font-size="70%">{s}</tspan>'
def math_label(x,y,s,size=23,**kw): text(x,y,s,size=size,**kw)
def matrix(x,y,w,h,label,color,stroke):
    rect(x,y,w,h,color,stroke,2)
    # Thin margin marks identify a matrix without inventing entries or discrete cell counts.
    line([(x+8,y+8),(x+8,y+h-8)],stroke,1)
    line([(x+w-8,y+8),(x+w-8,y+h-8)],stroke,1)
    math_label(x+w/2,y+h/2+8,label,26,anchor='middle')

raw(f'<svg xmlns="http://www.w3.org/2000/svg" width="7in" height="{H/144}in" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
raw('<title id="title">LoRA: low-rank adaptation and merged deployment</title><desc id="desc">The same input x passes through frozen W zero and through trainable A then B, scaled by alpha over r. Their outputs are summed. After training the scaled update can be merged into a single deployment matrix.</desc>')
raw('<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="#182C3A"/></marker></defs>')
raw('<g font-family="DejaVu Sans, sans-serif">')
rect(0,0,W,H)
# Panel A: one shared input, two additive paths.
raw('<g id="adaptation">')
text(24,31,'a',22,weight='bold'); text(52,31,'Adaptation',21,weight='bold')
math_label(982,32,'h = W'+sub('0')+'x + (α/r)BAx',24,anchor='end')
text(328,69,'FROZEN',17,fill=MUTED,weight='bold',anchor='middle')
text(588,69,'Pretrained linear map',18,fill=MUTED)
rect(213,224,593,164,PALE,rx=12)
text(229,249,'LOW-RANK UPDATE',17,fill=ORANGE,weight='bold')
text(786,249,'A and B trainable',17,fill=ORANGE,anchor='end')
# Wiring drawn before scientific objects.
line([(81,210),(146,210)],arrow=True)
circle(146,210,3.5,INK,'none')
line([(146,210),(146,133),(248,133)],arrow=True)
line([(146,210),(146,292),(248,292)],arrow=True)
line([(408,133),(875,133),(875,190)],arrow=True)
line([(386,292),(445,292)],arrow=True)
line([(470,292),(552,292)],arrow=True)
line([(595,292),(713,292)],arrow=True)
line([(777,292),(875,292),(875,231)],arrow=True)
line([(895,210),(927,210)],arrow=True)
# Matrices and rank bottleneck.
matrix(253,89,150,88,'W'+sub('0'),GREY,G_STROKE)
math_label(328,201,'d × k',19,fill=MUTED,anchor='middle')
math_label(621,119,'W'+sub('0')+'x ∈ ℝ'+sup('d'),20,anchor='middle')
matrix(253,271,128,42,'A',AMBER,ORANGE)
math_label(317,342,'r × k',19,fill=ORANGE,anchor='middle')
text(317,368,'Gaussian init.',17,fill=ORANGE,anchor='middle')
rect(450,281,16,22,AMBER,ORANGE,1.8)
math_label(459,274,'Ax',19,anchor='middle')
math_label(459,337,'ℝ'+sup('r'),19,anchor='middle')
matrix(557,257,38,70,'B',AMBER,ORANGE)
math_label(576,350,'d × r',19,fill=ORANGE,anchor='middle')
text(576,374,'zero init.',17,fill=ORANGE,anchor='middle')
math_label(652,279,'BAx',19,anchor='middle')
rect(718,271,59,42,'white',ORANGE,1.8,5)
math_label(747.5,299,'α/r',21,anchor='middle')
text(747.5,338,'scale',17,fill=ORANGE,anchor='middle')
# Input, output, coordinate-wise addition.
math_label(56,212,'x',29,anchor='middle',italic=True)
math_label(56,241,'ℝ'+sup('k'),19,fill=MUTED,anchor='middle')
text(56,272,'input',17,fill=MUTED,anchor='middle')
circle(875,210,19)
text(875,219,'+',30,anchor='middle')
text(842,216,'sum',17,fill=MUTED,anchor='end')
math_label(951,212,'h',29,anchor='middle',italic=True)
math_label(951,241,'ℝ'+sup('d'),19,fill=MUTED,anchor='middle')
text(951,272,'output',17,fill=MUTED,anchor='middle')
text(229,414,'r ≪ min(d, k)',19,fill=ORANGE)
text(472,414,'At initialization: BA = 0, so h = W'+sub('0')+'x',18)
raw('</g>')
# Panel B is parameter construction followed by deployed data flow, not a training edge.
line([(24,438),(984,438)],'#CFD8DE',1.4)
raw('<g id="deployment">')
text(24,470,'b',22,weight='bold'); text(52,470,'Deployment',21,weight='bold')
text(238,470,'Merge once after training',18,fill=MUTED)
math_label(52,520,'W'+sub('merged')+' = W'+sub('0')+' + (α/r)BA',25)
math_label(52,556,'W'+sub('merged')+' ∈ ℝ'+sup('d × k'),19,fill=MUTED)
math_label(639,522,'x',26,anchor='middle',italic=True)
line([(657,513),(707,513)],arrow=True)
matrix(713,480,140,66,'W'+sub('merged'),GREY,G_STROKE)
line([(858,513),(913,513)],arrow=True)
math_label(937,522,'h',26,anchor='middle',italic=True)
text(783,575,'One linear map: h = W'+sub('merged')+'x',18,fill=MUTED,anchor='middle')
raw('</g></g></svg>')
svg=OUT/'figure.svg'; svg.write_text('\n'.join(p))
for filename,opts in [('figure.pdf',[]),('figure.png',['--export-dpi=300']),('figure-paper-size.png',['--export-dpi=144'])]:
    subprocess.run(['inkscape',str(svg),'--export-type='+filename.rsplit('.',1)[-1],'--export-filename='+str(OUT/filename),*opts],check=True,capture_output=True)
subprocess.run(['pdftoppm','-singlefile','-r','144','-png',str(OUT/'figure.pdf'),str(OUT/'figure-pdf-proof')],check=True,capture_output=True)
im=Image.open(OUT/'figure-paper-size.png').convert('RGB')
ImageOps.grayscale(im).save(OUT/'figure-grayscale.png')
im.resize((504,300)).save(OUT/'figure-thumbnail.png')
print('Built SVG, PDF, 300-dpi PNG and review proofs.')

# Three intentionally rough, topologically distinct composition sketches.
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1008" height="350" viewBox="0 0 1008 350"><rect width="1008" height="350" fill="white"/><g font-family="DejaVu Sans" fill="#182C3A">']
def st(x,y,t,size=14): s.append(f'<text x="{x}" y="{y}" font-size="{size}">{t}</text>')
def sb(x,y,w,h,t):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFF4E8" stroke="#526371"/>'); st(x+7,y+h/2+5,t)
def sp(d): s.append(f'<path d="{d}" fill="none" stroke="#526371" stroke-width="1.5"/>')
for x in [336,672]: sp(f'M{x},12 V332')
st(15,29,'1  Shared-input branches',17); st(15,51,'Chosen: data flow first')
st(17,150,'x'); sp('M30,145 H56 M56,145 V99 H91 M56,145 V210 H91')
sb(91,76,64,46,'W₀'); sp('M155,99 H296 V145')
sb(91,197,49,27,'A'); sp('M140,210 H168'); sb(168,184,26,52,'B'); sp('M194,210 H214');sb(214,197,50,27,'α/r');sp('M264,210 H296 V155');st(287,155,'+');sp('M306,149 H319');st(15,285,'Separate merge strip below');sb(15,301,295,27,'Wmerged = W₀ + (α/r)BA')
st(350,29,'2  Vertical residual fork',17);st(350,51,'Computation rises through two lanes')
st(494,310,'x');sp('M501,296 V271 M501,271 H408 V195 M501,271 H588 V238')
sb(379,145,58,50,'W₀');sb(560,213,55,25,'A');sp('M588,213 V184');sb(574,149,28,35,'B');sp('M588,149 V120');sb(561,93,54,27,'α/r');sp('M408,145 V79 H496 M588,93 V79 H507');st(496,84,'+');sp('M501,68 V60')
st(350,332,'Tall layout competes with deployment')
st(686,29,'3  Algebra-first factorization',17);st(686,51,'Parameter dimensions first')
sb(702,126,70,64,'W₀');st(785,164,'+');sb(814,126,27,64,'B');sb(858,145,100,25,'A');st(814,107,'scaled by α/r');st(705,216,'d × k');st(811,216,'d × r');st(882,216,'r × k')
st(695,276,'x');sp('M711,272 H743');sb(743,254,131,36,'Wmerged');sp('M874,272 H919');st(930,277,'h');st(686,332,'Shared-input path is less visible')
s.append('</g></svg>'); (OUT/'composition-sketches.svg').write_text('\n'.join(s))
