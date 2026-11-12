# Running the V4 subsea cables short on Colab

The project is built and validated locally. The Colab GPU does the Eevee
render only. The notebook is `notebook/cables_colab.ipynb`.

## Click-path

1. Open https://colab.research.google.com.
2. **File > Open notebook > GitHub tab** — paste
   `attempss7-tech/blender-cables-short`, open
   `notebook/cables_colab.ipynb`. (Or upload the `.ipynb` file
   directly: File > Upload notebook.)
3. **Runtime > Change runtime type > T4 GPU > Save.** The notebook fails
   fast with a clear message if no GPU is attached — do not render on CPU
   (Eevee falls back to software rendering, far too slow).
4. Run the cells **top to bottom, in order**. Do not use "Run all" blindly:
   you must STOP after the Eevee test-frames cell and inspect the 13 frames
   before running any shard cell.
5. The first cell mounts Google Drive — click through the auth prompt.
   Frames go to `MyDrive/cables_blender/frames/`, test frames to
   `MyDrive/cables_blender/test_frames/`, the final video to
   `MyDrive/cables_blender/final/`.

## The mandatory stop: Eevee test frames

**EGL fix (proven 2026-11-12, baked into the install cell):** Colab
ships the NVIDIA EGL library (`/usr/lib64-nvidia/libEGL_nvidia.so.0`) but
no vendor file for it, so Blender's EGL context fails (`EGL_BAD_MATCH`)
and Eevee silently falls back to CPU rendering at ~5 min/frame. The
install cell writes `/usr/share/glvnd/egl_vendor.d/10_nvidia.json`
before any render; with it, Eevee uses the T4 at ~3.5 s/frame (measured
2026-11-12 on the chicken short: 13 test frames in 45 s). The vendor file
lives only in the live session — after a session drop, re-running the
install cell re-creates it. If a render ever runs at minutes-per-frame,
the vendor file is missing: stop, re-run the install cell, re-run the
render.

Eevee was never validated locally (no GPU there). The test-frames cell
renders 13 frames, one per shot, and displays them inline. Check every one
for its phrase's enacted action:

- **f120** satellite + signal arc fading out (dim, almost gone) — "outer space"
- **f190** camera diving through the water column past fish toward the mud
- **f300** glowing cable lines stretched across the ocean floor map
- **f430** data pulses racing along glowing fibers inside the cable core
- **f530** human hair beside the glowing glass fiber, nearly the same thinness
- **f630** pressure arrows closing in, cable squeezed — "crushing pressure"
- **f680** seafloor plates shifted apart, crack open under the cable
- **f745** shark biting the cable, EM rings flaring around the bite
- **f920** jelly layer wrapped on, copper wrapping on — rings visible on the cable
- **f1000** steel armor wrapping on (tar comes after)
- **f1160** three cables snapped at once, ends whipped apart, sparks
- **f1290** bank screens + cloud icons freezing, frost on the screens,
  2D clerk frozen mid-point
- **f1400** city going dark — most lights out, a few still on

**If the deep shots (f630–f745) look too DARK:** run the FIX cell (raises
world strength + sun energy by 1.5x), then re-run the test-frames cell.
**If all 13 look right:** skip the fix cell and run the 3 shard cells.

## Shards (frames 0–1417 in 3 × 473)

- Shard 1: 0–472 · Shard 2: 473–945 · Shard 3: 946–1417.
- Each shard renders in 5 batches of 95 frames and copies each batch to
  Drive immediately. Per-frame timings print as it goes; each shard ends
  with a count check against Drive.
- Expected speed is unmeasured until the first test frame — budget roughly
  1–3 s/frame on a T4 (8–25 min per shard) and re-estimate from the
  test-frames timings.

## If a session drops mid-shard

Colab sessions reset/disconnect (12 h cap, ~90 min idle, GPU preemption).
Nothing is lost beyond the in-progress batch (~5 min of rendering):

1. Reopen the notebook (same file, same account).
2. Re-run the setup cells in order: mount Drive + GPU check, install
   Blender + libs, clone repo (or pull).
3. Re-run the interrupted shard cell. It first syncs that shard's finished
   frames from Drive back to local disk, then renders only the missing
   frames, batch by batch.
4. Continue with the remaining shard cells, then assembly.

Do NOT re-run the test-frames cell unless you changed something — the test
frames are already on Drive.

## Assembly + verification

The assembly cell checks all 1,418 frames are on Drive (and stops, listing
any missing frames, if not), then runs ffmpeg: PNG sequence → h264 mp4
(crf 17), fade-in 0.5 s + fade-out 0.5 s from 46.756 s (inside the final
voice — the last word ends at 47.04 s, so the fade never runs over dead
silence), muxed with the sound mix (`assets/mix.wav`, already −14.5 LUFS).
The verification cell prints ffprobe details + an ebur128 loudness reading.

Expected final: `cables_short.mp4`, ~47.26 s, 1080x1920, 30 fps,
h264 + AAC, ~−14.5 LUFS.

## If the committed .blend fails

The last markdown cell has the rebuild command: it re-runs
`scripts/build_all.py` in Colab (~15 s) to regenerate
`scenes/cables.blend` from the scripts, then re-run the
test-frames cell. The rebuild is deterministic — the same stats every time
(527 objects, 415 meshes, 11 Grease Pencil, 22 curves, 25,574 polys,
192 actions, 13 cameras).

## Known limits (from BUILD_NOTES.md)

- Emission-driven animation (arc fade, satellite dim, city lights going
  out, screen dimming, EM flare) was verified by keyframe data only — the
  Colab Eevee test frames are the first real look at these.
- The shark is a stylised low-poly build (cones + spheres), not a
  realistic shark — reads clearly at shot distance.
- The hair-vs-fiber shot has no scale label (no baked-in text) — the
  comparison reads from the two strands side by side.
- The 2D clerk appears only in shot 12 (f1208–1332); he freezes mid-point
  and holds the pose — no other humans in the video.
- No captions/text are baked in — captions are a separate overlay step.
