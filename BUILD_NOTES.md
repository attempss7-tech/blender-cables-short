# BUILD_NOTES.md — V4 "Why Subsea Internet Cables Are Wrapped in Steel"

Blender + Eevee short for @ExplainerMaan. Built 2026-11-12. Colab render
pending (parent runs it — see `COLAB_RUN.md`).

## Facts

- **Script:** verbatim, 124 words (`../scripts/SCRIPT_04_cables.md`).
  Built as written. Flagged (not changed): "three lines snapped = banking
  freezes" is overstated (the network has redundancy) — the user was told
  and the build uses their wording.
- **Voice:** Warm Pebble (avocado_v2:chip, speed 112), 47.256 s, 48 kHz.
  Last word "disconnected" ends 47.04 s; trailing silence ~0.22 s.
  **Total frames: 1,418 (0–1417)**, 30 fps, 1080x1920, Eevee only.
- **Sound mix:** `assets/mix.wav` — voice (gain only) + original deep
  ambient score in D minor (low drone pads + sparse soft plucks, ducked
  −3 dB under speech) + synthesized SFX (sonar ping, dive whoosh,
  bubbles, pressure creak, rock grind, shark bite, 4 wrap ticks, triple
  snap, freeze shimmer, power-down). −14.5 LUFS integrated, −1.2 dBTP,
  exactly 47.256 s (2,268,288 samples). Built by `audio/build_mix.py`
  (dsp kit copied from the v3 chicken short). Cue sheet: `audio/cues.md`.
- **.blend:** `scenes/cables.blend` — 527 objects (415 meshes, 11 Grease
  Pencil, 22 curves), 25,574 polys, 192 actions, 13 cameras, frames
  0–1417, BLENDER_EEVEE_NEXT. Build takes ~15 s.
- **Reproducibility:** rebuilt from `scripts/build_all.py` from scratch —
  identical stats AND identical file size (8,161,032 bytes).
- **Repo:** https://github.com/attempss7-tech/blender-cables-short
- **Notebook:** `notebook/cables_colab.ipynb` (13 cells, 3 shards
  0–472 / 473–945 / 946–1417, EGL fix cell kept verbatim from the chicken
  notebook).

## Architecture

One scene, one 1,418-frame timeline. Each shot's set lives under a parent
empty at a distinct world X (0, 60, 120, …, 720); sets are scale-hidden
(0.001) outside their shot span, with keys on both sides of every
transition. One sun + world background, keyframed per shot (lighting
presets in `SHOT_PLAN.md`). Cameras are NOT parented to sets. 13 markers
bound to 13 cameras (Cam01–Cam13); camera paths are Catmull-Rom with
Track-To, copied from the chicken pattern. Every shot has camera movement.

Build scripts (`scripts/`): `common.py` (helpers), `shots_space.py`
(shots 1–3), `shots_core.py` (4–5), `shots_deep.py` (6–8),
`shots_layers.py` (9–10), `shots_end.py` (11–13), `build_all.py`
(markers + camera binding + lighting), `render_stills.py` (Workbench
stills), `colab_render.py` (copied from the chicken project).

## Per-phrase verdicts (all 13 shots verified in stills)

Stills: 34 Workbench stills at 540x960 in `out/stills/` (2–3 per shot,
at action beats) + 4 contact sheets. All viewed. Workbench cannot show
emission, so emission-driven animation was verified by keyframe data
against the .blend (see "Emission verification" below) — the Colab Eevee
test frames are the first real look at those.

| Shot | Frames | Phrase enacted | Still verdict |
|---|---|---|---|
| 1 Space | 0–134 | signal arc BOUNCES off satellite, then FADES OUT on "outer space" (f118–133) | Satellite + arc visible; arc fade verified by keys (2.5→0, f117–133), panels dim 1.2→0.15 |
| 2 Dive | 135–224 | camera DIVES DOWN through water column past fish to the muddy floor ("mud" f165–175) | Dive corridor + fish + mud floor all read; rays thinned and moved off-path |
| 3 Map | 225–371 | glowing cable lines STRETCH/draw on between continents | Draw-on verified by keys (bevel_factor_end staggered f240–360); map plane 60 m |
| 4 Core | 372–479 | camera pushes INTO the cable cross-section; data pulses RACE along glowing fibers | Pulses (r=0.11) visible racing along fibers |
| 5 Hair | 480–554 | human hair SLIDES IN beside glowing glass fiber ("hair" f526–538) | Two strands side by side, nearly same thinness; fiber pulse at f530 verified by keys |
| 6 Pressure | 555–640 | arrows CLOSE IN; cable SQUEEZES ("pressure" f621–638) | Arrows (upper hemisphere, stop 1.0 m out) + cable flex visible |
| 7 Shelves | 641–719 | seafloor plates GRIND/SHIFT under the cable | Plates shifted, crack open; moiré z-fight fixed (see below) |
| 8 Shark | 720–809 | shark swims up and BITES cable ("chew" f738–747); EM rings shimmer/flare | Shark (scale 0.55) + bite at x=1.6 visible; EM flare to 5.5 at f743 verified by keys |
| 9 Wrap I | 810–968 | jelly WRAPS ON (f899–930), copper WRAPS ON (f936–963), orbiting wrap beads | Rings with real holes + seam markers (spin visible); fiber glow-up at f890 verified |
| 10 Wrap II | 969–1079 | steel armor WRAPS ON (f970–1017), tar WRAPS ON (f1034–1075) | Steel + tar rings visible; cameras pulled back to fit |
| 11 Snap | 1080–1207 | THREE cables SNAP AT ONCE ("snapped" f1154–1165), ends whip apart, sparks | Three cables, ends whipped apart 25°/28°, overlap 0.15 m past centre pre-snap; highlight pulses f1111/1114/1117 verified |
| 12 Freeze | 1208–1332 | bank screens + cloud icons FREEZE ("freeze" f1281–1296) — spinners halt, frost scales in, 2D clerk freezes mid-point | Clerk upright, flat 2D, face visible, frozen mid-point at f1290/f1320; screens dim to 0.25 by f1310 verified |
| 13 Dark | 1333–1417 | city lights go out one by one ("disconnected" f1387–1411) | City reads; staggered light-off (f1344/1368/1400), nodes/links fade to 0 at f1411, verified by keys |

**2D human (mandatory rule):** the bank clerk in shot 12 is built with
the proven rig (`../shared/2d_rig.py` — 180° base yaw intact, placement
rotation Z = 3.142, Damped Track billboard on Cam12). He freezes
mid-point via manual `_rot` keys — the rig's `point()`/`head_turn()`
helpers lower the arm / return the head, so they can't hold a frozen
pose. He is the only human in the video.

**Emission verification** (programmatic, `/tmp/verify_keys.py` against
the .blend — Workbench can't show emission): S1_Arc 2.5→0 at f117–133;
S1_SatPanel 1.2→0.15; S8_EMRing flare to 5.5 at f743 with flicker;
S11_Cable0/1/2 highlight pulses at f1111/1114/1117; S12 screens dim to
0.25 by f1310; S13_Win0/3/7 staggered off at f1344/1368/1400;
S13_Node/Link fade to 0 at f1411; S13_LampM0 off at f1363; S9_Fiber
glow-up at f890; S5_Fiber pulse at f530; S3 cables bevel_factor_end
draw-on staggered f240–360. All 13 markers bound to the correct cameras.

## Decisions / fixes during the build

- **Moiré bug (shot 7):** a woven grid patch was z-fighting between the
  crack box's front/back faces (y=±3.5) and the plates' coplanar faces.
  Diagnosed by hide-and-render probes. Fix: crack box depth 7.0→6.9
  (front at y=3.45) and under-plane z −0.95→−1.0. Verified gone in f0660.
- **Layer rings:** given real holes (jelly 0.70/0.18, copper 1.05/0.18,
  steel 1.40/0.16, tar 1.72/0.20; fiber hex radius 0.36) + seam markers
  so the wrap spin is visible, not a static torus.
- **Snap halves:** overlap 0.15 m past centre (pivots ±0.1) so the cables
  read whole before the snap; whip reduced to 25°/28° so ends stay in
  frame.
- **Screen-left = world +X** for cameras at +Y looking toward −Y
  (camera-right ≈ world −X) — staging was mirrored against world coords.
- **In `shots_end.py`, `cm.emis_mat("S11_Cable%d")` is called twice for
  the same name** — the cache returns the same material, which is how the
  highlight pulse works (intentional, not a bug).
- **Mix OOM fix:** `dsp.widen()` takes MONO in — passing it a stereo
  array made `np.pad` explode to 9.6 GB. `build_mix.py` now widens the
  mono bed before stereo-izing.
- **Mix SFX levels:** events use the v3 rule (applied = naive − 6 dB);
  the ocean bed is integrated loudness, not reduced.

## Timings (measured)

- .blend build from scripts: ~15 s (local).
- Workbench stills: ~0.7–2.4 s each locally (540x960).
- Mix build: ~24 s (local).
- Colab render: unmeasured — budget 1–3 s/frame on a T4 (8–25 min per
  shard, ~30–45 min total), re-estimate from the test-frames timings.

## Colab watch-list

- **Emission actions are unseen until the Eevee test frames** — arc fade,
  satellite dim, EM flare, screen dimming, city lights going out. If any
  reads wrong, fix the keys in the scripts, rebuild, re-test.
- **Deep shots (f630–f745) may read too dark** — the notebook has a fix
  cell (world strength + sun energy ×1.5) for exactly this.
- **EGL fix is mandatory** — if a render runs at minutes/frame, the
  vendor file is missing; re-run the install cell.
- Fade-out starts at 46.756 s (assembly cell) — inside the final voice,
  never over dead silence. Voice is present under the fade zone
  (46.756–47.04 s, rms 0.039 in the mix).

## Known limits

- The shark is a stylised low-poly build (cones + spheres), not a
  realistic shark — reads clearly at shot distance.
- The hair-vs-fiber shot has no scale label (no baked-in text) — the
  comparison reads from the two strands side by side.
- The 2D clerk appears only in shot 12; he holds one frozen pose.
- No captions/text baked in — captions are a separate overlay step.
- Workbench stills were the only local visual check (no local GPU);
  Eevee test frames in Colab are the authoritative look check.
