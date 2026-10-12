"""Build the three-panel team-performance figure used as Figure 6(b).

Source: Figure_6_Team_Performance_Outcomes.png (original 2x2 chart, 2972x2231 px).
The mission-score panel (B) is dropped because its values were display examples,
not measured scores. Panels A (orders delivered), C (error count) and
D (appropriate support actions) are copied pixel-for-pixel at full resolution;
only the lettered panel titles are redrawn without letters, and the shared
footnote moves to the LaTeX caption.

Usage: python make_team_performance_panels.py <source.png> <output.png>
"""
import os
import sys

import matplotlib
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]

# Plot areas below each panel title (found from white-band analysis of the source).
# Left-column crops stop at LEFT_R so panel B's y-axis label (x ~1500-1560) is excluded.
SPLIT_X = 1577
LEFT_R = 1480
PANELS = [
    ("Orders delivered", (0, 205, LEFT_R, 1007)),
    ("Error count", (0, 1260, LEFT_R, 2054)),
    ("Appropriate support actions", (SPLIT_X, 1260, 2972, 2054)),
]
TITLE_H = 70
GAP = 40

src = Image.open(SRC).convert("RGB")
crops = [(title, src.crop(box)) for title, box in PANELS]
width = sum(c.width for _, c in crops) + GAP * (len(crops) - 1)
height = TITLE_H + max(c.height for _, c in crops)
out = Image.new("RGB", (width, height), "white")

font_path = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf", "DejaVuSans-Bold.ttf")
font = ImageFont.truetype(font_path, 46)
draw = ImageDraw.Draw(out)

x = 0
for title, crop in crops:
    out.paste(crop, (x, TITLE_H))
    draw.text((x + 60, TITLE_H // 2), title, font=font, fill="black", anchor="lm")
    x += crop.width + GAP

out.save(OUT, optimize=True)
print(OUT, out.size)
