#!/usr/bin/env node
/**
 * Convert Mermaid diagrams → SVG using mermaid-cli (mmdc).
 *
 * Usage:
 *   cd scripts && npm install
 *   node export_diagrams.mjs            # convert all
 *   node export_diagrams.mjs dual_llm   # convert one
 *
 * Output:
 *   diagrams/<name>.svg
 *
 * To also get Excalidraw files, paste the .mmd content into
 * https://excalidraw.com (Hamburger → Mermaid to Excalidraw).
 */

import { execFileSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MERMAID_DIR = path.join(__dirname, "..", "diagrams", "mermaid");
const OUTPUT_DIR = path.join(__dirname, "..", "diagrams");
const MMDC = path.join(__dirname, "node_modules", ".bin", "mmdc");

/** Mermaid CLI config for clean SVG output. */
const MMDC_CONFIG = {
  theme: "default",
  themeVariables: {
    fontSize: "14px",
    fontFamily: "system-ui, sans-serif",
  },
};

const CONFIG_PATH = path.join(__dirname, ".mermaidrc.json");

function writeConfig() {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(MMDC_CONFIG, null, 2));
}

function convertOne(name) {
  const mmdPath = path.join(MERMAID_DIR, `${name}.mmd`);
  const svgPath = path.join(OUTPUT_DIR, `${name}.svg`);

  if (!fs.existsSync(mmdPath)) {
    console.error(`  ✗ ${name}.mmd not found`);
    return false;
  }

  try {
    execFileSync(MMDC, [
      "-i", mmdPath,
      "-o", svgPath,
      "-c", CONFIG_PATH,
      "-b", "transparent",
    ], { stdio: "pipe" });
    console.log(`  ✓ ${name}.svg`);
    return true;
  } catch (err) {
    const stderr = err.stderr ? err.stderr.toString().trim() : err.message;
    console.error(`  ✗ ${name}: ${stderr.split("\n")[0]}`);
    return false;
  }
}

function main() {
  const filter = process.argv[2];

  const mmdFiles = fs
    .readdirSync(MERMAID_DIR)
    .filter((f) => f.endsWith(".mmd"))
    .map((f) => f.replace(".mmd", ""))
    .filter((name) => !filter || name === filter)
    .sort();

  if (mmdFiles.length === 0) {
    console.error("No .mmd files found" + (filter ? ` matching '${filter}'` : ""));
    process.exit(1);
  }

  writeConfig();
  console.log(`Converting ${mmdFiles.length} diagram(s) → SVG...\n`);

  let success = 0;
  let failed = 0;

  for (const name of mmdFiles) {
    const ok = convertOne(name);
    if (ok) success++;
    else failed++;
  }

  // Cleanup config
  if (fs.existsSync(CONFIG_PATH)) fs.unlinkSync(CONFIG_PATH);

  console.log(`\nDone: ${success} converted, ${failed} failed.`);
  console.log(`SVGs saved to: ${OUTPUT_DIR}/`);

  if (failed > 0) process.exit(1);
}

main();
