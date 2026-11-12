# common.py — shared helpers for the V4 subsea-cables Blender short.
#
# Conventions (same as the chicken build):
# - One scene, one 1418-frame timeline (frames 0-1417). Shots are HARD
#   CUTS at the marker frames in SHOTS (end is exclusive).
# - Each shot builds its own SET under a parent empty at a distinct world
#   location (spread along X, 60 m apart) and the set is scale-hidden
#   outside its shot span (visible_span), so no set leaks into another
#   shot's frame. Cameras are NOT parented to sets.
# - Visibility is ROOT SCALE (0.001 = hidden), never hide_render.
#   Always key BOTH sides of a visibility change.
# - Lighting: one sun + world background, keyframed per shot by
#   build_all.py (key_lighting at every shot boundary).
# - Timing comes from voice/words.json via SHOT_PLAN.md — never by feel.
# - Humans are flat 2D Grease Pencil via shared/2d_rig.py (shot 12 only).
#   Worlds/scenery/objects are own-built 3D meshes.
import math

import bpy
from mathutils import Matrix, Vector

FRAME_END = 1418            # timeline is frames 0..1417
HIDDEN = 0.001              # root scale that reads as "not there"

# (shot number, start frame, end frame [exclusive], lighting preset)
SHOTS = [
    (1, 0, 135, "space"),
    (2, 135, 225, "dive"),
    (3, 225, 372, "map"),
    (4, 372, 480, "dark"),
    (5, 480, 555, "dark"),
    (6, 555, 641, "deep"),
    (7, 641, 720, "deep"),
    (8, 720, 810, "deep"),
    (9, 810, 969, "dark"),
    (10, 969, 1080, "dark"),
    (11, 1080, 1208, "deep"),
    (12, 1208, 1333, "bank"),
    (13, 1333, 1418, "dusk"),
]

# lighting presets (keyframed at every shot boundary by build_all.py)
SPACE = dict(sun_energy=4.0, sun_color=(1.0, 1.0, 1.0),
             sun_loc=(10, 12, 18), world_color="#050810",
             world_strength=0.4)
DIVE = dict(sun_energy=1.2, sun_color=(0.6, 0.8, 1.0),
            sun_loc=(6, 8, 20), world_color="#06283d",
            world_strength=0.8)
MAP = dict(sun_energy=2.0, sun_color=(0.75, 0.9, 1.0),
           sun_loc=(10, 10, 25), world_color="#0a2a44",
           world_strength=0.9)
DARK = dict(sun_energy=1.5, sun_color=(0.85, 0.95, 1.0),
            sun_loc=(8, 10, 15), world_color="#06121f",
            world_strength=0.6)
DEEP = dict(sun_energy=1.0, sun_color=(0.55, 0.75, 1.0),
            sun_loc=(6, 8, 18), world_color="#06283d",
            world_strength=0.8)
BANK = dict(sun_energy=3.0, sun_color=(1.0, 0.96, 0.88),
            sun_loc=(8, 12, 14), world_color="#dfe8f0",
            world_strength=1.0)
DUSK = dict(sun_energy=0.8, sun_color=(0.7, 0.8, 1.0),
            sun_loc=(-10, 12, 12), world_color="#1a2438",
            world_strength=0.6)
LIGHTING = {"space": SPACE, "dive": DIVE, "map": MAP, "dark": DARK,
            "deep": DEEP, "bank": BANK, "dusk": DUSK}


# ---------------------------------------------------------------- colour

def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hx(hexcol):
    """'#rrggbb' -> linear RGB tuple for Blender colour inputs."""
    h = hexcol.lstrip("#")
    return tuple(_srgb_to_linear(int(h[i:i + 2], 16) / 255.0)
                 for i in (0, 2, 4))


# ---------------------------------------------------------------- materials

_mat_cache = {}


def flat_mat(name, hexcol, roughness=0.92):
    """Flat Principled material (Eevee + Cycles safe). Cached by name."""
    if name in _mat_cache:
        return _mat_cache[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*hx(hexcol), 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Specular IOR Level"].default_value = 0.3
    mat.diffuse_color = (*hx(hexcol), 1.0)  # Workbench MATERIAL colour mode
    _mat_cache[name] = mat
    return mat


def emis_mat(name, hexcol, strength=2.0, base_hex=None, roughness=0.6):
    """Emissive Principled material (self-glow in Eevee; flat colour in
    Workbench via diffuse_color). Emission strength is keyframeable via
    emis_key(). Each call site should use a UNIQUE name if it animates
    the strength independently."""
    if name in _mat_cache:
        return _mat_cache[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (
        *hx(base_hex or hexcol), 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Emission Color"].default_value = (*hx(hexcol), 1.0)
    bsdf.inputs["Emission Strength"].default_value = strength
    mat.diffuse_color = (*hx(hexcol), 1.0)
    _mat_cache[name] = mat
    return mat


def emis_key(mat, frame, strength):
    """Keyframe a material's Principled emission strength at one frame."""
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission Strength"].default_value = strength
    bsdf.inputs["Emission Strength"].keyframe_insert(
        data_path="default_value", frame=frame)


# ---------------------------------------------------------------- keyframes

def kf(obj, frame, data_path="rotation_euler"):
    obj.keyframe_insert(data_path=data_path, frame=frame)


def set_linear(obj):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def set_linear_range(obj, f_min, f_max):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if f_min <= kp.co.x <= f_max:
                    kp.interpolation = "LINEAR"


def set_bezier_range(obj, f_min, f_max):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if f_min <= kp.co.x <= f_max:
                    kp.interpolation = "BEZIER"


def loc_key(obj, frame, loc):
    obj.location = loc
    kf(obj, frame, "location")


def rot_key(obj, frame, rot_deg):
    obj.rotation_euler = tuple(math.radians(a) for a in rot_deg)
    kf(obj, frame, "rotation_euler")


def scale_key(obj, frame, s):
    if isinstance(s, (int, float)):
        obj.scale = (s, s, s)
    else:
        obj.scale = s
    kf(obj, frame, "scale")


# ---------------------------------------------------------------- mesh utils

def _link(obj):
    bpy.context.collection.objects.link(obj)
    return obj


def _mesh_transform(obj, matrix):
    obj.data.transform(matrix)
    obj.data.update()


def bake_scale(obj, sx, sy, sz):
    _mesh_transform(obj, Matrix.Diagonal(Vector((sx, sy, sz, 1.0))))


def translate_mesh(obj, dx, dy, dz):
    _mesh_transform(obj, Matrix.Translation(Vector((dx, dy, dz))))


def shade(obj, smooth=True):
    for p in obj.data.polygons:
        p.use_smooth = smooth


def new_empty(name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "PLAIN_AXES"
    e.empty_display_size = 0.08
    _link(e)
    if parent is not None:
        e.parent = parent
    e.location = loc
    return e


def _finish(obj, mat, parent, loc, rot):
    if parent is not None:
        obj.parent = parent
    obj.location = loc
    obj.rotation_euler = rot
    if mat is not None:
        obj.data.materials.append(mat)
    return obj


def add_sphere(name, r, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0),
               scale=(1, 1, 1), seg=20, rings=14, smooth_shade=True):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=seg, ring_count=rings, radius=r, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    bake_scale(obj, *scale)
    shade(obj, smooth_shade)
    return _finish(obj, mat, parent, loc, rot)


def add_cylinder(name, r, depth, mat, parent=None, loc=(0, 0, 0),
                 rot=(0, 0, 0), verts=20, smooth_shade=True, r2=None):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=r, depth=depth, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    shade(obj, smooth_shade)
    return _finish(obj, mat, parent, loc, rot)


def add_cone(name, r1, r2, depth, mat, parent=None, loc=(0, 0, 0),
             rot=(0, 0, 0), verts=16):
    bpy.ops.mesh.primitive_cone_add(
        vertices=verts, radius1=r1, radius2=r2, depth=depth,
        location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    shade(obj, True)
    return _finish(obj, mat, parent, loc, rot)


def add_box(name, dims, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    bake_scale(obj, dims[0], dims[1], dims[2])
    shade(obj, False)
    return _finish(obj, mat, parent, loc, rot)


def add_plane(name, size, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    shade(obj, False)
    return _finish(obj, mat, parent, loc, rot)


def add_torus(name, major_r, minor_r, mat, parent=None, loc=(0, 0, 0),
              rot=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_r, minor_radius=minor_r,
        major_segments=28, minor_segments=10, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    bake_scale(obj, *scale)
    shade(obj, True)
    return _finish(obj, mat, parent, loc, rot)


def add_tube(name, points, radius, mat, parent=None, loc=(0, 0, 0),
             cyclic=False, resolution=12):
    """A smooth tube along `points` (list of (x, y, z)) as a beveled
    Bezier curve. Returns the curve object; draw-on animation via
    curve.data.bevel_factor_end (keyframeable)."""
    cu = bpy.data.curves.new(name + "_curve", type='CURVE')
    cu.dimensions = '3D'
    cu.resolution_u = resolution
    cu.bevel_depth = radius
    cu.bevel_resolution = 4
    spline = cu.splines.new('BEZIER')
    spline.bezier_points.add(len(points) - 1)
    for bp, pt in zip(spline.bezier_points, points):
        bp.co = pt
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    spline.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, cu)
    _link(obj)
    if parent is not None:
        obj.parent = parent
    obj.location = loc
    obj.data.materials.append(mat)
    return obj


def curve_point_at(curve_obj, t):
    """Evaluate a point on a Bezier curve object at parameter t (0..1).
    Uses the first spline; good enough for pulse paths."""
    import mathutils
    spline = curve_obj.data.splines[0]
    pts = spline.bezier_points
    n = len(pts) - 1
    if n < 1:
        return Vector(pts[0].co)
    # piecewise cubic Bezier over consecutive point pairs
    seg = min(n - 1, int(t * n))
    u = t * n - seg
    p0 = Vector(pts[seg].co)
    p1 = Vector(pts[seg].handle_right)
    p2 = Vector(pts[seg + 1].handle_left)
    p3 = Vector(pts[seg + 1].co)
    return ((1 - u) ** 3 * p0 + 3 * (1 - u) ** 2 * u * p1
            + 3 * (1 - u) * u ** 2 * p2 + u ** 3 * p3)


# ---------------------------------------------------------------- visibility

def scale_at(obj, frame, s):
    """Keyframe an object's scale (uniform) at one frame."""
    obj.scale = (s, s, s)
    kf(obj, frame, "scale")


def visible_span(obj, f_start, f_end, base=1.0, fade_in=0, fade_out=0):
    """Object visible (scale=base) between f_start and f_end inclusive,
    hidden (scale 0.001) outside. Keys both sides of every transition."""
    if f_start > 0:
        scale_at(obj, f_start - 1, HIDDEN)
    if fade_in > 0:
        scale_at(obj, f_start, HIDDEN)
        scale_at(obj, f_start + fade_in, base)
    else:
        scale_at(obj, f_start, base)
    if fade_out > 0:
        scale_at(obj, f_end - fade_out, base)
        scale_at(obj, f_end, HIDDEN)
    else:
        scale_at(obj, f_end, base)
    if f_end < FRAME_END - 1:
        scale_at(obj, f_end + 1, HIDDEN)


def set_origin_visible(obj, f_start, f_end):
    """Same as visible_span but keeps the object's own base scale
    (for objects built at non-unit scale)."""
    base = obj.scale.copy()
    if f_start > 0:
        obj.scale = (HIDDEN, HIDDEN, HIDDEN)
        kf(obj, f_start - 1, "scale")
    obj.scale = base
    kf(obj, f_start, "scale")
    obj.scale = base
    kf(obj, f_end, "scale")
    if f_end < FRAME_END - 1:
        obj.scale = (HIDDEN, HIDDEN, HIDDEN)
        kf(obj, f_end + 1, "scale")


# ---------------------------------------------------------------- camera

def _catmull_rom(p0, p1, p2, p3, u):
    return 0.5 * ((2 * p1) + (-p0 + p2) * u
                  + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                  + (-p0 + 3 * p1 - 3 * p2 + p3) * u * u * u)


def _sample_keys(pts, f):
    """Catmull-Rom sample of [(frame, Vector, lens)] at frame f."""
    if f <= pts[0][0]:
        return pts[0][1], pts[0][2]
    if f >= pts[-1][0]:
        return pts[-1][1], pts[-1][2]
    i = next(i for i in range(len(pts) - 1)
             if pts[i][0] <= f < pts[i + 1][0])
    u = (f - pts[i][0]) / (pts[i + 1][0] - pts[i][0])
    p0 = pts[max(0, i - 1)][1]
    p1 = pts[i][1]
    p2 = pts[i + 1][1]
    p3 = pts[min(len(pts) - 1, i + 2)][1]
    loc = _catmull_rom(p0, p1, p2, p3, u)
    lens = pts[i][2] + (pts[i + 1][2] - pts[i][2]) * u
    return loc, lens


def build_shot_camera(name, cam_keys, focus_keys, f_start, f_end,
                      sample=3):
    """Build one marker-bound shot camera.

    cam_keys: [(frame, (x, y, z), lens_mm)] — Catmull-Rom path.
    focus_keys: [(frame, (x, y, z))] — Track-To focus path.
    Keys cover [f_start, f_end]. Returns (camera object, focus empty).
    """
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = cam_keys[0][2]
    cam_data.sensor_fit = "VERTICAL"
    cam_data.sensor_width = 36
    cam_data.clip_start = 0.1
    cam_data.clip_end = 500
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    focus = new_empty(name + "_Focus", loc=focus_keys[0][1])
    con = cam.constraints.new(type="TRACK_TO")
    con.target = focus
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"

    pts = [(f, Vector(loc), lens) for f, loc, lens in cam_keys]
    fpts = [(f, Vector(loc), 0.0) for f, loc in focus_keys]
    for f in range(f_start, f_end + 1, sample):
        loc, lens = _sample_keys(pts, f)
        cam.location = loc
        kf(cam, f, "location")
        cam_data.lens = lens
        cam_data.keyframe_insert(data_path="lens", frame=f)
        floc, _ = _sample_keys(fpts, f)
        focus.location = floc
        kf(focus, f, "location")
    if (f_end - f_start) % sample:
        loc, lens = _sample_keys(pts, f_end)
        cam.location = loc
        kf(cam, f_end, "location")
        cam_data.lens = lens
        cam_data.keyframe_insert(data_path="lens", frame=f_end)
        floc, _ = _sample_keys(fpts, f_end)
        focus.location = floc
        kf(focus, f_end, "location")
    set_linear(cam)
    set_linear(focus)
    if cam_data.animation_data and cam_data.animation_data.action:
        for fc in cam_data.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    return cam, focus


def set_origin(obj, loc):
    """Set an object's origin (mesh offset) — used to pivot rotations
    around a chosen point (e.g. cable snap halves)."""
    translate_mesh(obj, -loc[0], -loc[1], -loc[2])
    obj.location = (obj.location.x + loc[0], obj.location.y + loc[1],
                    obj.location.z + loc[2])
