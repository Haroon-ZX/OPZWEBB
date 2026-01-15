from PIL import Image
import os

# Files to convert (relative to Yellow folder)
files = [
    "WhatsApp Image 2026-01-08 at 6.04.01 PM (1).jpeg",
    "WhatsApp Image 2026-01-08 at 6.04.01 PM.jpeg",
    "WhatsApp Image 2026-01-08 at 6.04.02 PM (1).jpeg",
]

cwd = os.path.dirname(__file__)
output_dir = os.path.join(cwd, "out")
os.makedirs(output_dir, exist_ok=True)

# Parameters
THRESHOLD = 80  # distance threshold from background color to treat as background


def avg_corner_color(img):
    w, h = img.size
    samples = [img.getpixel((1,1)), img.getpixel((w-2,1)), img.getpixel((1,h-2)), img.getpixel((w-2,h-2))]
    r = sum([s[0] for s in samples])//len(samples)
    g = sum([s[1] for s in samples])//len(samples)
    b = sum([s[2] for s in samples])//len(samples)
    return (r,g,b)


def dist(c1, c2):
    return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5


for fname in files:
    path = os.path.join(cwd, '..', fname)
    if not os.path.exists(path):
        print(f"[SKIP] not found: {path}")
        continue

    print(f"Processing: {fname}")
    img = Image.open(path).convert("RGBA")
    bg = avg_corner_color(img)
    w,h = img.size

    pixels = img.load()

    for y in range(h):
        for x in range(w):
            r,g,b,a = pixels[x,y]
            d = dist((r,g,b), bg)
            if d < THRESHOLD:
                # make transparent with a small fade near edge
                alpha = int((d/THRESHOLD) * a)
                pixels[x,y] = (r,g,b,alpha)

    out_name = os.path.splitext(fname)[0] + ".png"
    out_path = os.path.join(output_dir, out_name)
    img.save(out_path)
    print(f"Saved: {out_path}")

print("Done.")
