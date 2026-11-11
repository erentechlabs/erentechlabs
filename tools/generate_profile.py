"""Generate the profile GIF. Requires Pillow: python -m pip install Pillow."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random

W,H=1200,1710
OUT=Path(__file__).resolve().parent.parent
def pick_font(*paths):
 for path in paths:
  if Path(path).is_file(): return path
 raise FileNotFoundError('Install Consolas or DejaVu Sans Mono to generate the panel.')
MONO=pick_font('C:/Windows/Fonts/consola.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
BOLD=pick_font('C:/Windows/Fonts/consolab.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf')
SANS=MONO; SANSB=BOLD
def f(n,k='mono'): return ImageFont.truetype({'mono':MONO,'bold':BOLD,'sans':SANS,'sansb':SANSB}[k],n)
def text(d,p,s,n,c,k='mono'): d.text(p,s,font=f(n,k),fill=c)
random.seed(23)
# Graphite / phosphor green palette sampled by eye from the preview.
BG=(2,10,9); BRIGHT=(142,255,103); GREEN=(75,239,130); LIME=(185,255,67); WHITE=(226,244,229); MUTED=(144,190,163); LINE=(24,99,62)
base=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(base)
# Matrix-like texture is subdued for readable text.
for y in range(8,H,4): d.line((15,y,W-15,y),fill=(4,16,13))
for x in range(40,W,55): d.line((x,24,x,H-24),fill=(5,21,17))
for y in range(38,H,55): d.line((20,y,W-20,y),fill=(5,21,17))
# One continuous luminous chassis with square corners.
d.rectangle((14,14,1186,1696),outline=(26,105,60),width=6)
d.rectangle((16,16,1184,1694),outline=(114,255,127),width=2)
text(d,(57,43),'eren@systems:~/README$',27,GREEN,'bold')
text(d,(1004,49),'PROFILE.SYS',16,(58,156,95),'bold')
d.line((57,91,1142,91),fill=(20,103,63),width=2)
text(d,(57,112),'>',70,LIME,'bold')
text(d,(120,112),'EREN KARAOĞLU',70,WHITE,'bold')
text(d,(123,197),'SYSTEMS  /  CLOUD  /  INFRASTRUCTURE',26,(179,227,195),'bold')
d.rectangle((122,239,229,242),fill=LIME)
# Holographic network: arced meridians, projected latitude bands and stars.
cx,cy,rx,ry=620,593,510,295
orb=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(orb)
# Dome outline and latitude curves as data arc, not a fabricated metric.
for start in [180,190,202]: od.arc((cx-rx,cy-ry,cx+rx,cy+ry),start,360,fill=(21,113,74,170),width=2)
for lat in [.17,.32,.48,.64,.79]:
 y=cy-ry*lat; span=rx*math.sqrt(max(0,1-lat*lat))
 pts=[]
 for i in range(121):
  x=-span+2*span*i/120
  pts.append((cx+x,y+39*(x/span)**2))
 od.line(pts,fill=(17,92,63,135),width=1)
for lon in [-.82,-.56,-.28,0,.28,.56,.82]:
 pts=[]
 for i in range(91):
  u=i/90; y=cy-ry*u
  x=cx+lon*rx*math.sqrt(max(0,1-u*u))
  pts.append((x,y))
 od.line(pts,fill=(19,107,70,130),width=1)
# Dense tiny illuminated dots are decorative, not geography or telemetry.
for i in range(1800):
 x=random.uniform(-1,1); y=random.uniform(0,1)
 if x*x+y*y<1 and random.random()<.55:
  px=cx+x*rx; py=cy-y*ry
  a=random.randint(55,145); od.point((int(px),int(py)),fill=(34,226,128,a))
base=Image.alpha_composite(base.convert('RGBA'),orb).convert('RGB'); d=ImageDraw.Draw(base)
# Stationary curves of the constellation.
beziers=[((120,559),(385,322),(562,468),(1032,344)),((190,594),(430,386),(621,570),(1106,455)),((339,530),(580,272),(772,500),(1053,492))]
def curve(p,q,r,s,steps=90):
 return [((1-u)**3*p[0]+3*(1-u)**2*u*q[0]+3*(1-u)*u*u*r[0]+u**3*s[0], (1-u)**3*p[1]+3*(1-u)**2*u*q[1]+3*(1-u)*u*u*r[1]+u**3*s[1]) for u in (i/steps for i in range(steps+1))]
paths=[curve(*b) for b in beziers]
for p in paths: d.line(p,fill=(27,159,90),width=2)
# Graphical command section ribbon, continuous interior, no separate panel.
def ribbon(y,label):
 d.line((55,y,55,y+43,280,y+43,300,y+22,280,y,55,y),fill=GREEN,width=2)
 text(d,(70,y+4),'> '+label,25,LIME,'bold')
 d.line((301,y+22,1140,y+22),fill=(27,126,75),width=2)
ribbon(631,'WHOAMI')
text(d,(76,692),'eren@systems:~$',24,GREEN,'bold'); text(d,(320,692),'whoami',24,WHITE,'bold')
text(d,(76,735),'name',23,GREEN,'bold'); text(d,(245,735),':  Eren Karaoğlu',23,WHITE)
text(d,(76,771),'focus',23,GREEN,'bold'); text(d,(245,771),':  Systems, cloud, networking, automation',23,WHITE)
text(d,(76,807),'about',23,GREEN,'bold'); text(d,(245,807),':  Information Systems Engineering graduate',23,WHITE)
text(d,(284,843),'Curious about the systems behind software.',23,MUTED)
ribbon(915,'STACK')
# Six bold labels with consistent baseline, larger than an icon grid on small screens.
stack=[('01','LINUX'),('02','WINDOWS'),('03','AZURE'),('04','POWERSHELL'),('05','NETWORKING'),('06','AUTOMATION')]
for i,(number,label) in enumerate(stack):
 x=76+(i%3)*350; y=985+(i//3)*78
 d.line((x,y,x,y+53),fill=(43,168,85),width=2)
 text(d,(x+12,y+3),number,17,(61,168,102),'bold')
 text(d,(x+50,y-2),label,25,WHITE,'bold')
 text(d,(x+50,y+30),['SYSTEMS','SERVER','CLOUD','SCRIPTING','SECURITY','BASH / PYTHON'][i],15,(107,177,132),'bold')
ribbon(1168,'LEARNING')
text(d,(76,1230),'NOW',20,GREEN,'bold')
text(d,(255,1225),'Windows Server  /  Linux  /  Active Directory',23,WHITE)
text(d,(76,1277),'NEXT',20,GREEN,'bold')
text(d,(255,1272),'Azure administration  /  Hybrid identity',23,WHITE)
text(d,(76,1324),'EXPLORING',20,GREEN,'bold')
text(d,(255,1319),'Terraform  /  Ansible  /  Kubernetes',23,WHITE)
d.line((57,1407,1141,1407),fill=(22,113,64),width=2)
text(d,(76,1442),'$ ./keep-building',25,GREEN,'bold')
text(d,(76,1487),'LEARN  >  BUILD  >  TROUBLESHOOT  >  AUTOMATE',24,WHITE,'bold')
text(d,(76,1546),'// understand the system. automate the routine.',20,(113,185,139),'mono')
d.line((57,1614,1141,1614),fill=(25,127,69),width=2)
text(d,(58,1640),'eren@systems:~$',23,GREEN,'bold')
d.line([(314,1635),(557,1635),(571,1654),(557,1673),(314,1673),(300,1654),(314,1635)],fill=LIME,width=2)
text(d,(324,1639),'STATUS: CURIOUS',21,LIME,'bold')
# Small decorative node labels integrated into the globe.
for label,x,y in [('NET',286,359),('SYS',510,527),('CLOUD',913,312),('INFRA',927,489)]:
 text(d,(x,y),'[ '+label+' ]',17,(152,244,183),'bold')

frames=[]
# Animated packets and cursor use glow layers; the underlying design stays steady.
for k in range(36):
 img=base.copy().convert('RGBA'); glow=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
 pts=[]
 for j,path in enumerate(paths):
  for offset in [0,.44]:
   index=int(((k/36+offset+j*.18)%1)*(len(path)-1)); x,y=path[index]; pts.append((x,y))
   gd.ellipse((x-10,y-10,x+10,y+10),fill=(58,255,130,170))
 img=Image.alpha_composite(img,glow.filter(ImageFilter.GaussianBlur(9))); ad=ImageDraw.Draw(img)
 for x,y in pts: ad.ellipse((x-4,y-4,x+4,y+4),fill=(192,255,160,255))
 if k<18: ad.rectangle((585,1641,597,1663),fill=(190,255,72,255))
 frames.append(img.convert('RGB'))
frames[0].save(OUT/'profile-terminal-v6.gif',save_all=True,append_images=frames[1:],duration=85,loop=0,optimize=True,disposal=2)
print('Generated bytes:',(OUT/'profile-terminal-v6.gif').stat().st_size)
