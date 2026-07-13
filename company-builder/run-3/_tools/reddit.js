/* Minimal old.reddit.com research fetcher (read-only, HTML parsing — JSON endpoints are blocked here).
   Usage:
     node reddit.js search <subreddit> "<query>" [t]   — top results (t=year|all)
     node reddit.js thread <old.reddit thread url> [max]
*/
const { execFileSync } = require("child_process");
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36";
const get = url => execFileSync("curl", ["-s", "-m", "40", "-A", UA, url], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
const strip = h => h.replace(/<[^>]+>/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&#39;|&#x27;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, " ").trim();

const mode = process.argv[2];
if (mode === "search") {
  const [sub, q, t] = process.argv.slice(3);
  const html = get(`https://old.reddit.com/r/${sub}/search/?q=${encodeURIComponent(q)}&restrict_sr=on&sort=top&t=${t || "year"}`);
  const results = html.split(/class="[^"]*\bsearch-result-link\b[^"]*"/).slice(1);
  if (!results.length) console.log("(no results or blocked; page len " + html.length + ")");
  for (const r of results.slice(0, 15)) {
    const title = (r.match(/search-title[^>]*>(.*?)<\/a>/s) || [])[1];
    const href = (r.match(/href="(https:\/\/old\.reddit\.com\/r\/[^"]+comments[^"]+)"/) || [])[1];
    const pts = (r.match(/search-score[^>]*>([^<]+)/) || [])[1];
    const cmts = (r.match(/search-comments[^>]*>([^<]+)/) || [])[1];
    const when = (r.match(/datetime="([^"T]+)/) || [])[1];
    if (title && href) console.log(`[${pts || "?"} | ${cmts || "?"} | ${when || "?"}] ${strip(title)}\n  ${href}`);
  }
} else if (mode === "thread") {
  const url = process.argv[3];
  const max = +(process.argv[4] || 14);
  const html = get(url);
  const t = html.match(/<title>([^<]+)<\/title>/);
  console.log("PAGE: " + (t ? strip(t[1]) : "?") + "\nURL: " + url + "\n");
  // the post body is the first usertext-body inside the expando / self text
  const things = html.split(/<div class="[^"]*\bthing\b[^"]*"/).slice(1);
  let n = 0;
  for (const th of things) {
    if (n > max) break;
    const author = (th.match(/class="author[^"]*"[^>]*>([^<]+)/) || [])[1];
    const score = (th.match(/class="score unvoted"[^>]*title="(\d+)"/) || th.match(/(\d+) points?/) || [])[1];
    const when = (th.match(/datetime="([^"T]+)/) || [])[1];
    const body = (th.match(/<div class="md">([\s\S]*?)<\/div>\s*<\/div>/) || [])[1];
    if (!author || !body) continue;
    n++;
    console.log(`u/${author} (${score || "?"}pts, ${when || "?"}): ${strip(body).slice(0, 650)}\n`);
  }
}
