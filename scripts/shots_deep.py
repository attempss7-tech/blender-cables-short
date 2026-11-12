# shots_deep.py — Shots 6-8 (frames 555-809).
#
# Shot 6 (f555-640): crushing pressure — arrows CLOSE IN from all sides
#   and the cable SQUEEZES ("pressure" f621-638).
# Shot 7 (f641-719): shifting continental shelves — seafloor plates
#   GRIND and SHIFT under the cable, which drags and bends.
# Shot 8 (f720-809): a shark swims up and BITES the cable ("chew"
#   f738-747) while EM field rings shimmer around it.
import math

from mathutils import Vector

import common as cm

X6, X7, X8 = 300.0, 360.0, 420.0


def _off(keys, x0):
    return [(f, (x + x0, y, z), lens) for f, (x, y, z), lens in keys]


def _off_f(keys, x0):
    return [(f, (x + x0, y, z)) for f, (x, y, z) in keys]


# ---------------------------------------------------------------- shot 6

def shot06(ctx):
    fs, fe = 555, 641
    s = cm.new_empty("Set06", loc=(X6, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_mud = cm.flat_mat("S6_Mud", "#5a4632", 1.0)
    m_cable = cm.flat_mat("S6_Cable", "#14181c", 0.9)
    m_arrow = cm.emis_mat("S6_Arrow", "#ff9a3c", 1.6, base_hex="#c85a1a")
    m_rock = cm.flat_mat("S6_Rock", "#4a4038", 1.0)

    cm.add_plane("S6_Mud", 30, m_mud, parent=s, loc=(0, 0, 0))
    for i, (dx, dy, r) in enumerate([(-4, -2, 0.8), (4.5, -2.5, 1.0),
                                     (5, 2, 0.6), (-5, 2.5, 0.7)]):
        cm.add_sphere("S6_Rock%d" % i, r, m_rock, parent=s,
                      loc=(dx, dy, 0.1), scale=(1, 1, 0.55))
    cable = cm.add_tube("S6_Cable", [(-7, 0, 0.18), (-3, 0.2, 0.15),
                                     (0, -0.2, 0.18), (3, 0.2, 0.15),
                                     (7, 0, 0.18)], 0.18, m_cable, parent=s)

    # pressure arrows: 6 directions converging on the cable centre.
    # Upper hemisphere ONLY — the first build's lower arrows sat under
    # the mud plane, and at 0.55 m the fat arrows piled into one orange
    # blob hiding the cable. Smaller arrows, stopping 1.0 m out.
    centre = Vector((0, 0, 0.18))
    dirs = []
    for ang in (25, 65, 105, 145):
        a = math.radians(ang)
        dirs.append(Vector((math.cos(a) * 0.8, 0, math.sin(a))))
    dirs.append(Vector((0, 1, 0.35)).normalized())
    dirs.append(Vector((0, -1, 0.35)).normalized())
    for i, d in enumerate(dirs):
        d = d.normalized()
        arr = cm.new_empty("S6_Arrow%d" % i, parent=s)
        cone = cm.add_cone("S6_ArrowCone%d" % i, 0.18, 0.02, 0.6, m_arrow,
                           parent=arr, rot=(0, 0, 0))
        shaft = cm.add_cylinder("S6_ArrowShaft%d" % i, 0.05, 0.6, m_arrow,
                                parent=arr, loc=(0, 0, -0.55), verts=10)
        # aim the cone's +Z at the centre (cone apex points +Z)
        arr.rotation_euler = (-d).to_track_quat('Z', 'Y').to_euler()
        for f, dist in ((555, 3.4), (600, 2.4), (621, 1.3), (630, 1.0),
                        (640, 1.1)):
            cm.loc_key(arr, f, tuple(centre + d * dist))
    # the cable SQUEEZES at "pressure" (f621-638) and partially rebounds
    cm.scale_key(cable, 555, (1.0, 1.0, 1.0))
    cm.scale_key(cable, 620, (1.0, 1.0, 1.0))
    cm.scale_key(cable, 630, (1.0, 0.82, 0.82))
    cm.scale_key(cable, 638, (1.0, 0.90, 0.90))
    cm.scale_key(cable, 640, (1.0, 0.92, 0.92))
    # creak shudder at the squeeze peak
    for f, jx in ((624, 0.03), (627, -0.03), (630, 0.03), (633, -0.02),
                  (636, 0.02)):
        cm.loc_key(cable, f, (jx, 0, 0))
    cm.loc_key(cable, 640, (0, 0, 0))

    cam_keys = [(555, (2.5, 9, 2.0), 38), (600, (2.0, 8, 1.6), 40),
                (640, (1.5, 7, 1.2), 42)]
    focus_keys = [(555, (0, 0, 0.2)), (640, (0, 0, 0.2))]
    cam, _ = cm.build_shot_camera("Cam06", _off(cam_keys, X6),
                                  _off_f(focus_keys, X6), fs, fe - 1)
    return (fs, cam)


# ---------------------------------------------------------------- shot 7

def shot07(ctx):
    fs, fe = 641, 720
    s = cm.new_empty("Set07", loc=(X7, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_plate = cm.flat_mat("S7_Plate", "#6a5138", 1.0)
    m_plate2 = cm.flat_mat("S7_Plate2", "#5a4632", 1.0)
    m_crack = cm.flat_mat("S7_Crack", "#0a0806", 1.0)
    m_cable = cm.flat_mat("S7_Cable", "#14181c", 0.9)
    m_rock = cm.flat_mat("S7_Rock", "#4a4038", 1.0)

    # ground plane BELOW the plates' bottoms (z=-0.95, not -0.9: at
    # -0.9 it was coplanar with the plate bottoms and z-fought into a
    # woven moire patch). Dark mud brown, not black — the black plane
    # read as a void band past the plates' far edge.
    m_under = cm.flat_mat("S7_Under", "#3a2c1e", 1.0)
    cm.add_plane("S7_Under", 30, m_under, parent=s, loc=(0, 0, -1.0))
    # two seafloor plates with a fault crack between them
    plate_l = cm.new_empty("S7_PlateL", parent=s, loc=(-4.2, 0, 0))
    cm.add_box("S7_PlateL_Top", (8.4, 7, 0.9), m_plate, parent=plate_l,
               loc=(0, 0, -0.45))
    for i, (dx, dy, r) in enumerate([(-2, -2, 0.8), (1.5, 2, 0.6),
                                     (-3, 1.5, 0.5)]):
        cm.add_sphere("S7_RockL%d" % i, r, m_rock, parent=plate_l,
                      loc=(dx, dy, 0.05), scale=(1, 1, 0.5))
    plate_r = cm.new_empty("S7_PlateR", parent=s, loc=(4.2, 0, 0))
    cm.add_box("S7_PlateR_Top", (8.4, 7, 0.9), m_plate2, parent=plate_r,
               loc=(0, 0, -0.45))
    for i, (dx, dy, r) in enumerate([(2, -2, 0.7), (-1.5, 2.5, 0.9),
                                     (3, 1, 0.5)]):
        cm.add_sphere("S7_RockR%d" % i, r, m_rock, parent=plate_r,
                      loc=(dx, dy, 0.05), scale=(1, 1, 0.5))
    # crack: wide + low so it reads as a dark gap, never poking above
    # the plate tops. Depth 6.9 (NOT 7.0): at 7.0 its front/back faces
    # were coplanar with the plates' front/back faces (y=+-3.5) and
    # z-fought into a woven moire patch on the right plate (diagnosed
    # 2026-11-12 by hide-and-render probes).
    cm.add_box("S7_Crack", (1.6, 6.9, 0.8), m_crack, parent=s,
               loc=(0, 0, -0.55))
    cable = cm.add_tube("S7_Cable", [(-7.5, 0, 0.18), (-3, 0.2, 0.15),
                                     (0, 0, 0.10), (3, -0.2, 0.15),
                                     (7.5, 0, 0.18)], 0.18, m_cable,
                        parent=s)
    # the left plate GRINDS sideways (f650-700) with a final jolt (f705)
    # — 1.8 m of shift so the movement reads clearly at render distance
    cm.loc_key(plate_l, 641, (-4.2, 0, 0))
    cm.loc_key(plate_l, 670, (-4.9, 0.1, 0))
    cm.loc_key(plate_l, 700, (-5.8, 0.15, 0))
    cm.loc_key(plate_l, 705, (-6.0, 0.15, 0))
    cm.loc_key(plate_l, 719, (-6.0, 0.15, 0))
    cm.rot_key(plate_l, 641, (0, 0, 0))
    cm.rot_key(plate_l, 705, (0, 0, 2.5))
    cm.rot_key(plate_l, 719, (0, 0, 2.5))
    # the cable drags with the plate and sags into the widened crack
    cm.loc_key(cable, 641, (0, 0, 0))
    cm.loc_key(cable, 700, (-0.45, 0.05, -0.06))
    cm.loc_key(cable, 719, (-0.5, 0.05, -0.08))
    cm.rot_key(cable, 641, (0, 0, 0))
    cm.rot_key(cable, 719, (0, 0, 2.0))
    # rock chips tumble into the crack
    for i in range(3):
        chip = cm.add_sphere("S7_Chip%d" % i, 0.12, m_rock, parent=s,
                             loc=(-0.6 - i * 0.3, -1 + i, 0.4),
                             seg=8, rings=6)
        f0 = 665 + i * 12
        cm.loc_key(chip, f0, (-0.6 - i * 0.3, -1 + i, 0.4))
        cm.loc_key(chip, f0 + 18, (-0.2 - i * 0.15, -1 + i, -0.35))

    cam_keys = [(641, (0, 11, 6), 35), (680, (-1.5, 10.5, 5.6), 35),
                (719, (-3, 10.5, 5.5), 36)]
    focus_keys = [(641, (0, 0, 0)), (719, (-1.5, 0, 0))]
    cam, _ = cm.build_shot_camera("Cam07", _off(cam_keys, X7),
                                  _off_f(focus_keys, X7), fs, fe - 1)
    return (fs, cam)


# ---------------------------------------------------------------- shot 8

def _build_shark(s):
    """Own-built stylised shark from primitives, facing -X.
    Returns (root, jaw_pivot, tail)."""
    m_body = cm.flat_mat("S8_SharkBody", "#5a7086", 0.7)
    m_belly = cm.flat_mat("S8_SharkBelly", "#d8dee2", 0.8)
    m_fin = cm.flat_mat("S8_SharkFin", "#4a6074", 0.7)
    m_eye = cm.flat_mat("S8_SharkEye", "#0a0a0a", 0.4)
    m_mouth = cm.flat_mat("S8_SharkMouth", "#2a1214", 0.9)

    root = cm.new_empty("S8_Shark", parent=s, loc=(9, 1, 2.5))
    # scaled 0.55 — at full size the ~6 m shark filled the whole frame
    # (first-build stills); at 0.55 it reads against the cable + rings
    root.scale = (0.55, 0.55, 0.55)
    # body: elongated sphere, nose at -X
    cm.add_sphere("S8_Body", 0.9, m_body, parent=root,
                  scale=(2.3, 0.62, 0.68))
    cm.add_cone("S8_Snout", 0.5, 0.08, 1.1, m_body, parent=root,
                loc=(-2.3, 0, 0.05), rot=(0, math.radians(90), 0))
    cm.add_sphere("S8_Belly", 0.9, m_belly, parent=root,
                  loc=(0.1, 0, -0.18), scale=(2.0, 0.55, 0.5))
    # tail: upper + lower caudal fins (wagged as one group)
    tail = cm.new_empty("S8_Tail", parent=root, loc=(2.0, 0, 0))
    cm.add_cone("S8_TailUp", 0.08, 0.5, 1.0, m_fin, parent=tail,
                loc=(0.45, 0, 0.45), rot=(0, 0, math.radians(-35)),
                verts=4)
    cm.add_cone("S8_TailLow", 0.08, 0.35, 0.7, m_fin, parent=tail,
                loc=(0.4, 0, -0.3), rot=(math.radians(180), 0,
                                         math.radians(35)), verts=4)
    # dorsal + pectoral fins (flattened cones)
    cm.add_cone("S8_Dorsal", 0.1, 0.55, 1.0, m_fin, parent=root,
                loc=(0.2, 0, 0.75), rot=(0, 0, math.radians(-20)),
                verts=4)
    for side, sy in (("L", 1), ("R", -1)):
        cm.add_cone("S8_Pec%s" % side, 0.08, 0.4, 0.9, m_fin, parent=root,
                    loc=(-0.9, sy * 0.6, -0.25),
                    rot=(math.radians(sy * 55), 0, math.radians(-90)),
                    verts=4)
    # eyes + mouth
    for sy in (1, -1):
        cm.add_sphere("S8_Eye%s" % ("L" if sy > 0 else "R"), 0.09, m_eye,
                      parent=root, loc=(-1.7, sy * 0.5, 0.28),
                      seg=10, rings=8)
    cm.add_box("S8_Mouth", (0.9, 0.5, 0.12), m_mouth, parent=root,
               loc=(-1.9, 0, -0.42))
    # lower jaw: hinged, opens downward (rotation about Y)
    jaw = cm.new_empty("S8_Jaw", parent=root, loc=(-1.5, 0, -0.45))
    cm.add_box("S8_JawMesh", (1.1, 0.45, 0.1), m_belly, parent=jaw,
               loc=(-0.55, 0, -0.05))
    return root, jaw, tail


def shot08(ctx):
    fs, fe = 720, 810
    s = cm.new_empty("Set08", loc=(X8, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_mud = cm.flat_mat("S8_Mud", "#5a4632", 1.0)
    m_cable = cm.flat_mat("S8_Cable", "#14181c", 0.9)
    m_em = cm.emis_mat("S8_EMRing", "#35e0ff", 2.0)
    m_rock = cm.flat_mat("S8_Rock", "#4a4038", 1.0)

    cm.add_plane("S8_Mud", 30, m_mud, parent=s, loc=(0, 0, 0))
    for i, (dx, dy, r) in enumerate([(-5, -2.5, 0.8), (5.5, -2, 0.9),
                                     (-6, 2, 0.6)]):
        cm.add_sphere("S8_Rock%d" % i, r, m_rock, parent=s,
                      loc=(dx, dy, 0.1), scale=(1, 1, 0.55))
    cable = cm.add_tube("S8_Cable", [(-8, 0, 0.18), (-3, 0.2, 0.15),
                                     (0, -0.2, 0.18), (3, 0.2, 0.15),
                                     (8, 0, 0.18)], 0.18, m_cable, parent=s)
    # EM field rings shimmering around the cable (tori encircling it)
    rings = []
    for i, rx in enumerate((-2.0, -1.0, 0.0, 1.0, 2.0)):
        ring = cm.add_torus("S8_EMRing%d" % i, 0.55, 0.05, m_em, parent=s,
                            loc=(rx, 0, 0.18),
                            rot=(0, math.radians(90), 0))
        rings.append(ring)
    for f in range(720, 810, 6):
        sc = 1.0 + 0.10 * math.sin((f - 720) * 0.5)
        for ring in rings:
            cm.scale_key(ring, f, sc)
    # rings FLARE at the bite (f738-747), then flicker and settle
    cm.emis_key(m_em, 720, 2.0)
    cm.emis_key(m_em, 738, 2.0)
    cm.emis_key(m_em, 743, 5.5)
    cm.emis_key(m_em, 748, 2.5)
    cm.emis_key(m_em, 755, 4.5)
    cm.emis_key(m_em, 762, 2.0)
    cm.emis_key(m_em, 809, 2.0)

    shark, jaw, tail = _build_shark(s)
    # swim path: in from the right, bite at the cable, tug, swim off.
    # The scaled shark's mouth sits ~1.0 m ahead of its root, so the
    # bite root position is x=1.6 (mouth lands on the cable at x=0).
    cm.loc_key(shark, 720, (10, 1.0, 2.5))
    cm.loc_key(shark, 730, (6, 0.6, 1.6))
    cm.loc_key(shark, 738, (3.2, 0.2, 0.9))
    cm.loc_key(shark, 745, (1.6, 0, 0.62))
    cm.loc_key(shark, 760, (1.6, 0, 0.62))
    cm.loc_key(shark, 775, (2.8, 0.6, 1.2))
    cm.loc_key(shark, 809, (8, 2.0, 2.6))
    cm.rot_key(shark, 720, (0, 0, 0))
    cm.rot_key(shark, 745, (0, 0, 0))
    cm.rot_key(shark, 775, (0, 0, -18))
    cm.rot_key(shark, 809, (0, 0, -30))
    # head-shake tug while biting (f748-770)
    for f in range(748, 772, 4):
        cm.rot_key(shark, f, (0, 0, 6 * math.sin((f - 748) * 0.8)))
    cm.rot_key(shark, 775, (0, 0, -18))
    # tail wag throughout
    for f in range(720, 810, 5):
        cm.rot_key(tail, f, (0, 0, 14 * math.sin((f - 720) * 0.7)))
    # jaws: open f738-742, CLOSE ON the cable f743-747, release f748+
    cm.rot_key(jaw, 720, (0, 0, 0))
    cm.rot_key(jaw, 737, (0, 0, 0))
    cm.rot_key(jaw, 742, (0, -28, 0))
    cm.rot_key(jaw, 747, (0, 0, 0))
    cm.rot_key(jaw, 760, (0, 0, 0))
    cm.rot_key(jaw, 772, (0, -20, 0))
    cm.rot_key(jaw, 780, (0, 0, 0))
    # the cable jerks and shakes when bitten
    cm.loc_key(cable, 720, (0, 0, 0))
    cm.loc_key(cable, 742, (0, 0, 0))
    for f, jx, jz in ((744, 0.06, 0.05), (747, -0.05, -0.04),
                      (750, 0.05, 0.04), (754, -0.04, -0.03),
                      (758, 0.03, 0.02), (762, 0, 0)):
        cm.loc_key(cable, f, (jx, 0, jz))
    cm.loc_key(cable, 809, (0, 0, 0))

    cam_keys = [(720, (6, 10.5, 4), 36), (745, (1, 9.5, 2.6), 38),
                (775, (3, 10, 3), 38), (809, (5, 10.5, 3.5), 36)]
    focus_keys = [(720, (7, 0, 2)), (745, (1, 0, 0.6)),
                  (775, (2, 0, 1)), (809, (4, 0, 1.5))]
    cam, _ = cm.build_shot_camera("Cam08", _off(cam_keys, X8),
                                  _off_f(focus_keys, X8), fs, fe - 1)
    return (fs, cam)


def build(ctx):
    return dict(cameras=[shot06(ctx), shot07(ctx), shot08(ctx)])
