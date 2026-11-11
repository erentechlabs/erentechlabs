"""Encode the original image-generated frames as a looping profile GIF.

Install Pillow, then run: python tools/generate_profile.py
"""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent.parent
source_files = [root / 'assets/cloud-frame-01.png', root / 'assets/cloud-frame-02.png']
frames = []
for path in source_files:
    with Image.open(path) as source:
        frames.append(source.convert('RGB'))
if frames[0].size != frames[1].size:
    raise ValueError('Animation frames must have identical dimensions')
output = root / 'profile-cloud-v8.gif'
frames[0].save(output, save_all=True, append_images=frames[1:], duration=1500,
               loop=0, optimize=False, disposal=2)
print(f'Created {output.name} ({output.stat().st_size:,} bytes)')
