# SHOT_PLAN.md — V4 "Why Subsea Internet Cables Are Wrapped in Steel"

Voice: 47.256 s, frames 0–1417 (30 fps). Last word "disconnected" ends
47.04 s (f1411); fade-out sits INSIDE the final ~0.5 s (ffmpeg, from
46.756 s). All timings from `voice/words.json` (vosk, hand-fixed).

CORE RULE (user, non-negotiable): every phrase gets its own distinct
animated scene that LITERALLY ENACTS what the voice says at that exact
moment. Objects MOVE in sync with the words — never a static
establishing shot standing in for an action phrase. Camera movement in
every scene. No captions/text baked in.

Sets live at distinct world locations (spread along X) AND are
scale-hidden outside their shot span, so no set ever leaks into another
shot's frame. Lighting is keyframed per shot (sun + world background),
like the chicken build. All objects own-built in bpy — no downloads,
no template scenes. Humans (shot 12 only) are flat 2D Grease Pencil
via `shared/2d_rig.py` — never 3D figures.

## Shot table (13 shots, hard cuts at markers)

| # | Frames | Seconds | Words | Enacted action |
|---|---|---|---|---|
| 1 | 0–134 | 0.00–4.47 | "Ninety-nine percent of international internet traffic doesn't bounce through outer space—" | Satellite + signal arc BOUNCING off it, then arc FADING OUT / satellite dimming on "outer space" |
| 2 | 135–224 | 4.50–7.47 | "it's sitting in the mud at the bottom of the ocean." | Camera DIVES DOWN through the water column past fish to the muddy floor where the cable lies |
| 3 | 225–371 | 7.50–12.37 | "Stretched across ocean floors are hundreds of thousands of miles of subsea fiber cables." | World/ocean map; glowing cable lines STRETCH (draw on) across the seafloor between continents |
| 4 | 372–479 | 12.40–15.97 | "At their core, the glass fibers carrying global data" | Camera pushes INTO a cable cross-section; glowing fibers with data pulses RACING along them |
| 5 | 480–554 | 16.00–18.47 | "are barely thicker than a strand of hair." | A human hair SLIDES IN beside a glowing glass fiber — the fiber nearly as thin ("hair" f526–538) |
| 6 | 555–640 | 18.50–21.33 | "But out in the deep, they face crushing pressure," | Pressure arrows CLOSE IN from all sides; the cable SQUEEZES/flexes ("pressure" f621–638) |
| 7 | 641–719 | 21.37–23.97 | "shifting continental shelves," | Seafloor plates GRIND and SHIFT under the cable; the cable drags and bends |
| 8 | 720–809 | 24.00–26.97 | "and curious sharks that chew on electromagnetic fields." | Shark swims up and BITES the cable ("chew" f738–747); EM field rings SHIMMER around it |
| 9 | 810–968 | 27.00–32.27 | "To survive, that fragile fiber is wrapped in petroleum jelly, copper tubing," | Cross-section: jelly layer WRAPS ON (f899–930), then copper tubing WRAPS ON (f936–963), each with an orbiting wrap bead |
| 10 | 969–1079 | 32.30–35.97 | "high-tensile steel armor, and thick waterproof tar." | Steel armor wires WRAP ON (f970–1017), then thick tar WRAPS ON (f1034–1075); finished cable rotates |
| 11 | 1080–1207 | 36.00–40.23 | "If just three of these underwater lines snapped simultaneously," | THREE cables SNAP AT ONCE ("snapped" f1154–1165) — ends whip apart, sparks fly, data light leaks |
| 12 | 1208–1332 | 40.27–44.40 | "international banking and cloud infrastructure would freeze in seconds," | Bank screens + cloud icons: loading spinners HALT, screens FROST OVER ("freeze" f1281–1296); 2D clerk freezes mid-gesture |
| 13 | 1333–1417 | 44.43–47.26 | "leaving the modern world completely disconnected." | City lights / connected devices go DARK one by one ("disconnected" f1387–1411); world goes silent and dark |

## Phrase-by-phrase animation beats (frame-accurate)

### Shot 1 — Space (f0–134). Set at X=+0 (space set).
- f0–60: Earth below (big blue sphere, green continent blobs, cloud
  wisps), stars, satellite drifting slowly; camera slow push-in.
- f60–117: signal pulse (glowing sphere) travels ground station → satellite
  → back: the arc BOUNCES. Arc is a beveled curve; pulse rides a
  sampled path. Two bounces.
- f118–133 ("outer space", f118–133): the arc's emission fades to 0 and
  the satellite dims (emission down, slight scale settle) — the signal
  does NOT bounce through space. Camera keeps pushing; cut on the dim.

### Shot 2 — The dive (f135–224). Set at X=+60.
- f135–175: camera DIVES fast from the bright surface (light rays,
  bubbles rising) down through the water column; fish swim across the
  frame; light dims with depth (world/sun keyed darker across the shot).
- f165–175 ("mud"): the muddy floor comes into view; camera decelerates.
- f176–224: camera settles low over the mud; the black cable lies
  half-buried across the frame; a few bubbles rise; camera slow drift
  forward along the cable.

### Shot 3 — World cables (f225–371). Set at X=+120.
- Ocean map: dark-blue seafloor plane with stylised continents
  (flattened green/tan shapes) and glowing cable curves between them.
- f240–360: cable lines DRAW ON one by one (bevel_factor_end 0→1),
  staggered — the network STRETCHES across the ocean floors. Small
  glowing pulses travel along finished lines.
- Camera: slow orbit/pan over the map, descending slightly.

### Shot 4 — The core (f372–479). Set at X=+180.
- Cable end cross-section facing camera; camera pushes INTO the core.
- f385–430 ("their core"): outer layers peel back in scale (slight
  outward drift) as the camera closes in on the glowing fiber bundle.
- f430–479: data pulses (small bright spheres) RACE along the fibers
  toward camera; fibers glow cyan; camera slow rotation around the core.

### Shot 5 — Hair vs fiber (f480–554). Set at X=+240.
- Dark backdrop; the glowing glass fiber stands vertical, centre-right.
- f480–510: a human hair (brown wavy tube, slightly thicker) SLIDES IN
  from screen-left and settles beside the fiber.
- f510–538: both strands gently sway; the fiber pulses brighter on
  "hair" (f526–538) — the comparison lands: the fiber is barely thicker.
- Camera: slow push-in on the pair.

### Shot 6 — Crushing pressure (f555–640). Set at X=+300.
- Cable on the seafloor, camera low and close, slow push-in.
- f580–620: pressure arrows (cones) around the cable begin CLOSING IN.
- f621–638 ("pressure"): arrows press in hard; the cable SQUASHES
  (scale dips ~15% on Y/Z) and flexes, then partially rebounds;
  a faint creak shudder (tiny location jitter) at the squeeze peak.
- f639–640: hold on the squeezed cable; cut.

### Shot 7 — Shifting shelves (f641–719). Set at X=+360.
- Seafloor split into two plates with a visible fault crack; the cable
  drapes across the fault.
- f650–700: the left plate GRINDS sideways (slow translate + slight
  rotation); the cable bends/drags with it; small rock chips tumble.
- f700–719: the plate settles with a final jolt; the cable sags into
  the widened crack. Camera slow pan following the shift.

### Shot 8 — Shark bite (f720–809). Set at X=+420.
- Cable on the seafloor with EM field rings (glowing tori) SHIMMERING
  around it (scale pulse).
- f720–737 ("sharks"): shark swims in from screen-right, tail wagging,
  circling toward the cable; camera tracks it.
- f738–747 ("chew"): jaws OPEN, then CLOSE ON the cable — the bite.
  The cable jerks/shakes; EM rings flare bright, then flicker.
- f748–809: shark tugs (head shakes, cable flexes), then releases and
  swims off; rings settle back to a shimmer. Camera follows the shark
  out, then rests on the bitten cable.

### Shot 9 — Jelly + copper wrap (f810–968). Set at X=+480.
- Cable cross-section, end-on, camera slow push + slight orbit.
- f886–896 ("wrapped"): the fragile fiber bundle glows; a wrap bead
  begins orbiting.
- f899–930 ("petroleum jelly"): the jelly ring (pale yellow, slightly
  translucent look) WRAPS ON — scales in from 1.2→1.0 with a spin,
  bead orbiting once around it.
- f936–963 ("copper tubing"): the copper ring (orange metallic) WRAPS
  ON the same way, over the jelly.
- f964–968: brief hold on the two-layer cable; cut.

### Shot 10 — Steel + tar wrap (f969–1079). Set at X=+540.
- Same cross-section language, new camera angle (slightly lower, closer).
- f970–1017 ("high-tensile steel armor"): steel armor ring WRAPS ON —
  a grey ring plus visible armor-wire ridges (small tori) winding on.
- f1034–1075 ("thick waterproof tar"): the thick black tar outer ring
  WRAPS ON, sealing the cable.
- f1076–1079: the finished armored cable rotates slowly; camera pulls
  back a touch to show the complete cross-section; cut.

### Shot 11 — Three snaps (f1080–1207). Set at X=+600.
- Three parallel cables across the seafloor, camera slow push-in.
- f1111–1120 ("three"): a subtle highlight pulse runs along all three
  cables in turn (1-2-3).
- f1154–1165 ("snapped"): ALL THREE SNAP AT ONCE — each cable's two
  halves WHIP apart (fast rotation + translate), sparks (small emissive
  spheres) burst outward, severed fiber ends glow and leak light.
- f1166–1207 ("simultaneously"): halves settle, sparking fading; camera
  shake (small jitter) at the snap, then still; cut on the dead cables.

### Shot 12 — Freeze (f1208–1332). Set at X=+660.
- Bank interior: counter, wall screens, cloud icon cluster. One flat 2D
  human clerk (Grease Pencil, `2d_rig.py`) standing at the counter,
  facing camera (+Y), idle + head turn toward the screens.
- f1227–1241 ("banking"): screens show a spinning loader (orbiting
  bright dot) and rising bars; the clerk points at a screen.
- f1250–1280 ("cloud infrastructure"): the cloud icon's spinner also
  turns; data dots flow into the cloud.
- f1281–1296 ("freeze"): spinners HALT mid-rotation; frost planes
  (pale blue) SCALE IN over the screens; the clerk FREEZES mid-gesture
  (all animation keys stop — held pose).
- f1297–1332 ("in seconds"): frost spreads (second frost plane on the
  cloud icon); screens dim to grey; the clerk stays frozen; camera slow
  push-in; cut.

### Shot 13 — Dark world (f1333–1417). Set at X=+720.
- City skyline at dusk: 8 buildings with lit window grids, a few
  streetlights, a network-node sphere with glowing links.
- f1333–1386 ("leaving the modern world"): lights begin going out —
  buildings dim one by one (staggered emission keys), streetlights die.
- f1387–1411 ("disconnected"): the last windows go dark; the network
  sphere's links fade; the skyline is nearly black against a dim sky.
- f1412–1417: hold on the dark city; the ffmpeg fade-out (from 46.756 s)
  closes the video. Camera: slow pull-back/drift throughout.

## Lighting presets (sun + world, keyed at every shot boundary)

| Shot | Preset | World colour / strength | Sun energy / colour |
|---|---|---|---|
| 1 space | space | #050810 / 0.4 | 4.0 white |
| 2 dive | deep | #06283d / 0.8 → darker across shot | 1.2 bluish |
| 3 map | deep | #0a2a44 / 0.9 | 2.0 |
| 4 core | dark | #06121f / 0.6 | 1.5 |
| 5 hair | dark | #0a0a12 / 0.6 | 2.0 |
| 6 pressure | deep | #06283d / 0.8 | 1.0 |
| 7 shelves | deep | #06283d / 0.8 | 1.0 |
| 8 shark | deep | #06283d / 0.8 | 1.2 |
| 9 layers | dark | #0a1420 / 0.7 | 2.0 |
| 10 layers | dark | #0a1420 / 0.7 | 2.0 |
| 11 snap | deep | #06283d / 0.8 | 1.2 |
| 12 bank | bright | #dfe8f0 / 1.0 | 3.0 warm white |
| 13 city | dusk | #1a2438 / 0.6 | 0.8 cool |

## Test frames (one per shot, for the Colab notebook)

120, 190, 300, 430, 530, 630, 680, 745, 920, 1000, 1160, 1290, 1400
