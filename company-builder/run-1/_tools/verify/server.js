/* Tiny static file server for the ReconStock demo + landing page.
   Usage: node server.js [port] [rootDir]
   Defaults: port 8123, root = ../../ (run-1), so:
     http://localhost:8123/product/  -> app demo
     http://localhost:8123/site/     -> landing page
*/
const http = require("http");
const fs = require("fs");
const path = require("path");

const port = Number(process.argv[2]) || 8123;
const root = path.resolve(process.argv[3] || path.join(__dirname, "..", ".."));

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".json": "application/json",
  ".csv": "text/csv"
};

const server = http.createServer((req, res) => {
  try {
    let urlPath = decodeURIComponent(req.url.split("?")[0]);
    if (urlPath.endsWith("/")) urlPath += "index.html";
    const filePath = path.normalize(path.join(root, urlPath));
    if (!filePath.startsWith(root)) { res.writeHead(403); res.end("Forbidden"); return; }
    fs.readFile(filePath, (err, data) => {
      if (err) { res.writeHead(404); res.end("Not found: " + urlPath); return; }
      res.writeHead(200, { "Content-Type": MIME[path.extname(filePath).toLowerCase()] || "application/octet-stream" });
      res.end(data);
    });
  } catch (e) {
    res.writeHead(500); res.end("Server error");
  }
});

server.listen(port, () => {
  console.log(`ReconStock demo server running at http://localhost:${port}/  (root: ${root})`);
  console.log(`  Product demo: http://localhost:${port}/product/`);
  console.log(`  Landing page: http://localhost:${port}/site/`);
});
