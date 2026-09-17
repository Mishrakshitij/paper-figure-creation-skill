#!/usr/bin/env python3
"""Composition sketches created before detailed hybrid figure rendering."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
OUT = Path(__file__).resolve().parent
fig, axes = plt.subplots(3,1,figsize=(7,5.4),facecolor='white')
layouts = [
 ('A  Staggered example + expanded restoration (selected)',[(.01,.36,.20,.42,'source / mask'),(.25,.38,.08,.37,'visible'),(.36,.35,.13,.42,'encoder'),(.57,.38,.16,.36,'restore IDs'),(.78,.43,.08,.25,'decode'),(.90,.43,.09,.26,'predict'),(.01,.05,.48,.15,'shared mask token + identity legend'),(.59,.04,.40,.17,'masked targets → loss')]),
 ('B  Straight six-stage strip',[(.01,.37,.16,.35,'source'),(.21,.37,.16,.35,'mask'),(.42,.36,.12,.37,'encode'),(.59,.37,.13,.35,'restore'),(.77,.42,.08,.25,'decode'),(.90,.37,.09,.35,'predict'),(.25,.04,.74,.17,'target branch + masked-only scoring')]),
 ('C  Central image with split encoding and scoring lanes',[(.01,.30,.25,.51,'large source'),(.33,.56,.22,.23,'visible → encoder'),(.60,.56,.20,.23,'restore → decoder'),(.85,.56,.14,.23,'predict'),(.34,.17,.22,.22,'hidden targets'),(.69,.17,.30,.22,'masked-only scoring')])
]
for ax,(title,boxes) in zip(axes,layouts):
 ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');ax.text(.01,.98,title,va='top',fontsize=9,weight='bold',color='#173C43')
 for x,y,w,h,txt in boxes:
  ax.add_patch(Rectangle((x,y),w,h,facecolor='#E8F2EF' if 'restore' in txt or 'source' in txt else '#F5EFE4',edgecolor='#9BAFB4',lw=.7))
  ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=7.3,color='#234049',wrap=True)
fig.tight_layout(h_pad=1)
fig.savefig(OUT/'storyboards.png',dpi=130)
fig.savefig(OUT/'storyboards.svg')
plt.close(fig)
