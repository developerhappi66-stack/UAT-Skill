#!/usr/bin/env python3
"""Approved A2 portrait UAT layout; see references/layout-schema.md."""
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import math,json
import argparse
parser=argparse.ArgumentParser(description='Render complete UI screenshots as red-arrow UAT flows.')
parser.add_argument('manifest',type=Path)
parser.add_argument('output',type=Path)
args=parser.parse_args()
D=args.manifest.resolve().parent
cfg=json.loads(args.manifest.read_text())
OUT=args.output.resolve();OUT.parent.mkdir(parents=True,exist_ok=True)
regular=cfg.get('font_regular','/System/Library/Fonts/Supplemental/Arial.ttf')
bold=cfg.get('font_bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf')
for name,file in [('Arial',regular),('ArialB',bold)]:
 pdfmetrics.registerFont(TTFont(name,str((D/Path(file)).resolve())))
W,H=1190.55,1683.78
C=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
C.setTitle(cfg['title']);C.setAuthor(cfg.get('brand',''))
C.setSubject(cfg['evidence_note'])
pages=cfg['pages']
flow_ids=[p['flow'] for p in pages]
for flow in set(flow_ids):
 positions=[i for i,f in enumerate(flow_ids) if f==flow]
 assert len(positions)<=2, f'{flow}: a flow may occupy at most two pages'
 assert positions==list(range(positions[0],positions[-1]+1)), f'{flow}: pages must be consecutive'
images={key:(D/Path(value)).resolve() for key,value in cfg['screens'].items()}
RED=HexColor('#DA292E');INK=HexColor('#202D3C');GRAY=HexColor('#607080');GOLD=HexColor('#FDB813');PALE=HexColor('#FFF8E8')
placements=[];page_no=0

def txt(x,y,s,size=12,font='Arial',color=INK):
 C.setFont(font,size);C.setFillColor(color);C.drawString(x,H-y,s)
def wrap(s,width,size=12,font='Arial'):
 lines=[]
 for para in s.split('\n'):
  line=''
  for word in para.split():
   n=(line+' '+word).strip()
   if pdfmetrics.stringWidth(n,font,size)>width and line:lines.append(line);line=word
   else:line=n
  lines.append(line)
 return lines

def block(x,y,s,width,size=12,font='Arial',color=INK,leading=None):
 ls=wrap(s,width,size,font);leading=leading or size*1.35
 for i,line in enumerate(ls):txt(x,y+i*leading,line,size,font,color)
 return y+len(ls)*leading

def arrow(points,label='',label_pos=None,dashed=False):
 C.saveState();C.setStrokeColor(RED);C.setFillColor(RED);C.setLineWidth(2.7);C.setLineJoin(1)
 if dashed:C.setDash(5,4)
 p=C.beginPath();p.moveTo(points[0][0],H-points[0][1])
 for x,y in points[1:]:p.lineTo(x,H-y)
 C.drawPath(p);C.setDash()
 a,b=points[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);l=10;wid=4.5
 tri=C.beginPath();tri.moveTo(b[0],H-b[1]);
 for k in [-1,1]:
  x=b[0]-l*math.cos(ang)+k*wid*math.sin(ang);y=b[1]-l*math.sin(ang)-k*wid*math.cos(ang);tri.lineTo(x,H-y)
 tri.close();C.drawPath(tri,fill=1,stroke=0);C.restoreState()
 if label and label_pos:
  x,y=label_pos;lines=wrap(label,160,10.5,'ArialB');ww=max(pdfmetrics.stringWidth(z,'ArialB',10.5) for z in lines)+12
  C.setFillColor(white);C.rect(x-6,H-y-(len(lines)-1)*13-5,ww,len(lines)*13+3,fill=1,stroke=0)
  for i,z in enumerate(lines):txt(x,y+i*13,z,10.5,'ArialB',RED)

def header(flow,title,subtitle,part='1 / 1'):
 global page_no;page_no+=1
 C.bookmarkPage(f'page{page_no}');C.addOutlineEntry(f'{page_no:02d}  {title}  ({part})',f'page{page_no}',level=0)
 C.setFillColor(GOLD);C.rect(0,H-12,W,12,fill=1,stroke=0)
 txt(42,43,cfg['brand'],13,'ArialB');txt(W-330,43,cfg['review_label'],11,'Arial',GRAY)
 txt(42,83,f'{flow}   {title}',25,'ArialB');txt(W-132,81,part,15,'ArialB',RED)
 block(42,110,subtitle,W-84,11.5,color=GRAY)
 C.setStrokeColor(HexColor('#DCE1E5'));C.line(42,H-133,W-42,H-133)

def footer(note='',next_page=None,next_step=None):
 y=H-94
 C.setFillColor(PALE);C.roundRect(42,H-y-39,W-84,39,7,fill=1,stroke=0)
 block(54,y+15,note or 'Review the complete displayed content, labels, available actions and state-specific messages.',W-110,10.5,color=INK)
 txt(42,H-39,cfg['evidence_note'],10,'Arial',GRAY)
 txt(42,H-22,'Full-page captures preserve all scroll content. Pop-up views are accompanied by the full underlying page.',9.5,'Arial',GRAY)
 txt(W-120,H-25,f'{page_no:02d} / {len(pages)}',11,'ArialB')
 if next_page:
  y=H-118;arrow([(W-400,y),(W-355,y)])
  txt(W-345,y+4,f'CONTINUE: PAGE {next_page} / STEP {next_step}',12,'ArialB',RED)
 C.showPage()

def size(id):
 with Image.open(images[id]) as im:return im.size

def node(id,x,y,w,num,title,action=''):
 # y is the top of the label; every source pixel is fitted without clipping.
 sh=size(id);ih=w*sh[1]/sh[0];fh=ih+25
 txt(x,y+11,str(num).zfill(2),12,'ArialB',RED)
 ty=block(x+25,y+11,title,w-25,11.5,'ArialB',INK,13)
 if action:block(x,y+41,action,w,10,color=RED,leading=12)
 top=y+72
 C.setFillColor(HexColor('#E9EDF0'));C.roundRect(x+2,H-top-fh-4,w+10,fh,10,fill=1,stroke=0)
 C.setFillColor(HexColor('#171C22'));C.roundRect(x-4,H-top-fh,w+8,fh,10,fill=1,stroke=0)
 C.setFillColor(HexColor('#707780'));C.roundRect(x+w/2-15,H-top-8,30,2.5,1.25,fill=1,stroke=0)
 C.drawImage(ImageReader(str(images[id])),x,H-top-13-ih,width=w,height=ih,mask='auto')
 C.setFillColor(HexColor('#8C9299'));C.roundRect(x+w/2-20,H-top-fh+5,40,2.5,1,fill=1,stroke=0)
 placements.append(dict(page=page_no,id=id,x=x,y=top,w=w,h=fh,source=list(sh)))
 return dict(x=x,y=top,w=w,h=fh,bottom=top+fh)

def seq(rows,maxw=230,top=160,bottom=H-153):
 # Rows snake left-to-right, then right-to-left; constant capture width per page.
 counts=[len(row) for row in rows]
 ratios=[max(size(n[0])[1]/size(n[0])[0] for n in row) for row in rows]
 fixed=len(rows)*97+(len(rows)-1)*57
 w=min(maxw,(W-130-(max(counts)-1)*42)/max(counts),(bottom-top-fixed)/sum(ratios))
 allnodes=[];y=top;prevlast=None
 for ri,row in enumerate(rows):
  n=len(row);gap=(W-110-n*w)/(n-1) if n>1 else 0;xs=[55+i*(w+gap) for i in range(n)]
  if ri%2:xs.reverse()
  nodes=[node(item[0],x,y,w,*item[1:]) for x,item in zip(xs,row)]
  for a,b in zip(nodes,nodes[1:]):
   yy=y+145
   if b['x']>a['x']:arrow([(a['x']+w+7,yy),(b['x']-9,yy)])
   else:arrow([(a['x']-8,yy),(b['x']+w+9,yy)])
  if prevlast:
   a=prevlast;b=nodes[0];outside=W-26 if ri%2 else 26
   ay=a['y']+135;by=b['y']+135
   sx=a['x']+w+7 if ri%2 else a['x']-7;ex=b['x']+w+9 if ri%2 else b['x']-9
   arrow([(sx,ay),(outside,ay),(outside,by),(ex,by)])
   txt(outside-60 if ri%2 else outside+7,y-22,'NEXT',10,'ArialB',RED)
  prevlast=nodes[-1];allnodes+=nodes;y=max(z['bottom'] for z in nodes)+57
 return allnodes

for i,page in enumerate(pages):
 flow=page['flow'];total=flow_ids.count(flow);part=flow_ids[:i+1].count(flow)
 header(flow,page['title'],page['subtitle'],f'{part} / {total}')
 if 'rows' in page:
  seq(page['rows'],maxw=page.get('max_width',230))
 else:
  for item in page['nodes']:node(**item)
  for item in page['arrows']:arrow(**item)
  for item in page.get('text_blocks',[]):block(**item)
 if part<total:
  assert page.get('next_step') is not None, 'Continuation requires next_step'
 footer(page.get('note',''),i+2 if part<total else None,page.get('next_step'))
C.save()
for a in placements:
 assert a['w']>0 and a['x']>=0 and a['x']+a['w']<=W, a
 assert a['y']+a['h']<H-105, ('Screen overlaps footer',a)
 assert abs((a['h']-25)/a['w']-a['source'][1]/a['source'][0])<1e-6
OUT.with_suffix('.layout.json').write_text(json.dumps({'pages':page_no,'pageSize':[W,H],'placements':placements},indent=2))
print(f'{OUT}: {page_no} pages, {len(placements)} screenshot placements')
