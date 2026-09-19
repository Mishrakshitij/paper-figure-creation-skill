#!/usr/bin/env python3
"""Rebuild the SEAL hybrid demonstration from source-linked specifications."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'skills/paper-figure-creation/scripts'))
from render_graphs import render_graphs
from compose_svg import compose

INK = '#17232B'
MUTED = '#52626D'
TEAL = '#007D8A'
ORANGE = '#A96932'


def write_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def sketches():
    # Deliberately low-detail alternatives: select topology before decoration.
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="504pt" height="148pt" viewBox="0 0 504 148"><rect width="504" height="148" fill="white"/>']
    def box(x,y,w,h,txt,c='#F1F4F5'):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{c}" stroke="#AAB6BD" stroke-width=".6"/>')
        if txt:s.append(f'<text x="{x+w/2}" y="{y+h/2+3}" font-family="DejaVu Sans" font-size="8" text-anchor="middle" fill="{INK}">{escape(txt)}</text>')
    for x,title in [(5,'A · Explanation beside evidence'),(174,'B · Ribbon above evidence'),(343,'C · Results around a loop')]:
        s.append(f'<text x="{x}" y="13" font-family="DejaVu Sans" font-size="8" font-weight="bold">{escape(title)}</text>')
    box(5,23,49,104,'Concept','#E7F3F2')
    for i in range(3):box(59+i*33,23,29,104,'Plot')
    box(174,23,157,34,'Passage → edit → adapt → ask','#E7F3F2')
    for i in range(3):box(174+i*53,64,49,63,'Plot')
    box(344,23,153,25,'Plot')
    box(344,54,38,73,'Plot');box(459,54,38,73,'Plot');box(389,64,63,44,'Adapt ↻','#E7F3F2')
    s.append('<text x="5" y="143" font-family="DejaVu Sans" font-size="8" fill="#007D8A">Selected A: one reading order, shared method rows, equal quantitative scales.</text></svg>')
    (HERE/'layout-sketches.svg').write_text(''.join(s))
    subprocess.run(['inkscape',str(HERE/'layout-sketches.svg'),'--export-type=png','--export-dpi=150','--export-filename='+str(HERE/'layout-sketches.png')],check=True,capture_output=True)


def graph_spec(width=318, height=220, standalone=False):
    original = json.loads((ROOT/'examples/seal/teaser.spec.json').read_text())
    source = json.loads((ROOT/'examples/seal/reported-tables.json').read_text())
    spec = {k:copy.deepcopy(original[k]) for k in ('version','status','provenance','evidence')}
    spec['kind'] = 'graphs'
    spec['provenance']['retrieved_utc'] = '2026-09-19'
    spec['provenance']['example_status'] = 'Exact Table 2 values; no constructed quantitative evidence.'
    spec['provenance']['sources'] = [s for s in spec['provenance']['sources'] if s['id']=='knowledge']
    spec['evidence']['metrics'] = [m for m in spec['evidence']['metrics'] if m['id']!='arc']
    spec['evidence']['results'] = [r for r in spec['evidence']['results'] if r['metric_id']!='arc']
    spec['evidence']['claims'] = []
    order = ['base','passage','synthetic','gpt41','seal']
    values = {row[0]:row[2] for row in source['table2']}
    for result in spec['evidence']['results']:
        col = ['single','cpt200','cpt2067'].index(result['metric_id'])
        assert result['value'] == values[result['method_id']][col]
    spec['figure'] = {'width_in':width/72,'height_in':height/72,'font_pt':8,'dpi':150}
    spec['layout'] = {'rows':1,'cols':3}
    if standalone:
        spec['figure'].update(title='SEAL: knowledge incorporation across adaptation regimes',
                             subtitle='Qwen2.5-7B · SQuAD questions answered without the passage · Table 2',
                             note='Reported means; no entry-specific uncertainty. Tuned hyperparameters; not compute matched.')
        start,panelw,gap,bottom,ph = 108,111,19,42,143
    else:
        start,panelw,gap,bottom,ph = 89,62,12,30,151
    labels = ['Base model','Passage only','Passage +\nself-generated','Passage +\nGPT-4.1 data','SEAL']
    ft = 'Full fine-tuning' if standalone else 'Full FT'
    titles = [('single','1 passage\nLoRA'),('cpt200','200 passages\n'+ft),('cpt2067','2,067 passages\n'+ft)]
    colors = ['#74818A','#74818A','#74818A',ORANGE,TEAL]
    markers = ['o','s','^','D','*']
    spec['charts'] = []
    for i,(metric,title) in enumerate(titles):
        spec['charts'].append({'type':'dot','metric_id':metric,'title':title,'panel_label':'',
            'categories':labels if i==0 else ['']*5,'xlim':[25,70],'xticks':[30,45,60],
            'xlabel':'Accuracy (%)' if standalone else '', 'value_labels':True,'value_format':'.1f',
            'rect':[(start+i*(panelw+gap))/width,bottom/height,panelw/width,ph/height],
            'series':[{'id':'methods','label':'Methods','values':[values[m][i] for m in order],
                       'result_ids':[m+'_'+metric for m in order], 'point_colors':colors,
                       'point_markers':markers,'point_label_offsets':[[3,3]]*5}]})
    return spec


def manifest():
    overlays=[]
    def text(x,y,s,size=8,fill=INK,bold=False,anchor='start'):
        overlays.append({'type':'text','x':x,'y':y,'text':s,'font_size_pt':size,
                         'font_weight':'bold' if bold else 'normal','fill':fill,'anchor':anchor})
    def rect(x,y,w,h,fill,stroke='none',radius=0):
        overlays.append({'type':'rect','x':x,'y':y,'width':w,'height':h,'fill':fill,'stroke':stroke,'radius_pt':radius,'stroke_width_pt':.7})
    def arrow(points,color=TEAL):
        overlays.append({'type':'arrow','points':points,'stroke':color,'stroke_width_pt':1.1})
    def line(x,y,x2,y2,color='#D7E0E4'):
        overlays.append({'type':'path','d':f'M {x} {y} L {x2} {y2}','fill':'none','stroke':color,'stroke_width_pt':.7})
    text(12,19,'SEAL learns how to write its own training data',13,bold=True)
    text(12,34,'Knowledge incorporation · Qwen2.5-7B · SQuAD without passage context',8,fill=MUTED)
    line(177,48,177,313)
    text(12,56,'a   Rewrite, adapt, then answer',9,bold=True)
    text(190,56,'b   All methods, all three settings',9,bold=True)
    text(190,70,'Mean no-context accuracy (%) ↑',8,fill=MUTED)
    text(25,91,'PASSAGE',8,bold=True,fill=MUTED)
    text(103,91,'SELF-EDIT',8,bold=True,fill=TEAL)
    # All content on the notebook remains editable, generated image is blank.
    for y,s in [(112,'In 1987,'),(124,'Lyra opened'),(136,'its archive.')]:text(25,y,s,8)
    for y,s in [(112,'The archive’s'),(124,'opening year'),(136,'was 1987.')]:text(103,y,s,8,fill=TEAL)
    arrow([[78,154],[97,154]])
    text(88,172,'Generated by LMθ',8,anchor='middle')
    text(88,188,'Constructed example',8,fill=MUTED,anchor='middle')
    arrow([[88,195],[88,209]])
    rect(19,214,141,50,'#E9F4F3',radius=4)
    text(30,226,'Fine-tune on passage',8,bold=True,fill=TEAL)
    text(30,237,'+ self-edit',8,bold=True,fill=TEAL)
    # A symbolic parameter array: abstract structural illustration, not weights.
    for x,col in [(34,'#A3B0B6'),(109,TEAL)]:
        for r in range(2):
            for c in range(3):rect(x+c*5,243+r*5,3.5,3.5,col)
    text(59,252,'θ',11);arrow([[75,248],[95,248]]);text(134,252,'θ′',11)
    arrow([[88,266],[88,275]])
    text(88,286,'Ask without the passage',9,bold=True,anchor='middle')
    text(88,300,'“When did the archive open?”',8,anchor='middle')
    text(12,317,'Rewrite policy learned with RL.',8,fill=MUTED)
    # Evidence interpretation keeps SEAL's weaker CPT results visible.
    text(190,302,'SEAL leads for one passage;',8,bold=True,fill=TEAL)
    text(190,315,'GPT-4.1 data leads in both CPT settings.',8,bold=True,fill=ORANGE)
    text(12,333,'Table 2, arXiv:2506.10943v2 · No uncertainty reported; tuned hyperparameters, not compute matched.',8,fill=MUTED)
    return {'version':1,'canvas':{'width_pt':504,'height_pt':342},
            'assets':[
                {'id':'notebook','path':'assets/passage-notebook.jpg','kind':'raster','box_pt':[14,60,154,154],'fit':'contain',
                 'provenance':{'source':'Built-in image generation, 2026-09-19','role':'illustration','license_status':'Generated for this project; no external source artwork. Model identity not exposed.'}},
                {'id':'results','path':'results-panel.svg','kind':'vector','box_pt':[182,76,318,220],'fit':'contain',
                 'provenance':{'source':'SEAL Table 2, https://arxiv.org/html/2506.10943v2','role':'reported quantitative evidence','license_status':'Data replot; original vector design.'}}
            ],'overlays':overlays}


def proofs():
    from PIL import Image
    for stem in ['seal-teaser','seal-graphs']:
        subprocess.run(['pdftoppm','-png','-singlefile','-r','110',str(HERE/(stem+'.pdf')),str(HERE/(stem+'-pdf-proof'))],check=True,capture_output=True)
        subprocess.run(['pdftoppm','-png','-singlefile','-r','72',str(HERE/(stem+'.pdf')),str(HERE/(stem+'-print'))],check=True,capture_output=True)
        with Image.open(HERE/(stem+'-pdf-proof.png')) as im:
            im.convert('L').save(HERE/(stem+'-grayscale.png'))


def main():
    sketches()
    for stem,width,height,standalone in [('results-panel',318,220,False),('seal-graphs',504,250,True)]:
        spec_path=HERE/(stem+'.spec.json')
        spec=json.loads(spec_path.read_text()) if spec_path.exists() else graph_spec(width,height,standalone)
        if not spec_path.exists():write_json(stem+'.spec.json',spec)
        render_graphs(spec,HERE/stem,formats=('svg','pdf','png') if standalone else ('svg',))
    comp_path=HERE/'composition.json'
    comp=json.loads(comp_path.read_text()) if comp_path.exists() else manifest()
    if not comp_path.exists():write_json('composition.json',comp)
    report=compose(comp,HERE,HERE/'seal-teaser',formats=('svg','pdf','png'),dpi=150)
    proofs()
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
