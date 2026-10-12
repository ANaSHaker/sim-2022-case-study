# Keeps rendered PNGs under ~1.45 MB: first gentle downscale (full color), palette quantization only as last resort.
import sys, os, glob, io
from PIL import Image
LIMIT = 1_450_000
d = sys.argv[1] if len(sys.argv) > 1 else '..'
for f in glob.glob(os.path.join(d, '*.png')):
    if os.path.getsize(f) <= LIMIT: continue
    src = Image.open(f).convert('RGB'); done = False
    for s in (0.92, 0.85, 0.78, 0.7):
        im = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
        if b.tell() <= LIMIT:
            open(f, 'wb').write(b.getvalue()); done = True
            print('scaled', os.path.basename(f), s, im.size, b.tell()); break
    if not done:
        src.quantize(256, dither=Image.Dither.FLOYDSTEINBERG).save(f, optimize=True)
        print('quantized', os.path.basename(f), os.path.getsize(f))
