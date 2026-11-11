"""Generate the animated terminal profile. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parent.parent
W, H = 1000, 1240

def pick(*paths):
    for path in paths:
        if Path(path).is_file():
            return path
    raise FileNotFoundError('Install Consolas and Segoe UI, or DejaVu fonts')

MONO = pick('C:/Windows/Fonts/consola.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
MONO_BOLD = pick('C:/Windows/Fonts/consolab.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf')
SANS = pick('C:/Windows/Fonts/segoeui.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
SANS_BOLD = pick('C:/Windows/Fonts/segoeuib.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')

def font(size, kind='mono'):
    return ImageFont.truetype({'mono': MONO, 'mono_bold': MONO_BOLD, 'sans': SANS, 'sans_bold': SANS_BOLD}[kind], size)

def write(d, pos, text, size, color, kind='mono'):
    d.text(pos, text, fill=color, font=font(size, kind))

BG = (9, 17, 28)
BAR = (16, 28, 42)
BORDER = (42, 65, 84)
RULE = (36, 57, 75)
WHITE = (228, 238, 246)
MUTED = (151, 174, 191)
DIM = (102, 132, 155)
BLUE = (121, 195, 244)
CYAN = (125, 210, 220)

base = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(base)
d.rectangle((1, 1, W-2, H-2), outline=BORDER, width=2)
d.rectangle((2, 2, W-3, 58), fill=BAR)
d.line((2, 58, W-2, 58), fill=BORDER, width=1)
for i, color in enumerate(((95, 113, 128), (95, 113, 128), (121, 195, 244))):
    d.ellipse((28+i*18, 25, 36+i*18, 33), fill=color)
write(d, (96, 17), 'eren@lab: ~', 19, MUTED)
write(d, (833, 20), 'PROFILE.SH', 15, DIM)

# A terminal header, with a small topology rather than decorative 3D imagery.
write(d, (51, 100), '// SYSTEMS  /  CLOUD  /  INFRASTRUCTURE', 17, BLUE, 'mono_bold')
write(d, (48, 145), 'EREN', 62, WHITE, 'sans_bold')
write(d, (48, 210), 'KARAOĞLU', 55, WHITE, 'sans_bold')
write(d, (52, 290), 'BUILD  /  TROUBLESHOOT  /  AUTOMATE', 16, MUTED, 'mono_bold')

# Thin-line topology: conceptual interests, not a claim of a live system.
write(d, (650, 104), 'CONNECTED FIELDS', 15, DIM, 'mono_bold')
center=(782, 208)
nodes=[((665,163),'SYS'),((901,163),'CLOUD'),((665,252),'NET'),((901,252),'AUTO')]
for p,_ in nodes:
    d.line((center,p), fill=(48,96,125), width=2)
for (x,y),name in nodes:
    d.rectangle((x-39,y-15,x+39,y+15), outline=(65,124,155), fill=BG, width=1)
    width=d.textlength(name, font=font(14,'mono_bold'))
    write(d, (x-width/2,y-9), name, 14, BLUE, 'mono_bold')
d.rectangle((center[0]-34,center[1]-19,center[0]+34,center[1]+19), outline=BLUE, fill=BAR, width=2)
write(d,(center[0]-16,center[1]-11),'>_',18,WHITE,'mono_bold')

def divider(y): d.line((51,y,949,y), fill=RULE, width=1)
def section(y,number,title,command):
    write(d,(51,y),number,17,DIM,'mono_bold')
    write(d,(96,y),title,17,BLUE,'mono_bold')
    write(d,(51,y+36),'eren@lab:~$',19,BLUE,'mono_bold')
    write(d,(205,y+36),command,19,WHITE,'mono_bold')

divider(337)
section(361,'01','WHOAMI','whoami')
write(d,(51,433),'Information Systems Engineering graduate.',25,WHITE,'sans')
divider(527)
section(550,'02','FOCUS','cat focus.conf')
rows=[('systems','Linux  /  Windows Server  /  Active Directory'),
      ('cloud','Azure  /  Virtualization  /  Hybrid identity'),
      ('networks','Routing  /  Security  /  Monitoring'),
      ('automation','PowerShell  /  Bash  /  Python')]
for i,(key,value) in enumerate(rows):
    y=626+i*37
    write(d,(51,y),key,19,CYAN,'mono_bold')
    write(d,(213,y),'=',19,DIM)
    write(d,(241,y),value,19,WHITE)

divider(795)
section(818,'03','LEARNING','cat learning.log')
learning=[('NOW','Windows Server, Linux and Active Directory'),
          ('NEXT','Azure administration and hybrid identity'),
          ('EXPLORING','Terraform, Ansible and Kubernetes')]
for i,(key,value) in enumerate(learning):
    y=895+i*40
    write(d,(51,y),key,17,BLUE,'mono_bold')
    write(d,(210,y),value,19,WHITE)

divider(1043)
write(d,(51,1070),'eren@lab:~$',19,BLUE,'mono_bold')
write(d,(205,1070),'./keep-building',19,WHITE,'mono_bold')
write(d,(51,1110),'LEARN  >  BUILD  >  TROUBLESHOOT  >  AUTOMATE',19,MUTED,'mono_bold')
d.rectangle((2,1175,W-3,H-3), fill=BAR)
d.line((2,1175,W-2,1175), fill=BORDER, width=1)
d.ellipse((51,1200,61,1210),fill=BLUE)
write(d,(76,1193),'SYSTEMS / CLOUD / INFRASTRUCTURE',17,MUTED,'mono_bold')
write(d,(749,1194),'ERENTECHLABS',16,DIM,'mono_bold')

frames=[]
for k in range(36):
    frame=base.copy(); draw=ImageDraw.Draw(frame)
    # Small packets move along the topology; the rest remains steady.
    for i, (p,_) in enumerate(nodes):
        t=(k/36+i*.23)%1
        x=center[0]+(p[0]-center[0])*t
        y=center[1]+(p[1]-center[1])*t
        draw.ellipse((x-3,y-3,x+3,y+3),fill=(181,226,251))
    if k<18:
        cursor_x=51+int(draw.textlength('LEARN  >  BUILD  >  TROUBLESHOOT  >  AUTOMATE',font=font(19,'mono_bold')))+11
        draw.rectangle((cursor_x,1114,cursor_x+10,1131),fill=BLUE)
    frames.append(frame)

output=ROOT/'profile-terminal-v11.gif'
frames[0].save(output, save_all=True, append_images=frames[1:], duration=85,
               loop=0, optimize=True, disposal=2)
print(f'Created {output.name}: {output.stat().st_size:,} bytes')
