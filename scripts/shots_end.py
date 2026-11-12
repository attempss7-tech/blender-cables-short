# shots_end.py — Shots 11-13 (frames 1080-1417).
#
# Shot 11 (f1080-1207): THREE cables SNAP AT ONCE ("snapped" f1154-1165)
#   — ends whip apart, sparks fly, severed fiber ends glow.
# Shot 12 (f1208-1332): bank screens + cloud icons FREEZE ("freeze"
#   f1281-1296) — spinners halt, frost scales in, the flat 2D clerk
#   freezes mid-gesture. Humans are Grease Pencil 2D (shared/2d_rig.py).
# Shot 13 (f1333-1417): the modern world goes DARK — city lights go out
#   one by one ("disconnected" f1387-1411).
import importlib.util
import math
import os

import common as cm

X11, X12, X13 = 600.0, 660.0, 720.0

# 2d_rig.py starts with a digit — import via importlib (see
# shared/build_proof.py). The rig has the 180 deg base yaw fix: do NOT
# "fix" it back; facing_deg=0 faces a +Y camera upright.
_SHARED = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared"))
_spec = importlib.util.spec_from_file_location(
    "two_d_rig", os.path.join(_SHARED, "2d_rig.py"))
rig2d = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rig2d)


def _off(keys, x0):
    return [(f, (x + x0, y, z), lens) for f, (x, y, z), lens in keys]


def _off_f(keys, x0):
    return [(f, (x + x0, y, z)) for f, (x, y, z) in keys]


# ---------------------------------------------------------------- shot 11

def shot11(ctx):
    fs, fe = 1080, 1208
    s = cm.new_empty("Set11", loc=(X11, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_mud = cm.flat_mat("S11_Mud", "#5a4632", 1.0)
    m_rock = cm.flat_mat("S11_Rock", "#4a4038", 1.0)
    m_spark = cm.emis_mat("S11_Spark", "#ffd23c", 5.0)
    m_end = cm.emis_mat("S11_FiberEnd", "#35e0ff", 4.0)

    cm.add_plane("S11_Mud", 30, m_mud, parent=s, loc=(0, 0, 0))
    for i, (dx, dy, r) in enumerate([(-5, -2.5, 0.8), (5.5, -2, 0.9),
                                     (-6, 2.5, 0.6), (6, 2.5, 0.7)]):
        cm.add_sphere("S11_Rock%d" % i, r, m_rock, parent=s,
                      loc=(dx, dy, 0.1), scale=(1, 1, 0.55))

    # three parallel cables; each is TWO halves on pivot empties at the
    # snap point so the halves can WHIP apart.
    halves = []  # (pivot, side_sign)
    for ci, cy in enumerate((-1.6, 0.0, 1.6)):
        m_cable = cm.emis_mat("S11_Cable%d" % ci, "#1a2028", 0.25,
                              base_hex="#14181c")
        for side, sx in (("L", -1), ("R", 1)):
            pivot = cm.new_empty("S11_C%d%s_Pivot" % (ci, side), parent=s,
                                 loc=(sx * 0.1, cy, 0.18))
            # halves OVERLAP 0.15 m past the centre so the cable reads as
            # whole before the snap (the first build's 0.5 m gap read as
            # already-snapped)
            pts = ([(0.15, 0, 0), (-2.5, 0.1, -0.02), (-5, -0.1, 0),
                    (-7.2, 0, 0)] if side == "L" else
                   [(-0.15, 0, 0), (2.5, -0.1, -0.02), (5, 0.1, 0),
                    (7.2, 0, 0)])
            cm.add_tube("S11_C%d%s" % (ci, side), pts, 0.18, m_cable,
                        parent=pivot)
            # glowing severed fiber end at the cut (hidden until the snap)
            end = cm.add_sphere("S11_C%d%s_End" % (ci, side), 0.16, m_end,
                                parent=pivot, loc=(sx * 0.18, 0, 0),
                                seg=10, rings=8)
            cm.scale_key(end, 1080, 0.001)
            cm.scale_key(end, 1154, 0.001)
            cm.scale_key(end, 1156, 1.0)
            cm.scale_key(end, 1207, 1.0)
            halves.append((pivot, sx, ci))
    # "three" (f1111-1120): a highlight pulse runs along the cables 1-2-3
    for ci in range(3):
        m = cm.emis_mat("S11_Cable%d" % ci, "#1a2028", 0.25,
                        base_hex="#14181c")
        f0 = 1111 + ci * 3
        cm.emis_key(m, 1080, 0.25)
        cm.emis_key(m, f0, 1.6)
        cm.emis_key(m, f0 + 4, 0.25)
    # THE SNAP (f1154-1165): all three snap AT ONCE — halves whip apart
    # (25 deg, not 38 — the first build's wider whip pushed the severed
    # ends out of frame by f1195)
    for pivot, sx, ci in halves:
        cm.rot_key(pivot, 1080, (0, 0, 0))
        cm.rot_key(pivot, 1153, (0, 0, 0))
        cm.rot_key(pivot, 1165, (0, 0, sx * 25))
        cm.rot_key(pivot, 1185, (0, 0, sx * 28))
        cm.loc_key(pivot, 1080, (sx * 0.1, (-1.6, 0.0, 1.6)[ci], 0.18))
        cm.loc_key(pivot, 1153, (sx * 0.1, (-1.6, 0.0, 1.6)[ci], 0.18))
        cm.loc_key(pivot, 1165, (sx * 0.7, (-1.6, 0.0, 1.6)[ci], 0.35))
        cm.loc_key(pivot, 1207, (sx * 0.8, (-1.6, 0.0, 1.6)[ci], 0.22))
    # sparks burst from the three snap points
    for i in range(12):
        ci = i % 3
        cy = (-1.6, 0.0, 1.6)[ci]
        ang = (i * 2.399) % (2 * math.pi)
        dx, dz = math.cos(ang) * 1.6, abs(math.sin(ang)) * 1.4 + 0.3
        sp = cm.add_sphere("S11_Spark%02d" % i, 0.07, m_spark, parent=s,
                           loc=(0, cy, 0.2), seg=8, rings=6)
        cm.scale_key(sp, 1080, 0.001)
        cm.scale_key(sp, 1154, 0.001)
        cm.scale_key(sp, 1156, 1.0)
        cm.loc_key(sp, 1155, (0, cy, 0.2))
        cm.loc_key(sp, 1185, (dx, cy + 0.3 * math.sin(ang), 0.2 + dz))
        cm.scale_key(sp, 1195, 0.4)
        cm.scale_key(sp, 1207, 0.001)

    cam_keys = [(1080, (0, 10.5, 3.2), 35), (1154, (0, 9.5, 2.8), 35),
                (1207, (0, 9, 2.6), 36)]
    focus_keys = [(1080, (0, 0, 0.2)), (1207, (0, 0, 0.2))]
    cam, _ = cm.build_shot_camera("Cam11", _off(cam_keys, X11),
                                  _off_f(focus_keys, X11), fs, fe - 1)
    # camera shake at the snap (f1154-1170): re-key the sampled path
    # position plus a jitter offset (base recomputed per frame — the
    # camera's current location is the last keyed value, not the path)
    from mathutils import Vector as _V
    _pts = [(f, _V((x + X11, y, z)), lens)
            for f, (x, y, z), lens in cam_keys]
    for f, jx, jz in ((1155, 0.10, 0.06), (1158, -0.09, -0.05),
                      (1161, 0.07, 0.04), (1164, -0.05, -0.03),
                      (1167, 0.03, 0.02), (1170, 0, 0)):
        base, _lens = cm._sample_keys(_pts, f)
        cam.location = (base.x + jx, base.y, base.z + jz)
        cm.kf(cam, f, "location")
    return (fs, cam)


# ---------------------------------------------------------------- shot 12

def shot12(ctx):
    fs, fe = 1208, 1333
    s = cm.new_empty("Set12", loc=(X12, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_floor = cm.flat_mat("S12_Floor", "#b8c0c8", 0.9)
    m_wall = cm.flat_mat("S12_Wall", "#d8e2ea", 0.95)
    m_counter = cm.flat_mat("S12_Counter", "#7a5a38", 0.8)
    m_screen = cm.emis_mat("S12_Screen", "#bfe0ff", 1.4,
                           base_hex="#9cc4e8")
    m_screen2 = cm.emis_mat("S12_Screen2", "#c8e8c8", 1.4,
                            base_hex="#a8d0a8")
    m_spinner = cm.emis_mat("S12_Spinner", "#ffffff", 3.0)
    m_bar = cm.emis_mat("S12_Bar", "#4a9ae8", 1.2)
    m_cloud = cm.flat_mat("S12_Cloud", "#f2f6fa", 1.0)
    m_frost = cm.emis_mat("S12_Frost", "#dceefb", 0.9,
                          base_hex="#c8e0f0")
    m_dot = cm.emis_mat("S12_Dot", "#ffd23c", 2.5)

    cm.add_plane("S12_Floor", 24, m_floor, parent=s, loc=(0, 0, 0))
    cm.add_plane("S12_Wall", 24, m_wall, parent=s, loc=(0, -3, 4),
                 rot=(math.radians(90), 0, 0))
    cm.add_box("S12_Counter", (3.4, 0.7, 1.1), m_counter, parent=s,
               loc=(0, -0.6, 0.55))
    # wall screens (bank) with spinning loaders + rising bars
    screens = []
    for i, (sx, mat) in enumerate(((-1.6, m_screen), (1.6, m_screen2))):
        scr = cm.add_plane("S12_Screen%d" % i, 1.0, mat, parent=s,
                           loc=(sx, -2.9, 2.3),
                           rot=(math.radians(90), 0, 0))
        scr.scale = (2.2, 1.3, 1)
        screens.append(scr)
        # spinner: orbiting bright dot (halts at f1281)
        dot = cm.add_sphere("S12_Spinner%d" % i, 0.09, m_spinner,
                            parent=s, loc=(sx, -2.8, 2.3),
                            seg=10, rings=8)
        for f in range(1208, 1282, 4):
            a = (f - 1208) * 0.35
            cm.loc_key(dot, f, (sx + 0.35 * math.cos(a), -2.8,
                                2.3 + 0.35 * math.sin(a)))
        # hold the last position after the freeze (no more keys = halted)
        a = (1280 - 1208) * 0.35
        cm.loc_key(dot, 1332, (sx + 0.35 * math.cos(a), -2.8,
                               2.3 + 0.35 * math.sin(a)))
        # rising bars on screen 0 (grow, then freeze)
        if i == 0:
            for b in range(3):
                bar = cm.add_box("S12_Bar%d" % b, (0.22, 0.06, 0.5),
                                 m_bar, parent=s,
                                 loc=(sx - 0.5 + b * 0.5, -2.85, 1.85))
                cm.scale_key(bar, 1208, (1, 1, 0.4))
                cm.scale_key(bar, 1240 + b * 12, (1, 1, 1.0 + b * 0.4))
                cm.scale_key(bar, 1280, (1, 1, 1.0 + b * 0.4))
                cm.scale_key(bar, 1332, (1, 1, 1.0 + b * 0.4))
    # cloud icon cluster with its own spinner + flowing data dots
    cloud = cm.new_empty("S12_Cloud", parent=s, loc=(0, -2.9, 3.9))
    for i, (dx, dz, r) in enumerate([(-0.5, 0, 0.32), (0, 0.12, 0.42),
                                     (0.5, 0, 0.32), (0, -0.12, 0.3)]):
        cm.add_sphere("S12_CloudPuff%d" % i, r, m_cloud, parent=cloud,
                      loc=(dx, 0, dz), scale=(1, 0.6, 1))
    cdot = cm.add_sphere("S12_CloudSpin", 0.08, m_spinner, parent=s,
                         loc=(0, -2.8, 3.9), seg=10, rings=8)
    for f in range(1208, 1282, 4):
        a = (f - 1208) * 0.4
        cm.loc_key(cdot, f, (0.7 * math.cos(a), -2.8,
                             3.9 + 0.7 * math.sin(a)))
    a = (1280 - 1208) * 0.4
    cm.loc_key(cdot, 1332, (0.7 * math.cos(a), -2.8,
                            3.9 + 0.7 * math.sin(a)))
    for j in range(3):
        d = cm.add_sphere("S12_DataDot%d" % j, 0.07, m_dot, parent=s,
                          loc=(0, -2.8, 3.0), seg=8, rings=6)
        f0 = 1220 + j * 15
        cm.loc_key(d, f0, (0, -2.8, 3.0))
        cm.loc_key(d, min(1280, f0 + 40), (0, -2.8, 3.75))
        cm.loc_key(d, 1332, (0, -2.8, 3.75))
    # frost planes SCALE IN over the screens at "freeze" (f1281-1296)
    # and over the cloud (f1300-1315); screens dim to grey
    for i, sx in enumerate((-1.6, 1.6)):
        fr = cm.add_plane("S12_Frost%d" % i, 1.0, m_frost, parent=s,
                          loc=(sx, -2.85, 2.3),
                          rot=(math.radians(90), 0, 0))
        fr.scale = (2.2, 1.3, 1)
        cm.scale_key(fr, 1208, 0.001)
        cm.scale_key(fr, 1280, 0.001)
        cm.scale_key(fr, 1296, (2.2, 1.3, 1))
        cm.scale_key(fr, 1332, (2.2, 1.3, 1))
    frc = cm.add_plane("S12_FrostCloud", 1.0, m_frost, parent=s,
                       loc=(0, -2.85, 3.9), rot=(math.radians(90), 0, 0))
    frc.scale = (1.8, 1.2, 1)
    cm.scale_key(frc, 1208, 0.001)
    cm.scale_key(frc, 1299, 0.001)
    cm.scale_key(frc, 1315, (1.8, 1.2, 1))
    cm.scale_key(frc, 1332, (1.8, 1.2, 1))
    cm.emis_key(m_screen, 1208, 1.4)
    cm.emis_key(m_screen, 1280, 1.4)
    cm.emis_key(m_screen, 1310, 0.25)
    cm.emis_key(m_screen2, 1208, 1.4)
    cm.emis_key(m_screen2, 1280, 1.4)
    cm.emis_key(m_screen2, 1310, 0.25)

    cam_keys = [(1208, (0, 6.5, 1.9), 38), (1281, (0, 6.0, 1.9), 38),
                (1332, (0, 5.5, 1.9), 40)]
    focus_keys = [(1208, (0, -1, 1.8)), (1332, (0, -1, 1.9))]
    cam, _ = cm.build_shot_camera("Cam12", _off(cam_keys, X12),
                                  _off_f(focus_keys, X12), fs, fe - 1)

    # ---- the 2D clerk (flat Grease Pencil human, @RicksClips3000 style)
    rig = rig2d.create_human(
        "Clerk", location=(X12 + 0.0, 0.9, 0), height=1.7,
        skin=(0.72, 0.48, 0.32), shirt=(0.15, 0.35, 0.65),
        pants=(0.20, 0.22, 0.30), hair=(0.12, 0.08, 0.06),
        shoe=(0.15, 0.12, 0.10), hat=None)
    rig["placement"].parent = s
    # placement is parented AFTER creation, so re-set its local location
    # (parent offset X12 is applied by the set empty itself)
    rig["placement"].location = (0.0, 0.9, 0)
    rig2d.idle(rig, 1208, 1240, cycles=1)
    # Point at the screen and FREEZE MID-GESTURE at f1281: manual keys
    # (the point()/head_turn() helpers lower the arm / return the head
    # at their end, so they can't hold a frozen pose). Arm up at f1245,
    # head turned at f1265, then NO MORE KEYS — the pose holds dead
    # still to the cut, which is the freeze.
    rig2d.settle_neutral(rig, 1240)
    rig2d._rot(rig["shoulder"]["R"], 1245, z_deg=-88, interp='BEZIER')
    rig2d._rot(rig["elbow"]["R"], 1245, z_deg=0, interp='BEZIER')
    rig2d._rot(rig["shoulder"]["R"], 1281, z_deg=-88, interp='BEZIER')
    rig2d._rot(rig["shoulder"]["R"], 1332, z_deg=-88, interp='BEZIER')
    rig2d._rot(rig["head_pivot"], 1250, y_deg=0, interp='BEZIER')
    rig2d._rot(rig["head_pivot"], 1265, y_deg=30, interp='BEZIER')
    rig2d._rot(rig["head_pivot"], 1281, y_deg=30, interp='BEZIER')
    rig2d._rot(rig["head_pivot"], 1332, y_deg=30, interp='BEZIER')
    rig2d.add_billboard(rig, cam)
    return (fs, cam)


# ---------------------------------------------------------------- shot 13

def shot13(ctx):
    fs, fe = 1333, 1418
    s = cm.new_empty("Set13", loc=(X13, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_ground = cm.flat_mat("S13_Ground", "#10141c", 1.0)
    m_build = cm.flat_mat("S13_Building", "#1c2432", 0.9)
    m_build2 = cm.flat_mat("S13_Building2", "#232c3c", 0.9)
    m_pole = cm.flat_mat("S13_Pole", "#2a2f38", 0.9)
    m_lamp = cm.emis_mat("S13_Lamp", "#ffd98a", 2.5)
    m_node = cm.emis_mat("S13_Node", "#35e0ff", 2.5)
    m_link = cm.emis_mat("S13_Link", "#35e0ff", 1.8)

    cm.add_plane("S13_Ground", 40, m_ground, parent=s, loc=(0, 0, 0))
    # 8 buildings in two rows; each has its OWN window material so the
    # lights go out building by building (staggered emission keys)
    buildings = [
        (-6.5, -2, 2.6, 5.0, m_build), (-3.2, -2, 3.0, 7.5, m_build2),
        (0.2, -2, 2.8, 10.0, m_build), (3.6, -2, 3.2, 6.0, m_build2),
        (6.8, -2, 2.6, 8.5, m_build),
        (-5.0, -6, 3.0, 9.0, m_build2), (0.5, -6, 3.4, 12.0, m_build),
        (5.5, -6, 3.0, 7.0, m_build2),
    ]
    for bi, (bx, by, bw, bh, bmat) in enumerate(buildings):
        cm.add_box("S13_Bldg%d" % bi, (bw, 2.4, bh), bmat, parent=s,
                   loc=(bx, by, bh / 2))
        m_win = cm.emis_mat("S13_Win%d" % bi, "#ffd98a", 2.2)
        # window grid on the front face (small emissive planes)
        ncols = max(2, int(bw / 0.8))
        nrows = max(2, int(bh / 1.4))
        for r in range(nrows):
            for c in range(ncols):
                wx = bx - bw / 2 + 0.5 + c * (bw - 1.0) / max(1, ncols - 1)
                wz = 1.0 + r * (bh - 2.0) / max(1, nrows - 1)
                cm.add_plane("S13_Win%d_%d_%d" % (bi, r, c), 0.42, m_win,
                             parent=s, loc=(wx, by + 1.21, wz),
                             rot=(math.radians(90), 0, 0))
        # lights go out: one building every ~8 frames from f1340
        f_off = 1340 + bi * 8
        cm.emis_key(m_win, 1333, 2.2)
        cm.emis_key(m_win, f_off, 2.2)
        cm.emis_key(m_win, f_off + 4, 0.0)
        cm.emis_key(m_win, 1417, 0.0)
    # streetlights die at f1360 / 1380 / 1400
    for i, (lx, f_off) in enumerate(((-4, 1360), (0, 1380), (4, 1400))):
        cm.add_cylinder("S13_Pole%d" % i, 0.07, 3.0, m_pole, parent=s,
                        loc=(lx, 1.5, 1.5), verts=8)
        lamp = cm.add_sphere("S13_Lamp%d" % i, 0.18, m_lamp, parent=s,
                             loc=(lx, 1.5, 3.1), seg=10, rings=8)
        m_l = cm.emis_mat("S13_LampM%d" % i, "#ffd98a", 2.5)
        lamp.data.materials.clear()
        lamp.data.materials.append(m_l)
        cm.emis_key(m_l, 1333, 2.5)
        cm.emis_key(m_l, f_off, 2.5)
        cm.emis_key(m_l, f_off + 3, 0.0)
    # network node sphere + glowing links above the city — fades last
    node = cm.add_sphere("S13_Node", 0.7, m_node, parent=s,
                         loc=(0, -3, 13.5), seg=16, rings=12)
    for i, (dx, dz) in enumerate([(-3, -2), (3, -2), (0, -4), (-2, 2),
                                  (2, 2)]):
        cm.add_tube("S13_Link%d" % i,
                    [(0, -3, 13.5), (dx * 0.5, -3, 13.5 + dz * 0.5),
                     (dx, -3, 13.5 + dz)], 0.05, m_link, parent=s)
        cm.add_sphere("S13_Node%d" % i, 0.16, m_node, parent=s,
                      loc=(dx, -3, 13.5 + dz), seg=10, rings=8)
    cm.emis_key(m_node, 1333, 2.5)
    cm.emis_key(m_node, 1387, 2.5)
    cm.emis_key(m_node, 1411, 0.0)
    cm.emis_key(m_link, 1333, 1.8)
    cm.emis_key(m_link, 1387, 1.8)
    cm.emis_key(m_link, 1411, 0.0)

    cam_keys = [(1333, (0, 24, 8), 30), (1375, (0, 26, 8.5), 30),
                (1417, (0, 28, 9), 30)]
    focus_keys = [(1333, (0, -3, 4.5)), (1417, (0, -3, 4.5))]
    cam, _ = cm.build_shot_camera("Cam13", _off(cam_keys, X13),
                                  _off_f(focus_keys, X13), fs, fe - 1)
    return (fs, cam)


def build(ctx):
    return dict(cameras=[shot11(ctx), shot12(ctx), shot13(ctx)])
