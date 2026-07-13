/* Ambient pad for WideTally videos: Dm9 / Bbmaj9 slow crossfade, gentle detune+tremolo, 75s.
   (Synthesis approach follows the local-tooling pattern from run-1/_tools, reused as engineering
   plumbing; chord content and envelope are this run's own.) Output: video/assets/music.wav */
const fs = require("fs"), path = require("path");
const SR = 44100, DUR = 75, N = SR * DUR;
const CHORDS = [
  [73.42, 110.0, 146.83, 174.61, 220.0, 261.63],  // D2 A2 D3 F3 A3 C4 (Dm add-ish)
  [58.27, 87.31, 116.54, 146.83, 174.61, 220.0]   // Bb1 F2 Bb2 D3 F3 A3 (Bbmaj9)
];
const SEG = 11;
const buf = new Float64Array(N);
for (let i = 0; i < N; i++) {
  const t = i / SR, seg = Math.floor(t / SEG), frac = (t % SEG) / SEG;
  let w = 1;
  if (frac > 0.68) { const x = (frac - 0.68) / 0.32; w = Math.cos(x * Math.PI / 2) ** 2; }
  const cur = CHORDS[seg % 2], nxt = CHORDS[(seg + 1) % 2];
  let s = 0;
  for (let k = 0; k < cur.length; k++) {
    const amp = 0.024 * (1 - k * 0.11);
    s += w * amp * (Math.sin(2 * Math.PI * cur[k] * t) + 0.55 * Math.sin(2 * Math.PI * cur[k] * 1.004 * t));
    s += (1 - w) * amp * (Math.sin(2 * Math.PI * nxt[k] * t) + 0.55 * Math.sin(2 * Math.PI * nxt[k] * 1.004 * t));
  }
  s *= 1 + 0.10 * Math.sin(2 * Math.PI * 0.075 * t);
  s *= 1 + 0.07 * Math.sin(2 * Math.PI * 0.019 * t + 0.9);
  if (t < 4) s *= t / 4;
  if (t > DUR - 6) s *= (DUR - t) / 6;
  buf[i] = s;
}
let peak = 0; for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(buf[i]));
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
console.log("Wrote", out);
