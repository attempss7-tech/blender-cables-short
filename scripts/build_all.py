# build_all.py — master build for the V4 subsea-cables Blender short.
#
# Builds all 13 shots in ONE scene on ONE 1418-frame timeline, each shot
# with its own set at a distinct world location (spread along X, 60 m
# apart), scale-hidden outside its shot span; 13 marker-bound cameras,
# sun + world lighting keyframed per shot.
# Saves scenes/cables.blend (BLENDER_EEVEE_NEXT, 1080x1920, 30 fps,
# frames 0-1417).
#
# Run from ~/workspace/blender_shorts_4/v4_cables:
#   ~/workspace/blender_chicken/tools/blender-4.2.23-linux-x64/blender \
#       --background --python scripts/build_all.py
import os
import sys
import time

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common as cm  # noqa: E402
import shots_space  # noqa: E402
import shots_core  # noqa: E402
import shots_deep  # noqa: E402
import shots_layers  # noqa: E402
import shots_end  # noqa: E402

MODULES = [shots_space, shots_core, shots_deep, shots_layers, shots_end]


def build_lights():
    """One sun (keyframed per shot) + the world background."""
    bpy.ops.object.light_add(type='SUN', location=(10, 12, 18))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 3.0
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    bpy.context.scene.world = world
    return sun, world


def key_lighting(sun, world, frame, preset):
    """Keyframe the full lighting state (sun, world) at one frame."""
    p = cm.LIGHTING[preset]
    sun.location = p["sun_loc"]
    sun.rotation_euler = (Vector((0, -3, 0)) - Vector(p["sun_loc"])
                          ).to_track_quat("-Z", "Y").to_euler()
    cm.kf(sun, frame, "location")
    cm.kf(sun, frame)
    sun.data.energy = p["sun_energy"]
    sun.data.keyframe_insert(data_path="energy", frame=frame)
    sun.data.color = p["sun_color"]
    sun.data.keyframe_insert(data_path="color", frame=frame)
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*cm.hx(p["world_color"]), 1.0)
    bg.inputs["Color"].keyframe_insert(data_path="default_value",
                                       frame=frame)
    bg.inputs["Strength"].default_value = p["world_strength"]
    bg.inputs["Strength"].keyframe_insert(data_path="default_value",
                                          frame=frame)


def main():
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)

    sun, world = build_lights()
    ctx = dict(sun=sun, world=world)

    # ---- lighting: key each shot's preset at its first AND last frame
    # so the light holds steady inside a shot and only changes across
    # the 1-frame hard cut between shots. (Shot 2 adds its own mid-shot
    # world-strength keys for the dive darkening.)
    for _num, start, end, preset in cm.SHOTS:
        key_lighting(sun, world, start, preset)
        key_lighting(sun, world, end - 1, preset)

    # ---- the 13 shots, in timeline order
    cameras = []  # (marker frame, camera object)
    for mod in MODULES:
        ts = time.time()
        info = mod.build(ctx)
        cameras.extend(info["cameras"])
        print("  %s built in %.1fs (%d cameras)"
              % (mod.__name__, time.time() - ts, len(info["cameras"])))

    # ---- markers + camera binding (hard cuts)
    scene = bpy.context.scene
    for frame, cam in sorted(cameras):
        m = scene.timeline_markers.new(name="Shot_%04d" % frame,
                                       frame=frame)
        m.camera = cam
    scene.camera = sorted(cameras)[0][1]

    # ---- scene settings (final: 1080x1920, 30 fps, Eevee on Colab GPU)
    scene.frame_start = 0
    scene.frame_end = 1417
    scene.render.fps = 30
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.image_settings.file_format = "PNG"

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.normpath(os.path.join(here, "..", "scenes",
                                        "cables.blend"))
    bpy.ops.wm.save_as_mainfile(filepath=out)

    n_mesh = sum(1 for o in scene.objects if o.type == "MESH")
    n_gp = sum(1 for o in scene.objects if o.type == "GPENCIL")
    n_cur = sum(1 for o in scene.objects if o.type == "CURVE")
    n_all = len(scene.objects)
    n_poly = sum(len(o.data.polygons) for o in scene.objects
                 if o.type == "MESH")
    n_actions = len(bpy.data.actions)
    print("BUILD ALL OK in %.1fs: %d objects (%d meshes, %d GP, "
          "%d curves), %d polys, %d actions, %d cameras, frames 0-1417"
          % (time.time() - t0, n_all, n_mesh, n_gp, n_cur, n_poly,
             n_actions, len(cameras)))
    print("saved:", out)


if __name__ == "__main__":
    main()
