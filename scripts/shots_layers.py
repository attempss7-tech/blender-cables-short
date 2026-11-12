# shots_layers.py — Shots 9-10 (frames 810-1079).
#
# Shot 9 (f810-968): cable cross-section, end-on. The petroleum jelly
#   layer WRAPS ON (f899-930), then the copper tubing WRAPS ON
#   (f936-963) — each with an orbiting wrap bead.
# Shot 10 (f969-1079): same cross-section language, new angle. The
#   high-tensile steel armor WRAPS ON (f970-1017), then the thick
#   waterproof tar WRAPS ON (f1034-1075); the finished cable rotates.
import math

import common as cm

X9, X10 = 480.0, 540.0


def _off(keys, x0):
    return [(f, (x + x0, y, z), lens) for f, (x, y, z), lens in keys]


def _off_f(keys, x0):
    return [(f, (x + x0, y, z)) for f, (x, y, z) in keys]


def _fiber_bundle(s, prefix, m_fiber):
    """7 glowing glass fibers in a hex pattern, axis along Y."""
    rot_y = (math.radians(90), 0, 0)
    # hex radius 0.36 (extent 0.47) — fits inside the jelly ring's hole
    fiber_pos = [(0, 0), (0.36, 0), (-0.36, 0), (0.18, 0.31),
                 (-0.18, 0.31), (0.18, -0.31), (-0.18, -0.31)]
    for i, (fx, fz) in enumerate(fiber_pos):
        cm.add_cylinder("%s_Fiber%d" % (prefix, i), 0.11, 2.4, m_fiber,
                        parent=s, loc=(fx, 0, fz), rot=rot_y, verts=12)


def _wrap_on(ring_group, bead, major_r, f_start, f_end, bead_mat,
             ring_mat=None):
    """Animate one layer wrapping on: the ring scales in from 1.25 with
    a spin, and a bead orbits once around it during the wrap. A seam
    marker (same material as the ring) rides the group's rotation so the
    spin is visible — a bare torus spinning about its own axis shows no
    motion."""
    if ring_mat is not None:
        cm.add_box(ring_group.name + "_Seam", (0.20, 0.34, 0.20),
                   ring_mat, parent=ring_group, loc=(major_r, 0, 0))
    cm.scale_key(ring_group, f_start, 1.25)
    cm.rot_key(ring_group, f_start, (0, 0, 0))
    cm.scale_key(ring_group, f_end, 1.0)
    cm.rot_key(ring_group, f_end, (0, 90, 0))
    # bead orbits once (in the XZ plane, facing the camera)
    n = 10
    for i in range(n + 1):
        f = f_start + (f_end - f_start) * i / n
        a = 2 * math.pi * i / n
        cm.loc_key(bead, int(round(f)),
                   (major_r * math.cos(a), 0.35,
                    major_r * math.sin(a)))
    cm.scale_key(bead, f_start, 1.0)
    cm.scale_key(bead, f_end, 1.0)
    cm.scale_key(bead, f_end + 1, 0.001)


def _ring(s, name, major_r, minor_r, mat, loc=(0, 0, 0)):
    """A layer ring facing the camera (+Y): torus rotated 90 deg about X
    so its plane is XZ."""
    return cm.add_torus(name, major_r, minor_r, mat, parent=s, loc=loc,
                        rot=(math.radians(90), 0, 0))


# ---------------------------------------------------------------- shot 9

def shot09(ctx):
    fs, fe = 810, 969
    s = cm.new_empty("Set09", loc=(X9, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_back = cm.flat_mat("S9_Back", "#04090f", 1.0)
    m_fiber = cm.emis_mat("S9_Fiber", "#35e0ff", 2.5)
    m_jelly = cm.flat_mat("S9_Jelly", "#e8d98a", 0.7)
    m_copper = cm.flat_mat("S9_Copper", "#b0662a", 0.35)
    m_bead = cm.emis_mat("S9_Bead", "#fff2a8", 3.5)

    cm.add_plane("S9_Back", 30, m_back, parent=s, loc=(0, -4, 0),
                 rot=(math.radians(90), 0, 0))
    _fiber_bundle(s, "S9", m_fiber)
    # the fragile fiber glows as "wrapped" is spoken (f886-896)
    cm.emis_key(m_fiber, 810, 2.5)
    cm.emis_key(m_fiber, 890, 4.0)
    cm.emis_key(m_fiber, 968, 2.5)

    # petroleum jelly ring wraps on f899-930
    jelly = cm.new_empty("S9_JellyGrp", parent=s)
    _ring(jelly, "S9_JellyRing", 0.70, 0.18, m_jelly)
    bead_j = cm.add_sphere("S9_BeadJ", 0.09, m_bead, parent=s,
                           loc=(0.70, 0.35, 0), seg=10, rings=8)
    cm.scale_key(jelly, 810, 0.001)
    cm.scale_key(jelly, 898, 0.001)
    _wrap_on(jelly, bead_j, 0.78, 899, 930, m_bead, m_jelly)
    cm.scale_key(jelly, 968, 1.0)
    # copper tubing ring wraps on f936-963
    copper = cm.new_empty("S9_CopperGrp", parent=s)
    _ring(copper, "S9_CopperRing", 1.05, 0.18, m_copper)
    bead_c = cm.add_sphere("S9_BeadC", 0.09, m_bead, parent=s,
                           loc=(1.05, 0.35, 0), seg=10, rings=8)
    cm.scale_key(copper, 810, 0.001)
    cm.scale_key(copper, 935, 0.001)
    _wrap_on(copper, bead_c, 1.13, 936, 963, m_bead, m_copper)
    cm.scale_key(copper, 968, 1.0)
    cm.scale_key(bead_j, 810, 0.001)
    cm.scale_key(bead_j, 898, 0.001)
    cm.scale_key(bead_c, 810, 0.001)
    cm.scale_key(bead_c, 935, 0.001)

    cam_keys = [(810, (0, 9.5, 0.5), 40), (890, (-0.4, 9, 0.4), 40),
                (968, (0.4, 8, 0.3), 42)]
    focus_keys = [(810, (0, 0, 0)), (968, (0, 0, 0))]
    cam, _ = cm.build_shot_camera("Cam09", _off(cam_keys, X9),
                                  _off_f(focus_keys, X9), fs, fe - 1)
    return (fs, cam)


# ---------------------------------------------------------------- shot 10

def shot10(ctx):
    fs, fe = 969, 1080
    s = cm.new_empty("Set10", loc=(X10, 0, 0))
    cm.visible_span(s, fs, fe - 1)

    m_back = cm.flat_mat("S10_Back", "#04090f", 1.0)
    m_fiber = cm.emis_mat("S10_Fiber", "#35e0ff", 2.5)
    m_jelly = cm.flat_mat("S10_Jelly", "#e8d98a", 0.7)
    m_copper = cm.flat_mat("S10_Copper", "#b0662a", 0.35)
    m_steel = cm.flat_mat("S10_Steel", "#7a828c", 0.45)
    m_wire = cm.flat_mat("S10_SteelWire", "#565e66", 0.4)
    m_tar = cm.flat_mat("S10_Tar", "#14100e", 0.95)
    m_bead = cm.emis_mat("S10_Bead", "#fff2a8", 3.5)

    cm.add_plane("S10_Back", 30, m_back, parent=s, loc=(0, -4, 0),
                 rot=(math.radians(90), 0, 0))
    _fiber_bundle(s, "S10", m_fiber)
    # already-wrapped inner layers, present from the start
    _ring(s, "S10_JellyRing", 0.70, 0.18, m_jelly)
    _ring(s, "S10_CopperRing", 1.05, 0.18, m_copper)

    # high-tensile steel armor wraps on f970-1017 (ring + wire ridges)
    steel = cm.new_empty("S10_SteelGrp", parent=s)
    _ring(steel, "S10_SteelRing", 1.40, 0.16, m_steel)
    for i, dy in enumerate((-0.25, 0.0, 0.25)):
        _ring(steel, "S10_SteelWire%d" % i, 1.40, 0.06, m_wire,
              loc=(0, dy, 0))
    bead_s = cm.add_sphere("S10_BeadS", 0.09, m_bead, parent=s,
                           loc=(1.40, 0.35, 0), seg=10, rings=8)
    cm.scale_key(steel, 969, 0.001)
    _wrap_on(steel, bead_s, 1.48, 970, 1017, m_bead, m_steel)
    cm.scale_key(steel, 1079, 1.0)
    cm.scale_key(bead_s, 969, 0.001)
    # thick waterproof tar wraps on f1034-1075
    tar = cm.new_empty("S10_TarGrp", parent=s)
    _ring(tar, "S10_TarRing", 1.72, 0.20, m_tar)
    bead_t = cm.add_sphere("S10_BeadT", 0.09, m_bead, parent=s,
                           loc=(1.72, 0.35, 0), seg=10, rings=8)
    cm.scale_key(tar, 969, 0.001)
    cm.scale_key(tar, 1033, 0.001)
    _wrap_on(tar, bead_t, 1.80, 1034, 1075, m_bead, m_tar)
    cm.scale_key(tar, 1079, 1.0)
    cm.scale_key(bead_t, 969, 0.001)
    cm.scale_key(bead_t, 1033, 0.001)
    # the finished cable is shown from a sweeping camera angle as the
    # shot closes (cam keys swing across it) — the wrap beads and seam
    # markers have already shown the rotation during each wrap.

    cam_keys = [(969, (1.6, 10, -1.2), 42), (1017, (0.8, 9.5, -0.8), 42),
                (1079, (-0.6, 9, -0.4), 40)]
    focus_keys = [(969, (0, 0, 0)), (1079, (0, 0, 0))]
    cam, _ = cm.build_shot_camera("Cam10", _off(cam_keys, X10),
                                  _off_f(focus_keys, X10), fs, fe - 1)
    return (fs, cam)


def build(ctx):
    return dict(cameras=[shot09(ctx), shot10(ctx)])
