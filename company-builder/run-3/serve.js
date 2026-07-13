/* WideTally local server — serves this folder. Run: node serve.js  → http://localhost:8130 */
const http = require("http"), fs = require("fs"), path = require("path");
const ROOT = __dirname, PORT = process.env.PORT || 8130;
const MIME = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".csv": "text/csv", ".png": "image/png", ".mp4": "video/mp4", ".txt": "text/plain", ".md": "text/plain; charset=utf-8", ".wav": "audio/wav", ".webm": "video/webm", ".json": "application/json" };
http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p === "/") p = "/RECAP.html";
  if (p.endsWith("/")) p += "index.html";
  const f = path.normalize(path.join(ROOT, p));
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, d) => {
    if (e) { res.writeHead(404, { "Content-Type": "text/plain" }); return res.end("404 " + p); }
    res.writeHead(200, { "Content-Type": MIME[path.extname(f).toLowerCase()] || "application/octet-stream" });
    res.end(d);
  });
}).listen(PORT, () => console.log(`WideTally local server → http://localhost:${PORT}\n  product demo: http://localhost:${PORT}/product/\n  landing page: http://localhost:${PORT}/site/`));
