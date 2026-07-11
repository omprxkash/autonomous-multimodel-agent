/* Synthesize a subtle ambient pad: two soft chords (A add9 / D add9) slowly
   crossfading, gently detuned sines, slow tremolo, 70s, fade in/out.
   Output: run-1/video/assets/music.wav (44.1kHz 16-bit mono). */
const fs = require("fs");
const path = require("path");

const SR = 44100, DUR = 70, N = SR * DUR;
const CHORDS = [
  [110.0, 164.81, 220.0, 246.94, 277.18],   // A2 E3 A3 B3 C#4  (A add9)
  [98.0, 146.83, 196.0, 220.0, 293.66]      // G2 D3 G3 A3 D4   (G add9-ish)
];
const SEG = 10; // seconds per chord before crossfade

const buf = new Float64Array(N);
for (let i = 0; i < N; i++) {
  const t = i / SR;
  const seg = Math.floor(t / SEG);
  const frac = (t % SEG) / SEG;
  // crossfade over the final 30% of each segment
  let w = 1;
  if (frac > 0.7) { const x = (frac - 0.7) / 0.3; w = Math.cos(x * Math.PI / 2) ** 2; }
  const cur = CHORDS[seg % 2], nxt = CHORDS[(seg + 1) % 2];

  let s = 0;
  for (let k = 0; k < cur.length; k++) {
    const amp = 0.026 * (1 - k * 0.12); // lower partials louder
    s += w * amp * (Math.sin(2 * Math.PI * cur[k] * t) + 0.6 * Math.sin(2 * Math.PI * cur[k] * 1.0035 * t));
    s += (1 - w) * amp * (Math.sin(2 * Math.PI * nxt[k] * t) + 0.6 * Math.sin(2 * Math.PI * nxt[k] * 1.0035 * t));
  }
  // slow tremolo + very slow swell
  s *= 1 + 0.12 * Math.sin(2 * Math.PI * 0.09 * t);
  s *= 1 + 0.08 * Math.sin(2 * Math.PI * 0.023 * t + 1.3);
  // global fades: 4s in, 6s out
  if (t < 4) s *= t / 4;
  if (t > DUR - 6) s *= (DUR - t) / 6;
  buf[i] = s;
}

// normalize to -12 dBFS peak (bed stays subtle; final level set in ffmpeg mix)
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
