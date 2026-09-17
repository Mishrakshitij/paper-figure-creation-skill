#!/usr/bin/env python3
"""Hybrid MAE method figure. Raster source example + editable vector semantics.

python examples/mae-hybrid/build_figure.py [--image PATH] [--output-dir PATH]
The image is only a synthetic teaching input. No model is run; output slots are
symbolic, never a generated or copied reconstruction. Crop identity is exact.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Polygon
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
W,H=7,4.15
INK='#193B43'; MUTED='#5A7178'; TEAL='#127F80'; TEAL_PALE='#E7F3EF'
BLUE='#32759C'; BLUE_PALE='#E9F2F7'; MASK='#B67943'; MASK_PALE='#F5ECD9'; GRID='#B6C8CA'
VISIBLE=(2,6,11,15); PACKED=(11,2,15,6)


def label(ax,x,y,text,size=8.5,color=INK,weight='normal',ha='left',va='center',**kw):
 return ax.text(x,y,text,fontsize=size,color=color,weight=weight,ha=ha,va=va,family='DejaVu Sans',**kw)

def box(ax,x,y,w,h,fc='white',ec=GRID,lw=.65,r=.02,z=2,**kw):
 p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',facecolor=fc,edgecolor=ec,linewidth=lw,zorder=z,**kw) if r else Rectangle((x,y),w,h,facecolor=fc,edgecolor=ec,linewidth=lw,zorder=z,**kw)
 ax.add_patch(p);return p

def arrow(ax,start,end,color=MUTED,connectionstyle='arc3',lw=1.05,**kw):
 p=FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=8,linewidth=lw,color=color,connectionstyle=connectionstyle,zorder=6,**kw);ax.add_patch(p);return p

def cell_xy(k,x,y,s):
 row,col=divmod(k-1,4);return x+col*s/4,y+(3-row)*s/4

def tiny_id(ax,x,y,k,color=TEAL):
 box(ax,x+.014,y+.016,.13,.115,fc='white',ec='none',r=.015,z=9)
 label(ax,x+.079,y+.073,str(k),size=7.3,color=color,weight='bold',ha='center',zorder=10)

def photo_grid(ax,arr,x,y,s,mode='source'):
 # The same array backs every image-based mark, including original targets.
 ax.imshow(arr,extent=(x,x+s,y,y+s),zorder=3,interpolation='nearest',aspect='auto')
 for k in range(1,17):
  px,py=cell_xy(k,x,y,s);cell=s/4
  if (mode=='masked' and k not in VISIBLE) or (mode=='targets' and k in VISIBLE):
   box(ax,px,py,cell,cell,fc=MASK_PALE if mode=='masked' else '#F7FAFA',ec='none',r=0,z=4)
   if mode=='masked':
    ax.plot([px+.055,px+cell-.055],[py+.055,py+cell-.055],color='#C6B696',lw=.75,zorder=5)
  box(ax,px,py,cell,cell,fc='none',ec='white',lw=.75,r=0,z=6)
  if mode!='targets' and k in VISIBLE:
   box(ax,px+.008,py+.008,cell-.016,cell-.016,fc='none',ec=TEAL,lw=1,r=0,z=8);tiny_id(ax,px,py,k)
  elif mode=='targets' and k not in VISIBLE:
   box(ax,px+.007,py+.007,cell-.014,cell-.014,fc='none',ec=MASK,lw=.75,r=0,z=8)
 box(ax,x,y,s,s,fc='none',ec=GRID,lw=.75,r=0,z=8)

def crop(arr,k):
 row,col=divmod(k-1,4);n=arr.shape[0]//4
 return arr[row*n:(row+1)*n,col*n:(col+1)*n,:]

def crop_tile(ax,arr,x,y,s,k):
 box(ax,x+.035,y-.027,s,s,fc='#DCE7E6',ec='none',r=0,z=1)
 ax.imshow(crop(arr,k),extent=(x,x+s,y,y+s),interpolation='nearest',aspect='auto',zorder=3)
 box(ax,x,y,s,s,fc='none',ec=TEAL,lw=.85,r=0,z=4)
 label(ax,x+s+.065,y+s/2,str(k),size=8,color=TEAL,weight='bold',zorder=8)

def latent(ax,x,y,s,k,masked):
 c=MASK if masked else BLUE;p=MASK_PALE if masked else BLUE_PALE
 box(ax,x+.014,y-.012,s,s,fc='#DFE6E7',ec='none',r=.018,z=2)
 box(ax,x,y,s,s,fc=p,ec=c,lw=.7,r=.018,z=3)
 if masked:ax.plot([x+.035,x+s-.035],[y+.035,y+s-.035],color='#C9A778',lw=.6,zorder=4)
 label(ax,x+s/2,y+s/2,str(k),size=7.8,color=c,weight='bold',ha='center',zorder=5,bbox=dict(facecolor=p,edgecolor='none',pad=.05))

def stack(ax,x,y,w,h,n,color,pale,title):
 for i in reversed(range(n)):
  box(ax,x+i*.05,y+i*.045,w,h,fc=pale,ec=color,lw=.8,r=.025,z=2+n-i)
 for j in range(3):box(ax,x+.085,y+.16+j*(h-.28)/3,w-.17,(h-.28)/3-.055,fc='white',ec=color,lw=.55,r=.013,z=10)
 label(ax,x+w/2+.03,y+h+.23,title,size=9.3,color=color,weight='bold',ha='center',zorder=12)

def draw(image_path,out):
 matplotlib.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42,'font.size':8.5})
 source=Image.open(image_path).convert('RGB')
 if source.width!=source.height or source.width%4:raise ValueError('Input must be square with width divisible by four; do not silently change crop identities.')
 arr=np.array(source)
 fig=plt.figure(figsize=(W,H),facecolor='white');ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(0,H));ax.axis('off')
 label(ax,.18,3.96,'MAE',size=12,weight='bold')
 label(ax,.75,3.96,'Learn from what is missing',size=11.3)
 for x,w,t in [(.18,1.64,'1  Mask the image'),(2.08,1.36,'2  Encode'),(3.75,3.07,'3  Restore and predict')]:
  label(ax,x,3.57,t,size=9.3,weight='bold');ax.plot([x,x+w],[3.42]*2,color='#D5E1E2',lw=.8)

 # A concrete image remains recognisable, with stable row-major patch IDs.
 photo_grid(ax,arr,.18,2.24,1.05,'source')
 label(ax,1.36,3.10,'Original',size=8.5)
 label(ax,1.36,2.93,'image',size=8.5)
 label(ax,1.36,2.63,'16 patches',size=8.5,color=MUTED)
 arrow(ax,(1.17,2.21),(1.40,2.00),color=MASK)
 label(ax,.73,2.11,'75% at random',size=8.5,color=MASK,ha='center')
 photo_grid(ax,arr,.70,.86,1.10,'masked')
 label(ax,1.25,.65,'4 visible · 12 hidden',size=8.5,ha='center')

 # Visible patch crops are literal excerpts; ID order is visibly shuffled.
 for i,k in enumerate(PACKED):crop_tile(ax,arr,2.10,1.12+(3-i)*.255,.205,k)
 arrow(ax,(1.83,1.63),(2.07,1.63),color=TEAL)
 arrow(ax,(2.49,1.63),(2.65,1.63),color=TEAL)
 label(ax,2.25,2.35,'Pack visible',size=8.5,ha='center',color=TEAL)
 label(ax,2.25,2.17,'patches',size=8.5,ha='center',color=TEAL)
 label(ax,2.29,.98,'4 tokens',size=8.5,ha='center')
 label(ax,2.29,.81,'+ pos.',size=8.5,ha='center',color=MUTED)
 stack(ax,2.68,1.13,.56,1.03,3,TEAL,TEAL_PALE,'Encoder')
 label(ax,2.99,.98,'visible only',size=8.5,ha='center',color=TEAL)

 # The focal operation is semantic, not a generic architecture box.
 arrow(ax,(3.45,1.67),(3.73,1.67),color=BLUE)
 for k in range(1,17):
  row,col=divmod(k-1,4);latent(ax,3.80+col*.253,1.16+(3-row)*.253,.228,k,k not in VISIBLE)
 label(ax,4.295,2.36,'Original positions',size=8.7,weight='bold',ha='center')
 label(ax,4.295,1.00,'4 latents + 12 masks',size=8.5,ha='center')
 box(ax,3.82,2.76,.24,.24,fc=MASK_PALE,ec=MASK,r=.015,z=3)
 label(ax,3.94,2.88,'M',size=9.0,weight='bold',color=MASK,ha='center',zorder=4)
 label(ax,4.295,3.16,'Shared mask token',size=8.5,color=MASK,ha='center')
 label(ax,4.17,2.88,'× 12 copies',size=8.5,color=MASK)
 arrow(ax,(4.30,2.73),(4.30,2.52),color=MASK,lw=.9)
 label(ax,5.21,2.89,'Unshuffle, then add',size=8.5,color=MUTED)
 label(ax,5.21,2.71,'decoder positions.',size=8.5,color=MUTED)

 arrow(ax,(4.86,1.68),(5.06,1.68),color=BLUE)
 stack(ax,5.10,1.39,.46,.55,2,MASK,MASK_PALE,'Decoder')
 label(ax,5.36,1.23,'lightweight',size=8.5,ha='center',color=MASK)
 arrow(ax,(5.66,1.68),(5.89,1.68),color=MASK)
 # Symbolic prediction slots avoid fabricating a successful reconstruction.
 for k in range(1,17):
  px,py=cell_xy(k,5.96,1.25,.84)
  masked=k not in VISIBLE
  box(ax,px+.008,py+.008,.194,.194,fc='#FBFAF7',ec=MASK if masked else '#CBD5D7',lw=.7 if masked else .5,r=.012,z=3)
  for j in range(2):ax.plot([px+.045,px+.163],[py+.072+j*.064]*2,color='#D6BA94' if masked else '#CBD5D7',lw=.7,zorder=4)
  if masked:ax.add_patch(Polygon([(px+.020,py+.192),(px+.068,py+.192),(px+.020,py+.144)],closed=True,facecolor=INK,edgecolor='none',zorder=5))
 label(ax,6.38,2.32,'Pixel predictions',size=8.7,weight='bold',ha='center')
 label(ax,6.38,2.15,'16 symbolic slots',size=8.5,color=MUTED,ha='center')
 label(ax,6.38,1.10,'12 masked slots',size=8.5,color=MASK,ha='center')
 arrow(ax,(6.39,.98),(6.39,.75),color=MASK)

 # Original targets are a separate training-only branch, with visible cells excluded.
 photo_grid(ax,arr,4.33,.10,.62,'targets')
 label(ax,4.64,.86,'Original targets',size=8.5,ha='center')
 arrow(ax,(5.00,.41),(5.96,.41),color=MASK)
 box(ax,5.99,.18,.82,.54,fc=MASK_PALE,ec=MASK,r=.045,z=3)
 label(ax,6.40,.51,'MSE',size=9.3,weight='bold',color=MASK,ha='center',zorder=4)
 label(ax,6.40,.31,'masked only',size=8.5,color=MASK,ha='center',zorder=4)
 label(ax,.18,.39,'One synthetic image; no model run.',size=8.5,color=MUTED)
 label(ax,.18,.20,'Projection layers and CLS token omitted.',size=8.5,color=MUTED)

 fig.canvas.draw();renderer=fig.canvas.get_renderer();bounds=fig.bbox
 clipped=[]
 for t in fig.findobj(matplotlib.text.Text):
  if not t.get_visible() or not t.get_text():continue
  b=t.get_window_extent(renderer)
  if b.x0<bounds.x0-.5 or b.y0<bounds.y0-.5 or b.x1>bounds.x1+.5 or b.y1>bounds.y1+.5:clipped.append(t.get_text())
 if clipped:raise RuntimeError(f'Text outside canvas: {clipped}')
 for ext in ('png','svg','pdf'):fig.savefig(out/f'figure.{ext}',dpi=220,facecolor='white')
 plt.close(fig)
 # Verify exact crops, count and source provenance rather than image plausibility.
 check={'figure_width_in':W,'figure_height_in':H,'text_outside_canvas':clipped,'source_asset':image_path.name,'source_sha256':hashlib.sha256(image_path.read_bytes()).hexdigest(),'source_dimensions_px':list(source.size),'visible_patch_ids':VISIBLE,'packed_patch_ids':PACKED,'masked_patch_ids':[k for k in range(1,17) if k not in VISIBLE],'visible_count':4,'mask_count':12,'encoder_input_count':4,'decoder_position_count':16,'loss_position_count':12,'predictions':'symbolic slots; no pixel reconstruction or numerical experiment','raster_content':'input image and its exact crops only; all text, arrows, frames and model geometry are vector','crop_identity_check':all(np.array_equal(crop(arr,k),arr[((k-1)//4)*arr.shape[0]//4:(((k-1)//4)+1)*arr.shape[0]//4,((k-1)%4)*arr.shape[1]//4:(((k-1)%4)+1)*arr.shape[1]//4,:]) for k in PACKED)}
 (out/'geometry-check.json').write_text(json.dumps(check,indent=2)+'\n')


def proofs(out):
 import fitz
 src=fitz.open(out/'figure.pdf');p=src[0]
 p.get_pixmap(matrix=fitz.Matrix(110/72,110/72)).save(out/'print-proof.png')
 p.get_pixmap(matrix=fitz.Matrix(110/72,110/72),colorspace=fitz.csGRAY).save(out/'grayscale-proof.png')
 src.close()


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--image',type=Path,default=ROOT/'assets/fox-input.jpg');p.add_argument('--output-dir',type=Path,default=ROOT)
 a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
 draw(a.image,a.output_dir);proofs(a.output_dir);print(a.output_dir/'figure.png')

if __name__=='__main__':main()
