/* Synthesize a low ambient bed for the DueCrew videos: two alternating chords
   (E minor add9 -> C major add9), softly detuned sines with a slow pulse.
   Distinct composition from run-1's generator (different chords, tempo, envelope).
   Output: run-2/video/assets/music.wav (44.1kHz 16-bit mono, 100s). */
const fs = require("fs");
const path = require("path");

const SR = 44100, DUR = 100, N = SR * DUR;
const CHORDS = [
  [82.41, 123.47, 164.81, 185.00, 246.94],  // E2 B2 E3 F#3 B3  (Em add9 flavor)
  [65.41, 130.81, 164.81, 196.00, 293.66]   // C2 C3 E3 G3 D4   (Cmaj add9)
];
const SEG = 12; // seconds per chord

const buf = new Float64Array(N);
for (let i = 0; i < N; i++) {
  const t = i / SR;
  const seg = Math.floor(t / SEG);
  const frac = (t % SEG) / SEG;
  let w = 1;
  if (frac > 0.65) { const x = (frac - 0.65) / 0.35; w = Math.cos(x * Math.PI / 2) ** 2; }
  const cur = CHORDS[seg % 2], nxt = CHORDS[(seg + 1) % 2];

  let s = 0;
  for (let k = 0; k < cur.length; k++) {
    const amp = 0.024 * (1 - k * 0.1);
    s += w * amp * (Math.sin(2 * Math.PI * cur[k] * t) + 0.5 * Math.sin(2 * Math.PI * cur[k] * 1.004 * t));
    s += (1 - w) * amp * (Math.sin(2 * Math.PI * nxt[k] * t) + 0.5 * Math.sin(2 * Math.PI * nxt[k] * 1.004 * t));
  }
  // slow pulse (like a watch tick smoothed out) + long swell
  s *= 1 + 0.10 * Math.sin(2 * Math.PI * 0.125 * t);
  s *= 1 + 0.07 * Math.sin(2 * Math.PI * 0.019 * t + 0.6);
  if (t < 3.5) s *= t / 3.5;
  if (t > DUR - 6) s *= (DUR - t) / 6;
  buf[i] = s;
}

let peak = 0;
for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(buf[i]));
const gain = 0.25 / peak;

const pcm = Buffer.alloc(44 + N * 2);
pcm.write("RIFF", 0); pcm.writeUInt32LE(36 + N * 2, 4); pcm.write("WAVE", 8);
pcm.write("fmt ", 12); pcm.writeUInt32LE(16, 16); pcm.writeUInt16LE(1, 20);
pcm.writeUInt16LE(1, 22); pcm.writeUInt32LE(SR, 24); pcm.writeUInt32LE(SR * 2, 28);
pcm.writeUInt16LE(2, 32); pcm.writeUInt16LE(16, 34);
pcm.write("data", 36); pcm.writeUInt32LE(N * 2, 40);
for (let i = 0; i < N; i++) pcm.writeInt16LE(Math.round(buf[i] * gain * 32767), 44 + i * 2);

const out = path.resolve(__dirname, "..", "..", "video", "assets", "music.wav");
fs.writeFileSync(out, pcm);
console.log("Wrote", out, (pcm.length / 1048576).toFixed(1) + " MB");
