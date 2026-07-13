/* Tiny static file server for the DueCrew demo + landing page.
   Usage: node server.js [port]   (root = run-2)
     http://localhost:8231/product/  -> app demo
     http://localhost:8231/site/     -> landing page */
const http = require("http");
const fs = require("fs");
const path = require("path");

const port = Number(process.argv[2]) || 8231;
const root = path.resolve(__dirname, "..", "..");
const MIME = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml",
  ".png": "image/png", ".json": "application/json", ".webm": "video/webm",
  ".mp4": "video/mp4", ".wav": "audio/wav", ".md": "text/plain; charset=utf-8"
};
http.createServer((req, res) => {
  try {
    let p = decodeURIComponent(req.url.split("?")[0]);
    if (p.endsWith("/")) p += "index.html";
    const f = path.normalize(path.join(root, p));
    if (!f.startsWith(root)) { res.writeHead(403); return res.end("Forbidden"); }
    fs.readFile(f, (e, d) => {
      if (e) { res.writeHead(404); return res.end("Not found: " + p); }
      res.writeHead(200, { "Content-Type": MIME[path.extname(f).toLowerCase()] || "application/octet-stream" });
      res.end(d);
    });
  } catch { res.writeHead(500); res.end("Server error"); }
}).listen(port, () => {
  console.log(`DueCrew demo server at http://localhost:${port}/  (root: ${root})`);
  console.log(`  Product demo: http://localhost:${port}/product/`);
  console.log(`  Landing page: http://localhost:${port}/site/`);
});
