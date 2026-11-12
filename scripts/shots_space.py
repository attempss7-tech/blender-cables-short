# shots_space.py — Shots 1-3 (frames 0-371).
#
# Shot 1 (f0-134): space — a signal arc BOUNCES off a satellite, then
#   FADES OUT on "outer space" (f118-133). Earth below, stars, satellite.
# Shot 2 (f135-224): the camera DIVES DOWN through the water column past
#   fish to the muddy ocean floor where the cable lies ("mud" f165-175).
# Shot 3 (f225-371): world/ocean map — glowing cable lines STRETCH
#   (draw on) across the seafloor between continents.
import math
import random

import bpy
from mathutils import Vector

import common as cm

X1, X2, X3 = 0.0, 60.0, 120.0


def _off(keys, x0):
    """Offset camera/focus key x-coordinates into world space."""
    return [(f, (x + x0, y, z), lens) for f, (x, y, z), lens in keys]


def _off_f(keys, x0):
    return [(f, (x + x0, y, z)) for f, (x, y, z) in keys]


# ---------------------------------------------------------------- shot 1

def shot01(ctx):
    fs, fe = 0, 135
    s = cm.new_empty("Set01", loc=(X1, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_earth = cm.flat_mat("S1_Earth", "#2a6db0", 0.85)
    m_land = cm.flat_mat("S1_Land", "#3f8a4a", 0.95)
    m_cloud = cm.flat_mat("S1_Cloud", "#eef4fa", 1.0)
    m_star = cm.emis_mat("S1_Star", "#ffffff", 2.5)
    m_sat = cm.flat_mat("S1_SatBody", "#9aa4ae", 0.5)
    m_panel = cm.emis_mat("S1_SatPanel", "#2a4a9a", 1.2, base_hex="#1a2a5a")
    m_arc = cm.emis_mat("S1_Arc", "#35e0ff", 2.5)
    m_pulse = cm.emis_mat("S1_Pulse", "#aef4ff", 4.0)
    m_dish = cm.flat_mat("S1_Dish", "#c8ccd2", 0.6)

    # Earth: big sphere below, top arc in frame; continents + clouds
    earth = cm.add_sphere("S1_Earth", 14, m_earth, parent=s,
                          loc=(0, -6, -16), seg=36, rings=24)
    for i, (dx, dy, dz, sx, sy, sz) in enumerate([
            (-4.5, -1.0, -3.2, 3.2, 2.2, 0.7),
            (3.5, -2.0, -3.6, 2.6, 1.8, 0.6),
            (0.5, -4.5, -2.6, 2.0, 1.4, 0.5)]):
        cm.add_sphere("S1_Land%d" % i, 1, m_land, parent=s,
                      loc=(dx, dy, dz), scale=(sx, sy, sz))
    for i, (dx, dy, dz, sx) in enumerate([(-2.5, -3.0, -2.2, 2.4),
                                          (4.0, -5.0, -2.8, 1.8),
                                          (-5.5, -5.5, -3.4, 1.6)]):
        cm.add_sphere("S1_Cloud%d" % i, 1, m_cloud, parent=s,
                      loc=(dx, dy, dz), scale=(sx, sx * 0.5, 0.35))

    # stars: deterministic scatter on a dome (big enough to read at
    # render distance — the first build's 0.1-0.22 stars were sub-pixel)
    rnd = random.Random(42)
    for i in range(46):
        a = rnd.uniform(0, 2 * math.pi)
        e = rnd.uniform(0.15, 1.35)
        r = rnd.uniform(26, 36)
        loc = (r * math.cos(a) * math.cos(e), -r * math.sin(a) * 0.6 - 6,
               r * math.sin(e) - 6)
        cm.add_sphere("S1_Star%02d" % i, rnd.uniform(0.25, 0.45), m_star,
                      parent=s, loc=loc, seg=8, rings=6)

    # ground station dish on Earth's top
    dish = cm.add_cone("S1_GroundDish", 0.9, 0.15, 0.7, m_dish, parent=s,
                       loc=(1.5, -6, -1.9), rot=(math.radians(140), 0,
                                                 math.radians(-20)))
    cm.add_cylinder("S1_GroundMast", 0.08, 0.8, m_dish, parent=s,
                    loc=(1.5, -6, -2.4))

    # satellite: body + solar panels + dish, slow drift + yaw.
    # Scaled 0.7 — at full size the 4.3 m panel span overflowed the
    # narrow 9:16 frame (first-build stills).
    sat = cm.new_empty("S1_Sat", parent=s, loc=(0, 2, 4))
    sat.scale = (0.7, 0.7, 0.7)
    cm.add_box("S1_SatBody", (0.9, 0.9, 0.9), m_sat, parent=sat)
    cm.add_box("S1_SatPanelL", (1.7, 0.06, 0.8), m_panel, parent=sat,
               loc=(-1.3, 0, 0))
    cm.add_box("S1_SatPanelR", (1.7, 0.06, 0.8), m_panel, parent=sat,
               loc=(1.3, 0, 0))
    cm.add_cone("S1_SatDish", 0.45, 0.08, 0.4, m_dish, parent=sat,
                loc=(0, 0, -0.6), rot=(math.radians(180), 0, 0))
    cm.add_cylinder("S1_SatAnt", 0.03, 0.9, m_dish, parent=sat,
                    loc=(0.3, 0.3, 0.8))
    cm.loc_key(sat, 0, (0, 2, 4))
    cm.loc_key(sat, 70, (0.3, 2.1, 4.2))
    cm.loc_key(sat, 134, (0.6, 2.2, 4.4))
    cm.rot_key(sat, 0, (0, 0, 0))
    cm.rot_key(sat, 134, (0, 0, 24))

    # signal arc: ground station -> satellite -> back (the bounce path)
    arc_pts = [(1.5, -6, -1.6), (0.9, -2.5, 1.2), (0.2, 1.5, 3.6),
               (0, 2, 4.0), (-0.2, 1.5, 3.6), (-0.9, -2.5, 1.2),
               (-1.5, -6, -1.6)]
    arc = cm.add_tube("S1_Arc", arc_pts, 0.055, m_arc, parent=s)
    # pulse rides the arc: two bounces f60-88 and f88-117
    pulse = cm.add_sphere("S1_Pulse", 0.14, m_pulse, parent=s,
                          loc=arc_pts[0], seg=12, rings=8)
    for f in range(60, 118, 3):
        t = (f - 60) / 28.0 if f < 88 else (f - 88) / 29.0
        p = cm.curve_point_at(arc, min(1.0, max(0.0, t)))
        cm.loc_key(pulse, f, p)
    cm.scale_key(pulse, 60, 1.0)
    cm.scale_key(pulse, 117, 1.0)
    # f118-133 ("outer space"): the arc FADES OUT, satellite dims
    cm.emis_key(m_arc, 117, 2.5)
    cm.emis_key(m_arc, 133, 0.0)
    cm.scale_key(pulse, 133, 0.001)
    cm.emis_key(m_panel, 117, 1.2)
    cm.emis_key(m_panel, 133, 0.15)
    cm.emis_key(m_pulse, 117, 4.0)
    cm.emis_key(m_pulse, 133, 0.0)

    cam_keys = [(0, (0, 17, 9), 32), (60, (0, 15, 8), 32),
                (117, (0, 13.5, 7.2), 34), (134, (0, 13, 7), 35)]
    focus_keys = [(0, (0, 0, 3)), (60, (0, 1, 3.6)),
                  (134, (0.4, 2, 4.2))]
    cam, _ = cm.build_shot_camera("Cam01", _off(cam_keys, X1),
                                  _off_f(focus_keys, X1), fs, fe - 1)
    return (fs, cam)


# ---------------------------------------------------------------- shot 2

def shot02(ctx):
    fs, fe = 135, 225
    s = cm.new_empty("Set02", loc=(X2, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_mud = cm.flat_mat("S2_Mud", "#5a4632", 1.0)
    m_rock = cm.flat_mat("S2_Rock", "#4a4038", 1.0)
    m_cable = cm.flat_mat("S2_Cable", "#14181c", 0.9)
    m_ray = cm.emis_mat("S2_Ray", "#9fd4e8", 0.7, base_hex="#6a9ab0")
    m_fish = cm.flat_mat("S2_Fish", "#7a9ab0", 0.8)
    m_fish2 = cm.flat_mat("S2_Fish2", "#c08a4a", 0.8)
    m_bubble = cm.emis_mat("S2_Bubble", "#cfeef8", 1.0)

    # light rays from the surface (long pale cones, converging down).
    # Thin, far back (y=-8) and OFF the dive corridor: the second
    # build's centre ray still filled the top of the frame at f150.
    for i, (dx, tilt) in enumerate([(-8, 12), (7, -6), (-3.5, -14)]):
        cm.add_cone("S2_Ray%d" % i, 0.08, 0.7, 12, m_ray, parent=s,
                    loc=(dx, -8, 8), rot=(math.radians(180 + tilt), 0, 0))

    # fish swimming across at different depths, ON the dive corridor
    # (y=3.5) and big enough to read during the fast dive — the second
    # build's fish were too small and too far off-path to see at all
    fish_defs = [
        ("S2_FishA", m_fish, 10.0, -7, 7, 135, 200, 2.6),
        ("S2_FishB", m_fish2, 6.0, 7, -7, 145, 215, 2.2),
        ("S2_FishC", m_fish, 2.0, -8, 8, 155, 224, 2.8),
        ("S2_FishD", m_fish2, -1.0, 8, -8, 165, 224, 2.0),
    ]
    for name, mat, z, x0, x1, f0, f1, sc in fish_defs:
        fish = cm.new_empty(name, parent=s, loc=(x0, 3.5, z))
        cm.add_cone(name + "_Body", 0.16 * sc, 0.02, 0.7 * sc, mat,
                    parent=fish, rot=(0, math.radians(-90), 0))
        tail = cm.add_cone(name + "_Tail", 0.02, 0.22 * sc, 0.35 * sc, mat,
                           parent=fish, loc=(0.5 * sc, 0, 0),
                           rot=(0, math.radians(90), 0))
        cm.loc_key(fish, f0, (x0, 3.5, z))
        cm.loc_key(fish, f1, (x1, 3.5, z))
        if x1 < x0:  # swimming left: face -X
            cm.rot_key(fish, f0, (0, 0, 180))
            cm.rot_key(fish, f1, (0, 0, 180))
        # tail wag
        for f in range(f0, f1 + 1, 5):
            cm.rot_key(tail, f, (0, 90, 18 * math.sin((f - f0) * 0.9)))

    # bubbles rising
    for i in range(8):
        bx = -4 + i * 1.1
        bz = -5 + (i % 4) * 2.5
        bub = cm.add_sphere("S2_Bubble%d" % i, 0.06 + 0.02 * (i % 3),
                            m_bubble, parent=s, loc=(bx, 0, bz),
                            seg=10, rings=8)
        cm.loc_key(bub, 135, (bx, 0, bz))
        cm.loc_key(bub, 224, (bx + 0.5, 0, bz + 7))

    # muddy seafloor + rocks + the cable lying half-buried
    cm.add_plane("S2_Mud", 40, m_mud, parent=s, loc=(0, 0, -6))
    for i, (dx, dy, r) in enumerate([(-5, -2, 0.9), (4, -3, 1.2),
                                     (6, 2, 0.7), (-3, 3, 0.6),
                                     (1, -4, 0.8), (-2, 1.5, 0.7),
                                     (2.5, 2.5, 0.9), (-6, 1, 0.8)]):
        cm.add_sphere("S2_Rock%d" % i, r, m_rock, parent=s,
                      loc=(dx, dy, -5.9), scale=(1, 1, 0.55))
    cm.add_tube("S2_Cable", [(-9, 0.5, -5.82), (-4, 0, -5.78),
                             (0, -0.5, -5.82), (4, 0.3, -5.78),
                             (9, -0.3, -5.82)], 0.13, m_cable, parent=s)

    # light dims with depth across the dive (world strength keys)
    world = ctx["world"]
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Strength"].default_value = 1.0
    bg.inputs["Strength"].keyframe_insert(data_path="default_value",
                                          frame=135)
    bg.inputs["Strength"].default_value = 0.65
    bg.inputs["Strength"].keyframe_insert(data_path="default_value",
                                          frame=224)

    cam_keys = [(135, (0, 7, 15), 30), (165, (0, 6.5, 6), 30),
                (185, (0, 6.5, -0.5), 32), (224, (0, 7, -1.8), 34)]
    focus_keys = [(135, (0, 0, 9)), (165, (0, 0, 0)),
                  (185, (0, 0, -4)), (224, (0, 0, -5.0))]
    cam, _ = cm.build_shot_camera("Cam02", _off(cam_keys, X2),
                                  _off_f(focus_keys, X2), fs, fe - 1)
    return (fs, cam)


# ---------------------------------------------------------------- shot 3

def shot03(ctx):
    fs, fe = 225, 372
    s = cm.new_empty("Set03", loc=(X3, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_floor = cm.flat_mat("S3_Floor", "#0d2f4a", 1.0)
    m_land = cm.flat_mat("S3_Land", "#4a7a3a", 0.95)
    m_land2 = cm.flat_mat("S3_Land2", "#8a7a4a", 0.95)
    m_cable = cm.emis_mat("S3_Cable", "#35e0ff", 2.2)
    m_pulse = cm.emis_mat("S3_Pulse", "#aef4ff", 4.0)
    m_rock = cm.flat_mat("S3_Rock", "#2a3a4a", 1.0)

    cm.add_plane("S3_Floor", 60, m_floor, parent=s, loc=(0, 0, 0))
    # stylised continents (flattened shapes)
    conts = [
        ("S3_LandA", m_land, (-9, -5, 0.25), (4.5, 3.0, 0.35)),
        ("S3_LandB", m_land2, (8, -6, 0.25), (3.5, 2.5, 0.35)),
        ("S3_LandC", m_land, (9, 5, 0.25), (3.0, 3.5, 0.35)),
        ("S3_LandD", m_land2, (-8, 6, 0.25), (4.0, 2.8, 0.35)),
        ("S3_LandE", m_land, (0, 0, 0.2), (2.2, 1.6, 0.3)),
    ]
    for name, mat, loc, sc in conts:
        cm.add_sphere(name, 1, mat, parent=s, loc=loc, scale=sc)
    for i, (dx, dy) in enumerate([(-4, 3), (5, -2), (-1, -7), (3, 7)]):
        cm.add_sphere("S3_Rock%d" % i, 0.5, m_rock, parent=s,
                      loc=(dx, dy, 0.1), scale=(1, 1, 0.4))

    # glowing cable lines that DRAW ON (bevel_factor_end 0 -> 1)
    cables = [
        [(-9, -5, 0.45), (-4, -2, 0.4), (0, 0, 0.4), (5, -3, 0.4),
         (8, -6, 0.45)],
        [(-8, 6, 0.45), (-3, 3, 0.4), (0, 0, 0.4), (5, 2, 0.4),
         (9, 5, 0.45)],
        [(-9, -5, 0.45), (-6, 1, 0.4), (-8, 6, 0.45)],
        [(8, -6, 0.45), (9, 0, 0.4), (9, 5, 0.45)],
        [(-8, 6, 0.45), (-2, 8, 0.4), (4, 7, 0.4), (9, 5, 0.45)],
    ]
    draw_start = [240, 260, 285, 305, 325]
    curves = []
    for i, pts in enumerate(cables):
        cu = cm.add_tube("S3_Cable%d" % i, pts, 0.09, m_cable, parent=s)
        f0 = draw_start[i]
        cu.data.bevel_factor_end = 0.0
        cu.data.keyframe_insert(data_path="bevel_factor_end", frame=f0)
        cu.data.bevel_factor_end = 1.0
        cu.data.keyframe_insert(data_path="bevel_factor_end",
                                frame=f0 + 35)
        curves.append(cu)
    # data pulses travelling along the first two finished lines
    for j, cu in enumerate(curves[:2]):
        p = cm.add_sphere("S3_Pulse%d" % j, 0.16, m_pulse, parent=s,
                          loc=(0, 0, 0.4), seg=12, rings=8)
        f0 = draw_start[j] + 35
        for f in range(f0, 372, 4):
            t = ((f - f0) / 45.0) % 1.0
            cm.loc_key(p, f, cm.curve_point_at(cu, t))
        cm.scale_key(p, f0, 1.0)

    cam_keys = [(225, (13, 17, 20), 28), (300, (5, 16, 16), 28),
                (371, (-6, 15, 14), 30)]
    focus_keys = [(225, (0, 0, 0)), (300, (0, 0, 0)), (371, (-1, 0, 0))]
    cam, _ = cm.build_shot_camera("Cam03", _off(cam_keys, X3),
                                  _off_f(focus_keys, X3), fs, fe - 1)
    return (fs, cam)


def build(ctx):
    return dict(cameras=[shot01(ctx), shot02(ctx), shot03(ctx)])
