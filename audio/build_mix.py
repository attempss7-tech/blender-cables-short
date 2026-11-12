# build_mix.py — soundtrack for V4 "Why Subsea Internet Cables Are Wrapped
# in Steel" (47.256 s, 48 kHz stereo, -14.5 LUFS).
#
# Voice = voice/voice.wav (Warm Pebble, gain only). Music = original deep
# ambient score in D minor (low drone pads + sparse soft plucks), ducked
# -3 dB under speech keyed from words.json. SFX = synthesized in
# numpy/scipy (sonar ping, dive whoosh, bubbles, pressure creak, rock
# grind, shark bite, wrap ticks, triple snap, freeze shimmer, power-down).
# Master: own 4x-oversampled look-ahead limiter, ceiling -1.2 dBTP.
# Writes ../assets/mix.wav + cues.md. Run from this directory:
#   python3 build_mix.py
import json
import os
import subprocess
import sys
import time

import numpy as np
from scipy import ndimage, signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsp import (SR, ns, tt, dbg, rng, lp, hp, bp, colored, smooth_noise,
                 ramp, fades, curve, modal, pan, st, place, widen,
                 integrated, momentary, lra, true_peak, read_wav, write_wav)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DUR = 47.256
N = ns(DUR)                      # 2,268,288 samples
TARGET_LUFS = -14.5
CEIL_DBTP = -1.2
DUCK_DB = -3.0

# story sections (name, start, end, music LU under the voice)
SECTIONS = [
    ("space", 0.00, 4.50, -10.0),
    ("dive", 4.50, 7.50, -10.0),
    ("map", 7.50, 12.40, -10.0),
    ("core", 12.40, 16.00, -10.5),
    ("hair", 16.00, 18.50, -11.0),
    ("threats", 18.50, 27.00, -9.5),
    ("layers", 27.00, 36.00, -10.0),
    ("snap", 36.00, 40.30, -9.5),
    ("freeze", 40.30, 44.40, -11.0),
    ("dark", 44.40, 47.256, -12.0),
]

# music rides (start, end, dB): keep quiet sentence-final words on top
DIPS = [(46.20, 47.10, -3.0)]    # "disconnected" lands clean, bed dies out


def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)


# ================================================================ voice
def load_voice():
    x, sr = read_wav(os.path.join(ROOT, "voice", "voice.wav"))
    assert sr == SR, sr
    v = x[0] if x.shape[0] == 1 else x.mean(0)
    out = np.zeros(N)
    out[: min(N, len(v))] = v[:N]
    return st(out)


def speech_spans(words, merge=0.3):
    sp = []
    for w in words:
        s, e = float(w["s"]), float(w["e"])
        if sp and s - sp[-1][1] < merge:
            sp[-1][1] = max(sp[-1][1], e)
        else:
            sp.append([s, e])
    return sp


def duck_db(spans, depth=DUCK_DB, pre=0.08, post=0.12, att=0.07, rel=0.45):
    ctrl = 1000
    nc = int(DUR * ctrl) + 2
    va = np.zeros(nc)
    for s, e in spans:
        va[max(0, int((s - pre) * ctrl)): int((e + post) * ctrl)] = 1.0
    ka, kr = 1 - np.exp(-1 / (att * ctrl)), 1 - np.exp(-1 / (rel * ctrl))
    env = np.zeros(nc)
    e = 0.0
    for i in range(nc):
        tgt = va[i]
        e += (tgt - e) * (ka if tgt > e else kr)
        env[i] = e
    return np.interp(np.arange(N) / SR, np.arange(nc) / ctrl, depth * env)


# ================================================================ music
def pad_chord(freqs, t0, t1, gain=1.0, detune_cents=6.0, lp_f=900.0):
    """Slow-attack additive pad over [t0, t1). Returns mono."""
    n0, n1 = ns(t0), ns(t1)
    n = n1 - n0
    t = np.arange(n) / SR
    x = np.zeros(n)
    r = rng(7)
    for f in freqs:
        for dc in (-detune_cents, detune_cents):
            ff = f * 2 ** (dc / 1200.0)
            ph = r.uniform(0, 2 * np.pi)
            x += np.sin(2 * np.pi * ff * t + ph) / len(freqs)
    # slow attack (1.2 s) + release (1.2 s), gentle swell in the middle
    env = np.ones(n)
    a, rel = ns(1.2), ns(1.2)
    env[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
    env[-rel:] = 0.5 + 0.5 * np.cos(np.pi * np.arange(rel) / rel)
    env *= 0.85 + 0.15 * np.sin(np.pi * np.arange(n) / n)
    x = lp(x * env * gain, lp_f)
    return x


def pluck(freq, dur=1.6, gain=1.0):
    """Soft decaying pluck (sine partials)."""
    t = tt(dur)
    x = np.zeros_like(t)
    for h, a in ((1, 1.0), (2, 0.4), (3, 0.18), (4, 0.08)):
        x += a * np.sin(2 * np.pi * freq * h * t)
    x *= np.exp(-3.0 * t) * (1 - np.exp(-t * 300))
    return x * gain


def build_music():
    m = np.zeros(N)
    # chord map: (t0, t1, [freqs]) — D minor, deep register
    D2, F2, A2 = 73.42, 87.31, 110.00
    Bb1, C3, D3, F3, A3 = 58.27, 130.81, 146.83, 174.61, 220.00
    chords = [
        (0.0, 12.4, [D2, A2, D3]),        # space/dive/map: open Dm
        (12.4, 18.5, [D2, F2, A2]),       # core/hair: Dm, lower
        (18.5, 27.0, [Bb1, D2, F2]),      # threats: dark Bb shift
        (27.0, 36.0, [D2, A2, F3]),       # layers: Dm returns, brighter
        (36.0, 40.3, [D2, Bb1, C3]),      # snap: tense, dissonant low
        (40.3, 47.256, [D2, A2]),         # freeze/dark: bare, dying out
    ]
    for t0, t1, freqs in chords:
        seg = pad_chord(freqs, t0, t1, gain=0.5)
        m[ns(t0):ns(t1)] += seg
    # sparse pluck motif at phrase starts (D minor pentatonic)
    D4, F4, A4, C5, E4, G4 = 293.66, 349.23, 440.00, 523.25, 329.63, 392.00
    motif = [(0.6, D4), (5.0, A4), (7.6, F4), (12.9, D4), (16.1, E4),
             (19.0, C5), (24.1, A4), (27.3, D4), (30.0, F4), (31.3, A4),
             (33.2, C5), (34.9, A4), (40.4, G4), (44.5, F4)]
    for t, f in motif:
        p = pluck(f, dur=1.8, gain=0.35)
        n0 = ns(t)
        m[n0:n0 + len(p)] += p[:N - n0]
    # gentle low pulse under the threats + snap sections (soft heartbeat)
    for t in np.arange(18.6, 40.0, 1.0):
        n0 = ns(t)
        pulse = np.sin(2 * np.pi * 55 * tt(0.25)) * np.exp(-tt(0.25) * 18)
        m[n0:n0 + len(pulse)] += pulse * 0.25
    # fade the bed out with the world going dark
    m[ns(46.0):] *= np.linspace(1, 0, N - ns(46.0))
    # widen() takes MONO in and returns stereo — never pass it stereo
    # (np.pad on a (2, N) array explodes it to (2+d, N+d) = 9.6 GB)
    return widen(m, rng(3), ms=9.0, amount=0.4)


# ================================================================ sfx
def sine_blip(freq, dur, gain=1.0, glide_to=None):
    t = tt(dur)
    if glide_to:
        f = np.linspace(freq, glide_to, len(t))
        ph = 2 * np.pi * np.cumsum(f) / SR
    else:
        ph = 2 * np.pi * freq * t
    return np.sin(ph) * np.exp(-3.5 * t / dur * 2) * gain


def noise_burst(dur, lo, hi, gain=1.0, decay=6.0):
    r = rng(int(dur * 1e6) % 9973 + 11)
    n = ns(dur)
    x = r.standard_normal(n)
    x = bp(x, lo, hi)
    x *= np.exp(-decay * np.arange(n) / SR)
    return x * gain


def build_sfx(v_ref):
    """Returns (stereo sfx stem, cue list). Levels are LU vs the voice
    stem (naive), reduced by 6 dB for events (v3 mix rule)."""
    s = np.zeros((2, N))
    C = []

    def ev(t, name, desc, mono, naive_lu, pan_=0.0, kind="event"):
        applied = naive_lu - 6.0 if kind == "event" else naive_lu
        # scale the event so its max momentary loudness is applied LU
        # below the voice integrated level (approx via peak matching)
        target_peak = dbg(v_ref + applied - 3.0)  # rough peak proxy
        pk = np.abs(mono).max() + 1e-12
        g = target_peak / pk
        x = pan(mono * g, pan_)
        place(s, x, t)
        C.append(dict(t=t, name=name, desc=desc, naive=naive_lu,
                      applied=applied, kind=kind, p=pan_))
        return x

    # ocean bed: very low brown noise for the whole video
    r = rng(99)
    bed = colored(N, r, slope=1.0, lo=20.0)
    bed = lp(bed, 220.0)
    bed /= np.abs(bed).max() + 1e-12
    bed *= dbg(-30.0)  # ~-30 LU under the voice (integrated bed)
    s += st(bed) * 0.5
    C.append(dict(t=0.0, name="amb_ocean", kind="bed",
                  desc="deep underwater ambience for the whole video",
                  naive=-30, applied=-30.0, p=0.0))

    # sonar ping on "outer space" (3.96s)
    ping = sine_blip(880, 0.9, 1.0)
    ping2 = sine_blip(880, 0.9, 0.4)
    ev(3.96, "sonar", "sonar ping as the signal fails in space", ping,
       -12, 0.1)
    place(s, pan(ping2 * 0.4, 0.1), 4.45)

    # dive whoosh (4.83-7.0s): noise sweep down
    n = ns(2.2)
    r2 = rng(5)
    whoosh = r2.standard_normal(n)
    whoosh = bp(whoosh, 150, 900)
    whoosh *= np.sin(np.pi * np.arange(n) / n) ** 1.5
    ev(4.83, "dive_whoosh", "camera dives through the water column",
       whoosh, -14, 0.0)

    # bubbles rising (5.5-7.0s): short rising blips
    for i, bt in enumerate((5.5, 5.8, 6.15, 6.5, 6.8)):
        b = sine_blip(500 + i * 160, 0.25, 1.0, glide_to=900 + i * 160)
        ev(bt, "bubble", f"bubble {i + 1} rising past the camera", b,
           -20, -0.3 + i * 0.15)

    # pressure creak (20.73s): low groan
    creak = sine_blip(55, 0.9, 1.0, glide_to=38)
    creak += noise_burst(0.9, 40, 200, 0.5, decay=2.0)
    ev(20.73, "creak", "cable groans under crushing pressure", creak,
       -13, 0.0)

    # rock grind (21.5-23.0s): low rumble
    grind = noise_burst(1.5, 30, 160, 1.0, decay=0.8)
    ev(21.5, "grind", "continental shelf grinds sideways", grind, -15, 0.0)

    # shark bite (24.6s): thump + crunch
    bite = sine_blip(60, 0.35, 1.0)
    bite += noise_burst(0.35, 600, 2400, 0.7, decay=14.0)
    ev(24.6, "bite", "shark jaws close on the cable", bite, -9, 0.0)

    # wrap ticks, one per layer (jelly 30.0, copper 31.4, steel 33.3, tar 35.0)
    for t, name, f0 in ((30.0, "wrap_jelly", 1200),
                        (31.4, "wrap_copper", 1600),
                        (33.3, "wrap_steel", 2200),
                        (35.0, "wrap_tar", 500)):
        tick = sine_blip(f0, 0.18, 1.0)
        tick += noise_burst(0.18, f0 // 2, f0 * 2, 0.4, decay=20.0)
        ev(t, name, f"{name.split('_')[1]} layer wraps on", tick,
           -16, -0.1 + 0.07 * f0 / 1000)

    # triple snap (38.55/38.62/38.69s): three sharp cracks
    for i, st_ in enumerate((38.55, 38.62, 38.69)):
        crack = noise_burst(0.22, 1200, 6000, 1.0, decay=18.0)
        crack += sine_blip(180, 0.22, 0.5)
        ev(st_, "snap", f"underwater line {i + 1} of 3 snaps", crack,
           -8, -0.3 + i * 0.3)

    # freeze shimmer (42.8s): descending glassy pings + cold drone
    for i, (ft, ff) in enumerate(((42.8, 1568), (43.05, 1319),
                                  (43.3, 1047), (43.55, 880))):
        p = sine_blip(ff, 0.5, 1.0)
        ev(ft, "freeze_ping", f"freeze shimmer {i + 1}", p, -15,
           -0.2 + i * 0.15)
    drone = sine_blip(220, 1.6, 0.5, glide_to=110)
    ev(42.8, "freeze_drone", "cold drone as everything freezes", drone,
       -18, 0.0)

    # power-down (46.0-47.2s): descending sweep into silence
    pd = sine_blip(300, 1.2, 1.0, glide_to=45)
    pd *= np.linspace(1, 0, len(pd)) ** 1.5
    ev(46.0, "power_down", "the modern world powers down", pd, -13, 0.0)

    return s, C


# ================================================================ limiter
def limiter(x, ceil_db=CEIL_DBTP, look=0.003, rel=0.08):
    c = dbg(ceil_db)
    n = x.shape[1]
    up = np.abs(signal.resample_poly(x, 4, 1, axis=-1)).max(0)
    pk = np.pad(up, (0, max(0, 4 * n - len(up))))[: 4 * n].reshape(n, 4).max(1)
    gr = np.minimum(1.0, c / np.maximum(pk, 1e-12))
    La = max(1, ns(look))
    g1 = ndimage.minimum_filter1d(gr, 2 * La + 1, mode="nearest")
    g2 = g1.copy()
    idx = np.flatnonzero(g1 < 1.0)
    if len(idx):
        kr = 1 - np.exp(-1 / (rel * SR))
        gap = ns(rel * 8)
        brk = np.flatnonzero(np.diff(idx) > gap)
        starts = np.concatenate([[idx[0]], idx[brk + 1]])
        ends = np.concatenate([idx[brk], [idx[-1]]])
        for a, b_ in zip(starts, ends):
            e = min(n, b_ + gap)
            seg = g1[a:e]
            out = np.empty(len(seg))
            g = 1.0
            for k in range(len(seg)):
                g = min(seg[k], g + (1 - g) * kr)
                out[k] = g
            g2[a:e] = out
    g3 = ndimage.uniform_filter1d(g2, 2 * La + 1, mode="nearest")
    g3 = np.minimum(g3, 1.0)
    return x * g3[None, :], g3


# ================================================================ main
def section_db(m_ducked, v):
    gains = {}
    for name, a, b, tgt in SECTIONS:
        seg = slice(ns(a), ns(b))
        Lm, Lv = integrated(m_ducked[:, seg]), integrated(v[:, seg])
        gains[name] = (Lv + tgt - Lm) if np.isfinite(Lm) else 0.0
    pts = [(a, gains[name]) for name, a, b, _ in SECTIONS]
    curve_db = np.zeros(N)
    t = np.arange(N) / SR
    for a, g in pts:
        curve_db[t >= a] = g
    curve_db = ndimage.uniform_filter1d(curve_db, ns(0.4), mode="nearest")
    for a, b, db in DIPS:
        d = np.zeros(N)
        d[ns(a): ns(b)] = db
        curve_db += ndimage.uniform_filter1d(d, ns(0.06), mode="nearest")
    return curve_db, gains


def ffmpeg_ebur(path):
    try:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i",
                            path, "-af", "ebur128=peak=true", "-f",
                            "null", "-"], capture_output=True, text=True,
                           timeout=300)
        txt = r.stderr
        i = txt.rfind("Summary:")
        if i < 0:
            return txt[-1500:]
        out = []
        for line in txt[i:].splitlines():
            out.append(line.rstrip())
            if line.strip().startswith("Peak:"):
                break
        return chr(10).join(l for l in out if l)
    except Exception as e:  # noqa
        return f"ffmpeg check failed: {e}"


def lufs(x):
    v = integrated(x)
    return v if np.isfinite(v) else -99.0


def main():
    t_start = time.time()
    words = json.load(open(os.path.join(ROOT, "voice", "words.json")))
    spans = speech_spans(words)
    v = load_voice()
    v_ref = integrated(v)
    log(f"voice: {v_ref:.2f} LUFS, TP {true_peak(v):.2f} dBTP")

    m_raw = build_music()
    log("music rendered", f"{lufs(m_raw):.2f} LUFS raw")
    dk = duck_db(spans)
    m_d = m_raw * dbg(dk)[None, :]
    sec_curve, sec_gains = section_db(m_d, v)
    m = m_d * dbg(sec_curve)[None, :]
    end = ns(DUR - 0.03)
    m[:, end:] *= np.linspace(1, 0, N - end)[None, :]

    s_st, C = build_sfx(v_ref)
    log("sfx rendered", f"{lufs(s_st):.2f} LUFS")

    mix0 = v + m + s_st
    G = TARGET_LUFS - lufs(mix0)
    for it in range(5):
        y, g3 = limiter(mix0 * dbg(G))
        L = lufs(y)
        log(f"master iter {it}: gain {G:+.2f} dB -> {L:.2f} LUFS, "
            f"TP {true_peak(y):.2f} dBTP, "
            f"max GR {-20 * np.log10(g3.min()):.2f} dB")
        if abs(L - TARGET_LUFS) < 0.02:
            break
        G += TARGET_LUFS - L
    y = fades(y, 0.0, 0.03)
    assert y.shape == (2, N), y.shape
    out_path = os.path.join(ROOT, "assets", "mix.wav")
    write_wav(out_path, y)
    log("wrote", out_path)

    I, TP, LRA = lufs(y), true_peak(y), lra(y)
    Mmax = float(np.max(momentary(y)))
    grdb = -20 * np.log10(g3)
    gr_stats = dict(max=float(grdb.max()),
                    pct_over_0_1=float((grdb > 0.1).mean() * 100),
                    pct_over_0_5=float((grdb > 0.5).mean() * 100))
    eb = ffmpeg_ebur(out_path)
    log(f"final: {I:.2f} LUFS, TP {TP:.2f} dBTP, LRA {LRA:.2f} LU, "
        f"max momentary {Mmax:.1f}")
    print(eb)

    # cues.md
    L = []
    w = L.append
    w("# Subsea Cables — soundtrack cue sheet")
    w("")
    w("All sound is original: synthesized in numpy/scipy by `build_mix.py` "
      "(dsp kit from the v3 chicken short).")
    w("Voice = `voice/voice.wav` (Warm Pebble), gain only.")
    w("")
    w("## Files")
    w("| file | content |")
    w("|---|---|")
    w(f"| `assets/mix.wav` | final mix, 48 kHz, stereo, 24-bit, "
      f"{N:,} samples = {DUR} s |")
    w("")
    w("## Master loudness (own BS.1770-4 meter)")
    w(f"- Integrated **{I:.1f} LUFS**, true peak **{TP:.1f} dBTP**, "
      f"LRA {LRA:.1f} LU, max momentary {Mmax:.1f} LUFS")
    w(f"- Stems: voice {lufs(v * dbg(G)):.1f} LUFS, "
      f"music {lufs(m * dbg(G)):.1f} LUFS, sfx {lufs(s_st * dbg(G)):.1f} "
      f"LUFS (master gain {G:+.2f} dB)")
    w(f"- Master limiter (4x oversampled look-ahead, ceiling {CEIL_DBTP} "
      f"dBTP): max gain reduction {gr_stats['max']:.2f} dB, active "
      f"(>0.1 dB) on {gr_stats['pct_over_0_1']:.2f} % of samples")
    w("")
    w("ffmpeg ebur128 cross-check:")
    w("```")
    w(eb)
    w("```")
    w("")
    w("## Music map (original deep ambient score, D minor)")
    w("Music target per section, LU under the voice (after a -3 dB speech "
      "duck keyed from words.json): " +
      ", ".join(f"{n} {t:+.1f}" for n, _, _, t in SECTIONS) +
      ". Applied section gains (dB): " +
      ", ".join(f"{k} {v_:+.1f}" for k, v_ in sec_gains.items()) + ".")
    w("")
    w("| section | time s | music |")
    w("|---|---|---|")
    w("| space | 0.00-4.50 | open Dm pad (D2/A2/D3) + pluck motif |")
    w("| dive | 4.50-7.50 | Dm pad continues, whoosh + bubbles |")
    w("| map | 7.50-12.40 | Dm pad, plucks at phrase starts |")
    w("| core/hair | 12.40-18.50 | lower Dm pad, sparse plucks |")
    w("| threats | 18.50-27.00 | dark Bb shift + low pulse |")
    w("| layers | 27.00-36.00 | Dm returns brighter, wrap ticks |")
    w("| snap | 36.00-40.30 | tense low cluster + heartbeat pulse |")
    w("| freeze | 40.30-44.40 | bare Dm, cold shimmer |")
    w("| dark | 44.40-47.26 | bed fades out with the lights |")
    w("")
    w("## SFX events")
    w("Level convention: every EVENT has a naive level (LU vs the voice "
      "stem); applied = naive - 6 dB (standard mix rule). BEDS are "
      "integrated loudness, not reduced.")
    w("")
    w("| # | time s | frame | cue | what | naive LU | applied LU | pan |")
    w("|---|---|---|---|---|---|---|---|")
    for i, c in enumerate(sorted(C, key=lambda c: (c["t"], c["name"]))):
        kind = " (bed, integrated)" if c["kind"] == "bed" else ""
        w(f"| {i + 1} | {c['t']:.3f} | {c['t'] * 30:.1f} | "
          f"{c['name']}{kind} | {c['desc']} | {c['naive']:+.0f} | "
          f"{c['applied']:+.1f} | {c['p']:+.2f} |")
    w("")
    open(os.path.join(HERE, "cues.md"), "w", encoding="utf-8").write(
        "\n".join(L))
    log(f"done in {time.time() - t_start:.0f} s")


if __name__ == "__main__":
    main()
