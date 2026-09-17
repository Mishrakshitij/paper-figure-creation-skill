from pathlib import Path
from html import escape
out=Path(__file__).parent
p=['<svg xmlns="http://www.w3.org/2000/svg" width="1008" height="670" viewBox="0 0 1008 670"><rect width="1008" height="670" fill="white"/><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 8 4 0 8" fill="none" stroke="#65717a"/></marker></defs><g font-family="DejaVu Sans" fill="#25323c">']
def t(x,y,s,size=15):p.append(f'<text x="{x}" y="{y}" font-size="{size}">{escape(s)}</text>')
def b(x,y,w,h,label,fill='#f5f6f6'):
 p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="#65717a"/>');t(x+10,y+25,label)
def a(d):p.append(f'<path d="{d}" fill="none" stroke="#65717a" stroke-width="1.5" marker-end="url(#a)"/>')
t(24,28,'Three composition sketches · Reasoning Gym setup',20)
t(24,62,'1  Split generated-entry sheet — selected',17)
b(24,76,360,34,'leg_counting · size 10 · seed 42');a('M180 110 V130');b(24,132,360,86,'Question: 1 sea slug + 1 deer','#eef7f5');t(36,188,'[large animal vignette]');b(24,218,360,42,'answer 4 · metadata','#fbf2e4');a('M384 172 H476');b(480,149,135,46,'Model');a('M615 172 H700');b(704,149,180,46,'Candidate 4');a('M794 195 V218');b(704,222,250,42,'Task-specific verifier','#fbf2e4');a('M384 242 H700');t(446,232,'complete entry')
t(24,305,'2  Horizontal assembly line',17)
for x,w,s in [(24,180,'Configuration'),(268,220,'Entry: slug + deer'),(554,130,'Model'),(752,222,'Verifier / score')]:b(x,328,w,67,s)
a('M204 358 H264');a('M488 358 H550');a('M684 358 H748');a('M376 395 V430 H865 V399');t(511,451,'reference bypass')
t(24,492,'3  Access lanes',17)
b(24,512,184,105,'Generated entry');b(258,512,716,48,'Model-visible: question → model → candidate','#eef7f5');b(258,584,716,48,'Evaluator: complete entry + candidate → verifier','#fbf2e4');a('M208 540 H254');a('M208 600 H254');a('M858 560 V580')
p.append('</g></svg>');(out/'composition-sketches.svg').write_text('\n'.join(p))
