# shots_core.py — Shots 4-5 (frames 372-554).
#
# Shot 4 (f372-479): the camera pushes INTO a cable cross-section; the
#   outer layers peel back and glowing glass fibers carry data pulses
#   RACING toward the camera.
# Shot 5 (f480-554): a human hair SLIDES IN beside a glowing glass fiber
#   for scale — the fiber is barely thicker ("hair" f526-538).
import math

import common as cm

X4, X5 = 180.0, 240.0


def _off(keys, x0):
    return [(f, (x + x0, y, z), lens) for f, (x, y, z), lens in keys]


def _off_f(keys, x0):
    return [(f, (x + x0, y, z)) for f, (x, y, z) in keys]


# ---------------------------------------------------------------- shot 4

def shot04(ctx):
    fs, fe = 372, 480
    s = cm.new_empty("Set04", loc=(X4, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_back = cm.flat_mat("S4_Back", "#04090f", 1.0)
    m_tar = cm.flat_mat("S4_Tar", "#14100e", 0.95)
    m_steel = cm.flat_mat("S4_Steel", "#7a828c", 0.45)
    m_copper = cm.flat_mat("S4_Copper", "#b0662a", 0.35)
    m_jelly = cm.flat_mat("S4_Jelly", "#e8d98a", 0.7)
    m_fiber = cm.emis_mat("S4_Fiber", "#35e0ff", 2.5)
    m_pulse = cm.emis_mat("S4_Pulse", "#c8f6ff", 5.0)

    cm.add_plane("S4_Back", 30, m_back, parent=s, loc=(0, -4, 0),
                 rot=(math.radians(90), 0, 0))
    # concentric cable cross-section, axis along Y (facing the camera)
    rot_y = (math.radians(90), 0, 0)  # cylinder axis Z -> Y
    layers = [
        ("S4_Tar", 2.3, 1.4, m_tar),
        ("S4_Steel", 1.95, 1.5, m_steel),
        ("S4_Copper", 1.6, 1.6, m_copper),
        ("S4_Jelly", 1.25, 1.7, m_jelly),
    ]
    layer_objs = []
    for name, r, depth, mat in layers:
        o = cm.add_cylinder(name, r, depth, mat, parent=s, loc=(0, 0, 0),
                            rot=rot_y, verts=40)
        layer_objs.append(o)
    # the layers peel back (drift outward) as the camera closes in
    for o in layer_objs:
        cm.scale_key(o, 372, (1.0, 1.0, 1.0))
        cm.scale_key(o, 430, (1.10, 1.0, 1.10))
        cm.scale_key(o, 479, (1.10, 1.0, 1.10))
    # glowing fiber bundle: 7 thin fibers in a hex pattern
    fiber_pos = [(0, 0), (0.42, 0), (-0.42, 0), (0.21, 0.36),
                 (-0.21, 0.36), (0.21, -0.36), (-0.21, -0.36)]
    for i, (fx, fz) in enumerate(fiber_pos):
        cm.add_cylinder("S4_Fiber%d" % i, 0.11, 3.2, m_fiber, parent=s,
                        loc=(fx, 0.6, fz), rot=rot_y, verts=12)
    # data pulses RACE along the fibers toward the camera (f430-479)
    for j in range(6):
        fx, fz = fiber_pos[j % len(fiber_pos)]
        p = cm.add_sphere("S4_Pulse%d" % j, 0.11, m_pulse, parent=s,
                          loc=(fx, -1.0, fz), seg=10, rings=8)
        f0 = 430 + j * 8
        cm.loc_key(p, f0, (fx, -1.0, fz))
        cm.loc_key(p, min(479, f0 + 30), (fx, 2.6, fz))
        cm.scale_key(p, f0, 1.0)
        cm.scale_key(p, min(479, f0 + 30), 1.0)

    cam_keys = [(372, (0, 11, 1.0), 35), (430, (0.4, 7.5, 0.6), 40),
                (479, (0.8, 6.5, 0.4), 45)]
    focus_keys = [(372, (0, 0, 0)), (430, (0, 0.5, 0)),
                  (479, (0, 1.0, 0))]
    cam, _ = cm.build_shot_camera("Cam04", _off(cam_keys, X4),
                                  _off_f(focus_keys, X4), fs, fe - 1)
    return (fs, cam)


# ---------------------------------------------------------------- shot 5

def shot05(ctx):
    fs, fe = 480, 555
    s = cm.new_empty("Set05", loc=(X5, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_back = cm.flat_mat("S5_Back", "#06060c", 1.0)
    m_hair = cm.flat_mat("S5_Hair", "#4a2e18", 0.8)
    m_fiber = cm.emis_mat("S5_Fiber", "#35e0ff", 2.5)
    m_tip = cm.emis_mat("S5_FiberTip", "#c8f6ff", 4.0)

    cm.add_plane("S5_Back", 30, m_back, parent=s, loc=(0, -4, 3),
                 rot=(math.radians(90), 0, 0))
    # the glass fiber: thin vertical glowing strand. Strands sit at
    # x=+-0.55 — the first build's +-0.9 put both at the frame edges in
    # the narrow 9:16 frame.
    fiber = cm.add_cylinder("S5_Fiber", 0.055, 6.0, m_fiber, parent=s,
                            loc=(0.55, 0, 3), verts=12)
    cm.add_sphere("S5_FiberTip", 0.09, m_tip, parent=s, loc=(0.55, 0, 6.0),
                  seg=10, rings=8)
    # the human hair: slightly thicker wavy brown strand, slides in
    hair_pts = [(0, 0, 0), (0.12, 0, 1.5), (-0.10, 0, 3.0),
                (0.12, 0, 4.5), (0, 0, 6.0)]
    hair = cm.add_tube("S5_Hair", hair_pts, 0.085, m_hair, parent=s,
                       loc=(-5.0, 0, 0))
    cm.loc_key(hair, 480, (-5.0, 0, 0))
    cm.loc_key(hair, 510, (-0.55, 0, 0))
    cm.loc_key(hair, 554, (-0.55, 0, 0))
    # both strands sway gently once the hair arrives
    for f in range(510, 555, 8):
        sway = 2.0 * math.sin((f - 510) * 0.35)
        cm.rot_key(hair, f, (0, 0, sway))
        cm.rot_key(fiber, f, (0, 0, -sway * 0.6))
    # the fiber pulses brighter on "hair" (f526-538)
    cm.emis_key(m_fiber, 510, 2.5)
    cm.emis_key(m_fiber, 530, 5.0)
    cm.emis_key(m_fiber, 554, 2.8)

    cam_keys = [(480, (0, 11, 3), 40), (510, (0, 10, 3), 40),
                (554, (0, 8.5, 3), 42)]
    focus_keys = [(480, (0, 0, 3)), (554, (0, 0, 3))]
    cam, _ = cm.build_shot_camera("Cam05", _off(cam_keys, X5),
                                  _off_f(focus_keys, X5), fs, fe - 1)
    return (fs, cam)


def build(ctx):
    return dict(cameras=[shot04(ctx), shot05(ctx)])
