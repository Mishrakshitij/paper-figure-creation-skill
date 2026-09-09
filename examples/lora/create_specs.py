import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
URL = 'https://arxiv.org/pdf/2106.09685v2'
rows = [
    ('ft', 'Full FT', 175255.8, 73.8, 89.5, 52.0, 28.0, 44.5),
    ('bitfit', 'BitFit', 14.2, 71.3, 91.0, 51.3, 27.4, 43.5),
    ('preembed', 'PreEmbed', 3.2, 63.1, 88.6, 48.3, 24.2, 40.5),
    ('prelayer', 'PreLayer', 20.2, 70.1, 89.5, 50.8, 27.3, 43.5),
    ('adapter7', 'AdapterH', 7.1, 71.9, 89.8, 53.0, 28.9, 44.8),
    ('adapter40', 'AdapterH', 40.1, 73.2, 91.5, 53.2, 29.0, 45.1),
    ('lora4', 'LoRA', 4.7, 73.4, 91.7, 53.8, 29.8, 45.9),
    ('lora37', 'LoRA', 37.7, 74.0, 91.6, 53.4, 29.2, 45.1),
]
metrics = [
    {'id':'params', 'label':'Trainable parameters', 'unit':'million parameters', 'direction':'lower'},
    {'id':'wiki', 'label':'WikiSQL logical-form accuracy', 'unit':'percent', 'direction':'higher'},
    {'id':'mnli', 'label':'MNLI-matched accuracy', 'unit':'percent', 'direction':'higher'},
    {'id':'r1', 'label':'SAMSum ROUGE-1', 'unit':'ROUGE points', 'direction':'higher'},
    {'id':'r2', 'label':'SAMSum ROUGE-2', 'unit':'ROUGE points', 'direction':'higher'},
    {'id':'rl', 'label':'SAMSum ROUGE-L', 'unit':'ROUGE points', 'direction':'higher'},
]
sources = [
    {'id':'method', 'kind':'paper', 'locator':URL, 'location':'Section 4.1, printed page 4, Equation 3 and subsequent scaling/initialization/merge paragraphs; Section 4.2, printed page 5'},
    {'id':'protocol', 'kind':'paper', 'locator':URL, 'location':'Section D.4, printed pages 19-20; Table 12, printed page 21; Section 5.5 and Table 4 caption, printed page 8'},
]
results = []
source_rows = []
for mid, label, *values in rows:
    source_rows.append({'id':mid,'method':label,'params_millions':values[0], 'WikiSQL':values[1], 'MNLI_m':values[2], 'SAMSum_R1':values[3], 'SAMSum_R2':values[4], 'SAMSum_RL':values[5]})
    sources.append({'id':'row_'+mid, 'kind':'paper', 'locator':URL,
        'location':f'Table 4, printed page 8 (PDF page index 7), GPT-3 ({label}) row with {values[0]:,.1f}M trainable parameters'})
    for i, metric in enumerate(metrics):
        dataset = 'WikiSQL' if metric['id']=='wiki' else 'MNLI-matched' if metric['id']=='mnli' else 'SAMSum' if metric['id'] in ('r1','r2','rl') else 'GPT-3 Table 4 adaptation'
        split = 'validation' if metric['id'] in ('wiki','mnli') else 'as reported in Table 4; split not explicit in table caption' if metric['id'] in ('r1','r2','rl') else 'training parameter count; not an evaluation split'
        results.append({'id':f'{mid}_{metric["id"]}','method_id':mid,'metric_id':metric['id'],'source_id':'row_'+mid,
            'value':values[i], 'source_column':metric['label'],
            'comparison':{'dataset':dataset,'split':split,'budget':'2 epochs; batch size 128; AdamW; common pretrained GPT-3 175B',
                'protocol':'Original paper Table 4. Learning rate tuned by method/dataset; best validation performance selected per run. Hardware NVIDIA Tesla V100. No equal-time or equal-parameter claim.'},
            'uncertainty':None})

claims = [
    {'id':'wiki_delta','type':'percentage_point_difference','proposed_result_id':'lora4_wiki','baseline_result_id':'ft_wiki','decimals':1,'display_value':-0.4},
    {'id':'mnli_delta','type':'percentage_point_difference','proposed_result_id':'lora4_mnli','baseline_result_id':'ft_mnli','decimals':1,'display_value':2.2},
]
spec = {'version':1,'kind':'teaser','status':'draft',
    'figure':{'width_in':7,'height_in':4.1,'concept_fraction':0.33,
        'title':'LoRA: adapt a frozen model with low-rank updates',
        'geometry_source':'build_figures.py','note':'Original reported data; schematic task example. Two-column draft; venue unspecified.'},
    'provenance':{'data_status':'reported','sources':sources,
        'retrieved_utc':'2026-09-09','paper_version':'arXiv:2106.09685v2, 16 Oct 2021',
        'extraction':'Web tool parsed original PDF text. Direct PDF download returned HTTP403. No digitization of plots.',
        'inclusion':'Every Table 4 method/parameter setting; WikiSQL and MNLI-m columns plotted. Full SAMSum data preserved here.',
        'task_uncertainty':{'WikiSQL_typical_sd_pp':0.5,'MNLI_m_typical_sd_pp':0.1,'SAMSum_typical_sd_points':[0.2,0.2,0.1],
            'source_id':'protocol','interpretation':'Task-level typical standard deviations over random seeds, not entry-specific estimates. No chart error bars.'}},
    'evidence':{'metrics':metrics,'results':results,'claims':claims},
    'charts':[],'row_order':[r[0] for r in rows], 'method_labels':{r[0]:r[1] for r in rows},
    'layout':{'concept_region_inches':[0.18,0.85,2.14,2.68], 'evidence_region_inches':[2.52,0.85,4.3,2.68],
        'font_pt':8.5,'axis_limits':{'wiki':[62,77.5],'mnli':[88.1,92.7]},'baseline_marker':'o','proposed_marker':'D'},
    'method_contract':{'h':'W0 x + (alpha/r) B(Ax)','dimensions':{'W0':'d x k','A':'r x k','B':'d x r','x':'k','h':'d'},
        'frozen':['W0'],'trainable':['A','B'],'initialization':{'A':'random Gaussian','B':'zero'},'inference':'Wmerged = W0 + (alpha/r) BA'}}
for metric in ['wiki','mnli']:
    spec['charts'].append({'type':'dot','title':metrics[1 if metric=='wiki' else 2]['label'], 'metric_id':metric,
        'categories':[r[1] for r in rows], 'xlabel':'Accuracy (%) ↑',
        'series':[{'id':metric,'label':'Table 4 methods','values':[r[3 if metric=='wiki' else 4] for r in rows],
            'result_ids':[r[0]+'_'+metric for r in rows], 'point_roles':['proposed' if r[0].startswith('lora') else 'baseline' for r in rows]}]})
(OUT/'teaser.spec.json').write_text(json.dumps(spec,indent=2)+'\n')
(OUT/'table4.json').write_text(json.dumps({'source':URL,'table':'4','rows':source_rows},indent=2)+'\n')
method = {k:spec[k] for k in ('version','status','provenance','method_contract')}
method.update({'kind':'method','figure':{'width_in':7,'height_in':4.6,'title':'LoRA computation: train a low-rank branch, then merge','geometry_source':'build_figures.py'},
    'evidence':{'metrics':[],'results':[],'claims':[]},'canonical_geometry':'build_figures.py:method_figure'})
(OUT/'method.spec.json').write_text(json.dumps(method,indent=2)+'\n')
print('Wrote two specs and exact Table 4 data.')
