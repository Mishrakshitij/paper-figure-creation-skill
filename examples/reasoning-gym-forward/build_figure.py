#!/usr/bin/env python3
"""Build original, fully editable SVG; render directly with Inkscape at 300 dpi."""
from pathlib import Path
from html import escape
import subprocess
OUT=Path(__file__).parent
W,H=1008,594
p=[]
ink='#243239'; muted='#4f6267'; teal='#176c67'; pale='#eff8f6'; gold='#846019'; sand='#fcf5e8'; edge='#a6b5b8'
def add(s):p.append(s)
def text(x,y,s,size=18,weight='normal',fill=ink,anchor='start',family='DejaVu Sans'):
 add(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')
def rect(x,y,w,h,fill='white',stroke='none',r=0,sw=1.5):
 add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def path(d,fill='none',stroke=ink,sw=2,extra=''):
 add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def arrow(d,color=ink):path(d,stroke=color,sw=2.3,extra='marker-end="url(#arrow)"')
def line(x1,y1,x2,y2,color=edge,sw=1.5,extra=''):
 add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" {extra}/>')
def ellipse(cx,cy,rx,ry,fill,stroke='none',sw=1.5):
 add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="7in" height="{H/144}in" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
add('<title id="title">Reasoning Gym benchmark setup</title><desc id="desc">Procedural leg-counting generation with size 10 and seed 42 produces an entry containing a question about one sea slug and one deer. The model receives only question text and produces an illustrative answer 4. A task-specific verifier receives the answer and the complete entry including reference answer and metadata. A reference answer check is documented to score 1.0. No aggregate model performance is shown.</desc>')
add('<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L8 4 L0 8 Z" fill="#243239"/></marker></defs>')
rect(0,0,W,H)
text(24,31,'Reasoning Gym: generate a question, verify an answer',23,'bold')
text(24,75,'a',21,'bold'); text(48,75,'Construct one example',20,'bold')
text(548,75,'b',21,'bold'); text(572,75,'Answer and verify',20,'bold')
# A compact generation strip; no pictorial stack implies an unsupported count.
add('<g id="procedural-construction">')
rect(24,97,450,83,'#f4f6f6',edge,7)
text(42,123,'leg_counting',20,'bold',teal)
text(42,155,'10 entries  ·  seed 42',18)
line(245,114,245,162,'#c1ccce')
text(254,123,'Procedural generator',17,'bold')
text(264,153,'Configurable complexity',16,fill=muted)
arrow('M249 180 V205')
add('</g>')
text(548,140,'Static question–answer interface',18,fill=muted)
# Main generated entry; all fields remain one identifiable object.
add('<g id="generated-entry">')
path('M24 214 H449 L474 239 V526 H24 Z',fill='white',stroke=teal,sw=2)
path('M449 214 V239 H474',stroke=teal,sw=1.5)
text(42,240,'QUESTION  ·  first generated entry',16,'bold',teal)
text(42,274,'How many legs in total for',20,'bold')
text(42,301,'1 sea slug and 1 deer?',20,'bold')
rect(40,315,418,117,pale,r=7)
# Original illustrative sea slug, shown without invented legs.
add('<g id="illustration-sea-slug" transform="translate(75 334)">')
ellipse(65,43,65,4,'#d2e6e1')
path('M5 39 C15 38 20 24 30 26 C36 13 45 26 51 18 C61 8 66 20 75 17 C88 11 100 21 104 26 C119 29 133 31 133 38 C116 44 84 45 56 44 C35 46 16 44 5 39 Z',fill='#419387',stroke='#176c67',sw=1.6)
path('M14 37 C33 35 43 38 55 34 C68 30 82 34 96 30 C109 32 118 32 126 36',stroke='#bce1d8',sw=2)
path('M34 28 C30 18 28 12 27 7 M44 23 C42 13 43 8 47 4',stroke='#176c67',sw=3)
ellipse(25.9,6,2.8,4.5,'#176c67');ellipse(47,4,2.8,4.5,'#176c67')
for x,y in [(58,24),(69,29),(81,23),(94,28),(49,32)]:ellipse(x,y,2,1.5,'#a9d5c9')
add('</g>')
text(142,402,'1 sea slug',17,anchor='middle')
text(249,369,'+',27,fill=muted,anchor='middle')
# Original side-view deer. Four separate legs preserve the relevant count.
add('<g id="illustration-deer" transform="translate(306 330) scale(.6)">')
ellipse(57,90,72,4,'#dce8e0')
# far legs
path('M33 51 L29 84 L25 89 H32 L39 57 M79 49 L84 81 L81 89 H89 L88 51',fill='#bc8b50',stroke='#805723',sw=2)
# torso and neck
path('M6 39 C9 19 34 18 56 23 C68 23 76 12 80 1 L94 4 L87 35 C95 45 88 58 75 60 L27 58 C11 57 3 52 6 39 Z',fill='#d8ae70',stroke='#805723',sw=2)
# tail
path('M9 32 L-3 22 L-5 33 L8 42',fill='#eed7ad',stroke='#805723',sw=2)
# near legs, each terminates in a dark hoof
path('M19 50 L18 86 L13 90 H22 L28 54 M64 54 L67 84 L63 90 H72 L72 51',fill='#d8ae70',stroke='#805723',sw=2)
path('M13 90 H22 M25 89 H32 M63 90 H72 M81 89 H89',stroke='#56432b',sw=3)
# head, muzzle, ear and visible antler branches
path('M79 3 C77 -8 83 -14 94 -12 L109 -6 L120 -4 L120 3 L103 9 L93 12 L86 9',fill='#d8ae70',stroke='#805723',sw=2)
path('M89 -11 L77 -24 L93 -20 L99 -12',fill='#d8ae70',stroke='#805723',sw=2)
path('M87 -12 L85 -33 L78 -41 M85 -32 L93 -40 M85 -24 L74 -30',stroke='#805723',sw=2.4)
ellipse(105,-3,2.1,2.1,'#243239');ellipse(120,-2,2,3,'#56432b')
path('M82 21 C81 30 82 36 85 40',stroke='#f2dfbd',sw=4)
add('</g>')
text(348,402,'1 deer',17,anchor='middle')
text(249,423,'Illustration only; the model receives text.',16,fill=muted,anchor='middle')
# Reference/metadata band: this is not model input.
rect(25,445,448,80,sand)
line(25,445,473,445,gold,1.5,'stroke-dasharray="6 5"')
text(42,472,'answer: 4',19,'bold',gold)
text(224,472,'metadata: …',18,fill=gold)
text(42,509,'These fields are not sent to the model.',16,fill=muted)
add('</g>')
# Upper model path originates beside the question text.
add('<g id="model-visible-route">')
text(513,255,'question',16,fill=teal,anchor='middle')
arrow('M474 280 H547')
rect(555,247,160,67,'#f1f4f5','#6b7f88',8,1.7)
text(635,274,'Tested',20,'bold',anchor='middle');text(635,299,'model',20,'bold',anchor='middle')
arrow('M715 280 H799')
# Candidate answer slip, conventional source not measured model outcome.
rect(807,227,177,113,'white','#647a83',7,1.7)
text(895.5,252,'Candidate',17,'bold',anchor='middle')
text(895.5,293,'4',36,'bold',teal,anchor='middle')
text(895.5,322,'illustrative',16,fill=muted,anchor='middle')
arrow('M895 340 V416')
text(880,380,'candidate answer',16,fill=muted,anchor='end')
add('</g>')
# The full entry and candidate meet at the evaluator, with no feedback arrow.
add('<g id="evaluation-route">')
text(593,444,'complete entry',17,'bold',anchor='middle')
text(593,468,'question, answer, metadata',16,fill=muted,anchor='middle')
arrow('M474 492 H711')
rect(719,425,265,115,sand,gold,8,1.8)
text(851.5,450,'Task-specific verifier',19,'bold',gold,anchor='middle')
text(740,488,'score',18,fill=muted)
text(808,491,'1.0',29,'bold',gold)
text(740,520,'documented for reference 4',16,fill=muted)
add('</g>')
text(24,570,'Illustrative candidate; no model run. Scoring rules vary by task.',17,fill=muted)
add('</svg>')
svg=OUT/'reasoning-gym-setup.svg';svg.write_text('\n'.join(p))
subprocess.run(['inkscape',str(svg),'--export-type=png',f'--export-filename={OUT / "reasoning-gym-setup.png"}','--export-dpi=300'],check=True)
subprocess.run(['inkscape',str(svg),'--export-type=png',f'--export-filename={OUT / "paper-width-proof.png"}','--export-dpi=96'],check=True)
# Inspection views are derived directly from the vector render.
from PIL import Image,ImageOps
im=Image.open(OUT/'reasoning-gym-setup.png').convert('RGB')
ImageOps.grayscale(im).save(OUT/'grayscale-proof.png')
im.thumbnail((420,420));im.save(OUT/'thumbnail-proof.png')
