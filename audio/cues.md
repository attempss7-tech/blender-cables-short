# Subsea Cables — soundtrack cue sheet

All sound is original: synthesized in numpy/scipy by `build_mix.py` (dsp kit from the v3 chicken short).
Voice = `voice/voice.wav` (Warm Pebble), gain only.

## Files
| file | content |
|---|---|
| `assets/mix.wav` | final mix, 48 kHz, stereo, 24-bit, 2,268,288 samples = 47.256 s |

## Master loudness (own BS.1770-4 meter)
- Integrated **-14.5 LUFS**, true peak **-1.2 dBTP**, LRA 2.1 LU, max momentary -9.7 LUFS
- Stems: voice -14.6 LUFS, music -24.8 LUFS, sfx -36.1 LUFS (master gain +7.42 dB)
- Master limiter (4x oversampled look-ahead, ceiling -1.2 dBTP): max gain reduction 3.75 dB, active (>0.1 dB) on 8.33 % of samples

ffmpeg ebur128 cross-check:
```
Summary:
  Integrated loudness:
    I:         -14.5 LUFS
    Threshold: -24.8 LUFS
  Loudness range:
    LRA:         2.1 LU
    Threshold: -34.8 LUFS
    LRA low:   -16.0 LUFS
    LRA high:  -13.9 LUFS
  True peak:
    Peak:       -1.2 dBFS
```

## Music map (original deep ambient score, D minor)
Music target per section, LU under the voice (after a -3 dB speech duck keyed from words.json): space -10.0, dive -10.0, map -10.0, core -10.5, hair -11.0, threats -9.5, layers -10.0, snap -9.5, freeze -11.0, dark -12.0. Applied section gains (dB): space -18.0, dive -19.6, map -18.7, core -18.6, hair -19.4, threats -17.3, layers -18.4, snap -16.2, freeze -20.7, dark -20.6.

| section | time s | music |
|---|---|---|
| space | 0.00-4.50 | open Dm pad (D2/A2/D3) + pluck motif |
| dive | 4.50-7.50 | Dm pad continues, whoosh + bubbles |
| map | 7.50-12.40 | Dm pad, plucks at phrase starts |
| core/hair | 12.40-18.50 | lower Dm pad, sparse plucks |
| threats | 18.50-27.00 | dark Bb shift + low pulse |
| layers | 27.00-36.00 | Dm returns brighter, wrap ticks |
| snap | 36.00-40.30 | tense low cluster + heartbeat pulse |
| freeze | 40.30-44.40 | bare Dm, cold shimmer |
| dark | 44.40-47.26 | bed fades out with the lights |

## SFX events
Level convention: every EVENT has a naive level (LU vs the voice stem); applied = naive - 6 dB (standard mix rule). BEDS are integrated loudness, not reduced.

| # | time s | frame | cue | what | naive LU | applied LU | pan |
|---|---|---|---|---|---|---|---|
| 1 | 0.000 | 0.0 | amb_ocean (bed, integrated) | deep underwater ambience for the whole video | -30 | -30.0 | +0.00 |
| 2 | 3.960 | 118.8 | sonar | sonar ping as the signal fails in space | -12 | -18.0 | +0.10 |
| 3 | 4.830 | 144.9 | dive_whoosh | camera dives through the water column | -14 | -20.0 | +0.00 |
| 4 | 5.500 | 165.0 | bubble | bubble 1 rising past the camera | -20 | -26.0 | -0.30 |
| 5 | 5.800 | 174.0 | bubble | bubble 2 rising past the camera | -20 | -26.0 | -0.15 |
| 6 | 6.150 | 184.5 | bubble | bubble 3 rising past the camera | -20 | -26.0 | +0.00 |
| 7 | 6.500 | 195.0 | bubble | bubble 4 rising past the camera | -20 | -26.0 | +0.15 |
| 8 | 6.800 | 204.0 | bubble | bubble 5 rising past the camera | -20 | -26.0 | +0.30 |
| 9 | 20.730 | 621.9 | creak | cable groans under crushing pressure | -13 | -19.0 | +0.00 |
| 10 | 21.500 | 645.0 | grind | continental shelf grinds sideways | -15 | -21.0 | +0.00 |
| 11 | 24.600 | 738.0 | bite | shark jaws close on the cable | -9 | -15.0 | +0.00 |
| 12 | 30.000 | 900.0 | wrap_jelly | jelly layer wraps on | -16 | -22.0 | -0.02 |
| 13 | 31.400 | 942.0 | wrap_copper | copper layer wraps on | -16 | -22.0 | +0.01 |
| 14 | 33.300 | 999.0 | wrap_steel | steel layer wraps on | -16 | -22.0 | +0.05 |
| 15 | 35.000 | 1050.0 | wrap_tar | tar layer wraps on | -16 | -22.0 | -0.07 |
| 16 | 38.550 | 1156.5 | snap | underwater line 1 of 3 snaps | -8 | -14.0 | -0.30 |
| 17 | 38.620 | 1158.6 | snap | underwater line 2 of 3 snaps | -8 | -14.0 | +0.00 |
| 18 | 38.690 | 1160.7 | snap | underwater line 3 of 3 snaps | -8 | -14.0 | +0.30 |
| 19 | 42.800 | 1284.0 | freeze_drone | cold drone as everything freezes | -18 | -24.0 | +0.00 |
| 20 | 42.800 | 1284.0 | freeze_ping | freeze shimmer 1 | -15 | -21.0 | -0.20 |
| 21 | 43.050 | 1291.5 | freeze_ping | freeze shimmer 2 | -15 | -21.0 | -0.05 |
| 22 | 43.300 | 1299.0 | freeze_ping | freeze shimmer 3 | -15 | -21.0 | +0.10 |
| 23 | 43.550 | 1306.5 | freeze_ping | freeze shimmer 4 | -15 | -21.0 | +0.25 |
| 24 | 46.000 | 1380.0 | power_down | the modern world powers down | -13 | -19.0 | +0.00 |
