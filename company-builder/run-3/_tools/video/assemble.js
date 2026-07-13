/* Assemble launch.mp4 (~53s) and founder.mp4 (~62s) from clips + audio.
   ffmpeg-static; durations parsed from `ffmpeg -i` (no ffprobe).
   Run from run-3/_tools:  node video/assemble.js  */
const { spawnSync } = require("child_process");
const path = require("path"), fs = require("fs");
const FFMPEG = require("ffmpeg-static");
const ROOT = path.resolve(__dirname, "..", "..");
const A = p => path.join(ROOT, "video", "assets", p);
const OUT = p => path.join(ROOT, "video", p);

function run(args, label) {
  const r = spawnSync(FFMPEG, args, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) { console.error(r.stderr.slice(-3000)); throw new Error(label + " failed"); }
  return r.stderr;
}
function probe(file) {
  const r = spawnSync(FFMPEG, ["-i", file], { encoding: "utf8" });
  const m = (r.stderr || "").match(/Duration: (\d+):(\d+):(\d+\.\d+)/);
  if (!m) throw new Error("no duration for " + file);
  return { dur: (+m[1]) * 3600 + (+m[2]) * 60 + (+m[3]), streams: ((r.stderr || "").match(/Stream #[^\n]+/g) || []).map(s => s.trim()) };
}
function assemble(outFile, segments, audioInputs, audioFilter, totalDur) {
  const args = ["-y"];
  segments.forEach(s => args.push("-i", s.file));
  audioInputs.forEach(f => args.push("-i", f));
  const n = segments.length;
  let fc = "";
  segments.forEach((s, i) => {
    const pad = s.srcDur && s.dur > s.srcDur - 0.2
      ? `,tpad=stop_mode=clone:stop_duration=${(s.dur - (s.srcDur - 0.2)).toFixed(3)}` : "";
    const trimDur = s.srcDur ? Math.min(s.dur, s.srcDur - 0.2) : s.dur;
    fc += `[${i}:v]trim=duration=${trimDur.toFixed(3)},setpts=PTS-STARTPTS,fps=30,scale=1280:720,setsar=1${pad}[v${i}];`;
  });
  fc += segments.map((_, i) => `[v${i}]`).join("") + `concat=n=${n}:v=1:a=0[v];`;
  fc += audioFilter(n);
  args.push("-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", totalDur.toFixed(3),
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", outFile);
  run(args, path.basename(outFile));
}

(function main() {
  const d = {};
  for (const c of ["ui-imports", "ui-ledger", "ui-books", "ui-ads", "ui-founder"]) d[c] = probe(A(path.join("clips", c + ".webm"))).dur;
  const voDur = probe(A("vo-founder.wav")).dur;
  console.log("clips:", JSON.stringify(d), "vo:", voDur.toFixed(1) + "s");

  // ---------- launch.mp4 ----------
  const segs1 = [
    { file: A("clips/card-hook.webm"), dur: 5.0 },
    { file: A("clips/ui-imports.webm"), dur: d["ui-imports"] - 0.1 },
    { file: A("clips/ui-ledger.webm"), dur: d["ui-ledger"] - 0.1 },
    { file: A("clips/card-noapi.webm"), dur: 5.5 },
    { file: A("clips/ui-books.webm"), dur: d["ui-books"] - 0.1 },
    { file: A("clips/ui-ads.webm"), dur: d["ui-ads"] - 0.1 },
    { file: A("clips/card-pricing.webm"), dur: 5.5 },
    { file: A("clips/card-close.webm"), dur: 5.5 }
  ];
  const t1 = segs1.reduce((s, x) => s + x.dur, 0);
  assemble(OUT("launch.mp4"), segs1, [A("music.wav")],
    n => `[${n}:a]aresample=44100,volume=0.9,atrim=duration=${t1.toFixed(3)},afade=t=in:d=1.5,afade=t=out:st=${(t1 - 4).toFixed(3)}:d=4[a]`, t1);
  console.log("launch.mp4 target", t1.toFixed(1) + "s");

  // ---------- founder.mp4 ----------
  const uiDur = d["ui-founder"] - 0.1;
  const total2 = voDur + 3.0;
  const closeSrc = probe(A("clips/card-close.webm")).dur;
  const privacyDur = 6.5;
  const logoDur = 5.0;
  const closeDur = Math.max(4.5, total2 - (logoDur + uiDur + privacyDur));
  const segs2 = [
    { file: A("clips/card-logo.webm"), dur: logoDur },
    { file: A("clips/ui-founder.webm"), dur: uiDur },
    { file: A("clips/card-privacy.webm"), dur: privacyDur },
    { file: A("clips/card-close.webm"), dur: closeDur, srcDur: closeSrc }
  ];
  const t2 = segs2.reduce((s, x) => s + x.dur, 0);
  assemble(OUT("founder.mp4"), segs2, [A("vo-founder.wav"), A("music.wav")],
    n => `[${n}:a]aresample=44100,adelay=900|900,apad[vo];` +
      `[${n + 1}:a]aresample=44100,volume=0.10,atrim=duration=${t2.toFixed(3)},afade=t=in:d=2,afade=t=out:st=${(t2 - 5).toFixed(3)}:d=5[mu];` +
      `[mu][vo]amix=inputs=2:duration=first:normalize=0[a]`, t2);
  console.log("founder.mp4 target", t2.toFixed(1) + "s");

  // ---------- verify: duration, streams, null-decode ----------
  for (const f of ["launch.mp4", "founder.mp4"]) {
    const p = probe(OUT(f));
    console.log(`\n${f}: ${p.dur.toFixed(2)}s, ${(fs.statSync(OUT(f)).size / 1048576).toFixed(2)} MB`);
    p.streams.forEach(s => console.log("  " + s));
    run(["-v", "error", "-i", OUT(f), "-f", "null", "-"], f + " decode check");
    console.log("  decode check: OK");
  }
  // frame extraction for visual inspection
  const FR = path.join(ROOT, "record", "video-frames"); fs.mkdirSync(FR, { recursive: true });
  for (const [f, times] of [["launch.mp4", [2, 9, 20, 31, 44, 50]], ["founder.mp4", [2, 12, 25, 40, 52, 60]]]) {
    for (const t of times) {
      run(["-y", "-ss", String(t), "-i", OUT(f), "-frames:v", "1", path.join(FR, `${f.replace(".mp4", "")}-${t}s.png`)], "frame");
    }
  }
  console.log("frames extracted to record/video-frames");
})();
