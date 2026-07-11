// Render brand/logo.svg to PNG at required favicon/app-icon sizes.
const sharp = require("./node_modules/sharp");
const path = require("path");
const fs = require("fs");

const src = "d:/AI/Business/run-1/brand/logo.svg";
const outDir = "d:/AI/Business/run-1/brand/exports";
fs.mkdirSync(outDir, { recursive: true });

const sizes = [32, 180, 512, 1024];

(async () => {
  for (const w of sizes) {
    const out = path.join(outDir, `logo-${w}.png`);
    await sharp(src, { density: 1600 })
      .resize({ width: w }) // full lockup is 4:1; width drives the export
      .png()
      .toFile(out);
    const st = fs.statSync(out);
    console.log(`${out}  ${st.size} bytes`);
    if (st.size === 0) throw new Error(`zero-byte export: ${out}`);
  }
  console.log("all exports OK");
})().catch((e) => { console.error(e); process.exit(1); });
