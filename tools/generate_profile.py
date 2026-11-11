"""Generate an animated, diagram-led GitHub profile panel. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 1480

def find_font(*paths):
    for path in paths:
        if Path(path).is_file():
            return path
    raise FileNotFoundError('Install Segoe UI / Consolas or DejaVu fonts')

FONT_REG = find_font('C:/Windows/Fonts/segoeui.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
FONT_BOLD = find_font('C:/Windows/Fonts/segoeuib.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
FONT_MONO = find_font('C:/Windows/Fonts/consola.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')

def font(size, style='regular'):
    return ImageFont.truetype({'regular': FONT_REG, 'bold': FONT_BOLD, 'mono': FONT_MONO}[style], size)

def label(draw, pos, value, size, color, style='regular'):
    draw.text(pos, value, font=font(size, style), fill=color)

BG = (11, 20, 31)
SURFACE = (15, 29, 44)
PANEL = (18, 34, 50)
EDGE = (46, 68, 87)
WHITE = (225, 236, 244)
SUBTLE = (158, 179, 195)
FAINT = (104, 130, 150)
BLUE = (110, 183, 230)
BLUE_LINE = (65, 128, 166)

im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle((1, 1, W-2, H-2), outline=(48, 76, 96), width=2)
d.rectangle((2, 2, W-3, 65), fill=(16, 29, 42))
d.line((2,65,W-2,65), fill=EDGE, width=1)
for i,c in enumerate([(92,111,126),(92,111,126),(110,183,230)]):
    d.ellipse((31+i*19, 28, 40+i*19, 37), fill=c)
label(d,(105,20),'eren@infrastructure: ~',20,SUBTLE,'mono')
label(d,(977,22),'PROFILE / 01',16,FAINT,'mono')
# Header and introduction: no exaggerated titles or claimed metrics.
label(d,(58,103),'EREN KARAOĞLU',65,WHITE,'bold')
label(d,(62,197),'SYSTEMS   /   CLOUD   /   INFRASTRUCTURE',22,BLUE,'mono')
d.line((62,249,1138,249),fill=EDGE,width=1)
label(d,(62,280),'01   ABOUT',19,BLUE,'mono')
label(d,(62,326),'Information Systems Engineering graduate.',30,WHITE)
label(d,(62,373),'Curious about the systems behind the software.',27,SUBTLE)
d.line((62,438,1138,438),fill=EDGE,width=1)
label(d,(62,470),'02   AREAS OF INTEREST',19,BLUE,'mono')
label(d,(858,473),'CONNECTED FIELDS',16,FAINT,'mono')
# Connecting lines first, with small animated packets added later.
for y in (588, 789):
    d.line((569,y,631,y),fill=BLUE_LINE,width=2)
d.line((600,588,600,789),fill=BLUE_LINE,width=2)
for x,y in ((600,588),(600,789)):
    d.ellipse((x-4,y-4,x+4,y+4),fill=BLUE)

cards = [
    (62,  528, 'SYSTEMS',    'Linux / Windows Server', 'Active Directory', 'server'),
    (631, 528, 'CLOUD',      'Azure / virtualization', 'Hybrid identity', 'cloud'),
    (62,  729, 'NETWORKING', 'Routing / security', 'Monitoring', 'network'),
    (631, 729, 'AUTOMATION', 'PowerShell / Bash', 'Python', 'terminal'),
]

def icon(draw, x, y, kind):
    col=BLUE
    if kind == 'server':
        for i in range(3):
            yy=y+i*15
            draw.rectangle((x,yy,x+37,yy+10),outline=col,width=2)
            draw.ellipse((x+5,yy+3,x+8,yy+6),fill=col)
    elif kind == 'cloud':
        draw.arc((x+1,y+13,x+21,y+33),90,270,fill=col,width=2)
        draw.arc((x+10,y+2,x+36,y+28),180,315,fill=col,width=2)
        draw.arc((x+27,y+13,x+47,y+33),270,90,fill=col,width=2)
        draw.line((x+10,y+33,x+37,y+33),fill=col,width=2)
    elif kind == 'network':
        draw.line((x+7,y+12,x+31,y+12,x+31,y+34,x+7,y+34,x+7,y+12),fill=col,width=2)
        for xx,yy in [(x+7,y+12),(x+31,y+12),(x+31,y+34),(x+7,y+34)]:
            draw.rectangle((xx-3,yy-3,xx+3,yy+3),fill=BG,outline=col,width=2)
    else:
        draw.rectangle((x,y+3,x+42,y+38),outline=col,width=2)
        draw.line((x+8,y+13,x+15,y+20,x+8,y+27),fill=col,width=2)
        draw.line((x+21,y+28,x+32,y+28),fill=col,width=2)

for x,y,title,line1,line2,kind in cards:
    d.rectangle((x,y,x+506,y+151), fill=PANEL, outline=EDGE, width=1)
    icon(d,x+24,y+25,kind)
    label(d,(x+89,y+21),title,23,WHITE,'bold')
    label(d,(x+89,y+62),line1,21,SUBTLE)
    label(d,(x+89,y+94),line2,21,SUBTLE)

d.line((62,934,1138,934),fill=EDGE,width=1)
label(d,(62,965),'03   LEARNING PATH',19,BLUE,'mono')
# Labels indicate interests and learning, not completed qualifications.
d.line((72,1029,72,1225),fill=(54,88,109),width=2)
items=[(1023,'NOW','Windows Server, Linux and Active Directory'),
       (1097,'NEXT','Azure administration and hybrid identity'),
       (1171,'EXPLORING','Terraform, Ansible and Kubernetes')]
for y,small,detail in items:
    d.ellipse((67,y+10,77,y+20),fill=BLUE)
    label(d,(100,y+1),small,18,BLUE,'mono')
    label(d,(260,y-3),detail,25,WHITE)
d.line((62,1275,1138,1275),fill=EDGE,width=1)
label(d,(62,1313),'$ learn  /  build  /  troubleshoot  /  automate',23,SUBTLE,'mono')
d.rectangle((2,1408,W-3,H-3),fill=(16,29,42))
d.line((2,1408,W-2,1408),fill=EDGE,width=1)
d.ellipse((62,1437,72,1447),fill=BLUE)
label(d,(87,1427),'STATUS: CURIOUS',19,SUBTLE,'mono')
label(d,(911,1428),'ERENTECHLABS',17,FAINT,'mono')

frames=[]
for k in range(36):
    frame=im.copy(); d=ImageDraw.Draw(frame)
    # The dots follow the connecting lines; no simulated usage statistics.
    y=588+(201*k/35)
    d.ellipse((597,y-3,603,y+3),fill=(166,219,249))
    if k < 18:
        cursor_x = 62 + int(d.textlength('$ learn  /  build  /  troubleshoot  /  automate', font=font(23, 'mono'))) + 12
        d.rectangle((cursor_x,1318,cursor_x+11,1339),fill=BLUE)
    frames.append(frame)

output=ROOT/'profile-diagram-v9.gif'
frames[0].save(output,save_all=True,append_images=frames[1:],duration=85,loop=0,optimize=True,disposal=2)
print(f'Created {output.name} ({output.stat().st_size:,} bytes)')
