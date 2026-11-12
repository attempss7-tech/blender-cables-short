# V4 — Why Subsea Internet Cables Are Wrapped in Steel

Blender + Eevee short for @ExplainerMaan. 47.256 s, 1080x1920, 30 fps,
1,418 frames. Scripted geometry (bpy) — every object own-built, no
downloaded models, no template scenes. One flat 2D bank clerk (proven
2D rig), everything else 3D.

- **Render:** `notebook/cables_colab.ipynb` on a Colab T4 GPU (3 shards).
  Click-path + session-drop recovery: `COLAB_RUN.md`.
- **Build record:** `BUILD_NOTES.md`. Phrase-by-phrase shot plan:
  `SHOT_PLAN.md`.
- **Voice:** Warm Pebble, 47.256 s (`voice/` is local only — the repo
  carries `assets/words.json` + `assets/mix.wav`).
- **Sound mix:** `assets/mix.wav`, −14.5 LUFS, built by
  `audio/build_mix.py` (cue sheet: `audio/cues.md`).
- **Rebuild the .blend from scripts** (~15 s, deterministic):
  `blender --background --python scripts/build_all.py`
