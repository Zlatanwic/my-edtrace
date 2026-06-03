import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const frontendDir = dirname(dirname(fileURLToPath(import.meta.url)));
const repoRoot = dirname(frontendDir);
const sourceImages = join(repoRoot, 'images');
const publicImages = join(frontendDir, 'public', 'images');

if (existsSync(sourceImages)) {
  rmSync(publicImages, { recursive: true, force: true });
  mkdirSync(publicImages, { recursive: true });
  cpSync(sourceImages, publicImages, { recursive: true });
}
