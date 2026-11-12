# render_stills.py — Workbench validation stills (540x960) for the V4
# cables short. 2-3 frames per shot, chosen at the enacted-action beats.
# Run:
#   blender --background scenes/cables.blend --python scripts/render_stills.py
# Frames can be overridden: --frames 120,190,300
import os
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
STILLS = os.path.join(ROOT, "out", "stills")
os.makedirs(STILLS, exist_ok=True)

# (frame, shot, what to check)
STILL_FRAMES = [
    (60, 1, "satellite + arc bouncing"),
    (120, 1, "arc fading on 'outer space'"),
    (150, 2, "diving through water column"),
    (190, 2, "approaching the mud floor"),
    (220, 2, "cable lying on the mud"),
    (250, 3, "first cables drawing on"),
    (300, 3, "network stretching across map"),
    (360, 3, "all cables drawn"),
    (400, 4, "pushing into the core"),
    (430, 4, "data pulses racing"),
    (470, 4, "core close-up"),
    (500, 5, "hair sliding in"),
    (530, 5, "hair vs fiber, fiber pulsing"),
    (580, 6, "arrows closing in"),
    (630, 6, "cable squeezed at 'pressure'"),
    (660, 7, "plates starting to shift"),
    (700, 7, "plate shifted, cable dragged"),
    (725, 8, "shark swimming in"),
    (745, 8, "shark biting the cable"),
    (790, 8, "shark swimming off"),
    (890, 9, "fiber glowing, 'wrapped'"),
    (920, 9, "jelly wrapping on"),
    (950, 9, "copper wrapping on"),
    (1000, 10, "steel armor wrapping on"),
    (1055, 10, "tar wrapping on"),
    (1120, 11, "three cables, highlight pulse"),
    (1160, 11, "THREE cables snapped at once"),
    (1195, 11, "severed ends glowing"),
    (1230, 12, "clerk pointing at screens"),
    (1290, 12, "screens freezing, frost in"),
    (1320, 12, "frozen bank, clerk still"),
    (1360, 13, "first buildings going dark"),
    (1400, 13, "world nearly dark"),
    (1415, 13, "final dark frame"),
]

FRAMES = [f for f, _, _ in STILL_FRAMES]
if "--frames" in sys.argv:
    i = sys.argv.index("--frames")
    FRAMES = [int(x) for x in sys.argv[i + 1].split(",")]

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.light = 'FLAT'
scene.display.shading.color_type = 'MATERIAL'
scene.display.shading.show_object_outline = False
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 50  # 540x960
scene.render.image_settings.file_format = 'PNG'

for f in FRAMES:
    t0 = time.time()
    scene.frame_set(f)
    scene.render.filepath = os.path.join(STILLS, "f%04d.png" % f)
    bpy.ops.render.render(write_still=True)
    print("STILL f%04d in %.1fs" % (f, time.time() - t0))

print("STILLS DONE:", len(FRAMES), "frames ->", STILLS)
