import { cp, mkdir, rm } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const dist = join(root, "dist");

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

const entries = [
  "index.html",
  "app.js",
  "styles.css",
  "robots.txt",
  "PUBLICATION_CHECKLIST.md",
  "data",
  "public",
];

for (const entry of entries) {
  await cp(join(root, entry), join(dist, entry), { recursive: true });
}
