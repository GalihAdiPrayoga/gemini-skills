#!/usr/bin/env node

/**
 * Gemini Skills & Cognitive Architecture Installer
 * Automatically detects .gemini location across Windows, macOS, and Linux
 * and syncs skills, plugins, rules, and extensions seamlessly.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Terminal ANSI colors
const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  red: '\x1b[31m',
};

function printBanner() {
  console.log(`\n${colors.cyan}${colors.bold}====================================================${colors.reset}`);
  console.log(`${colors.magenta}${colors.bold}   ✨ GEMINI SKILLS & COGNITIVE ARCHITECTURE ✨${colors.reset}`);
  console.log(`${colors.dim}   Automated Cross-Platform Installer & Sync Tool${colors.reset}`);
  console.log(`${colors.cyan}${colors.bold}====================================================${colors.reset}\n`);
}

function detectGeminiDirectory(customTarget) {
  if (customTarget) {
    return path.resolve(customTarget);
  }

  // 1. Check GEMINI_HOME environment variable
  if (process.env.GEMINI_HOME && fs.existsSync(process.env.GEMINI_HOME)) {
    return path.resolve(process.env.GEMINI_HOME);
  }

  // 2. Default User Home directory (.gemini)
  const home = os.homedir();
  const defaultGemini = path.join(home, '.gemini');

  return defaultGemini;
}

function copyRecursiveSync(src, dest, stats = { copied: 0, skipped: 0 }) {
  if (!fs.existsSync(src)) return stats;

  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    const items = fs.readdirSync(src);
    for (const item of items) {
      if (item === '.git' || item === 'node_modules') continue;
      copyRecursiveSync(path.join(src, item), path.join(dest, item), stats);
    }
  } else {
    const parentDir = path.dirname(dest);
    if (!fs.existsSync(parentDir)) {
      fs.mkdirSync(parentDir, { recursive: true });
    }
    fs.copyFileSync(src, dest);
    stats.copied++;
  }
  return stats;
}

function main() {
  printBanner();

  const args = process.argv.slice(2);
  let customTarget = null;
  let isDryRun = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--target' || args[i] === '-t') {
      customTarget = args[i + 1];
      i++;
    } else if (args[i] === '--dry-run') {
      isDryRun = true;
    } else if (args[i] === '--help' || args[i] === '-h') {
      console.log(`Usage: npx gemini-skills [options]\n`);
      console.log(`Options:`);
      console.log(`  -t, --target <path>  Custom target .gemini directory`);
      console.log(`  --dry-run            Simulate installation without writing files`);
      console.log(`  -h, --help           Show help info\n`);
      process.exit(0);
    }
  }

  const geminiDir = detectGeminiDirectory(customTarget);
  const repoRoot = path.resolve(__dirname, '..');

  console.log(`${colors.bold}📍 Target .gemini Location:${colors.reset} ${colors.green}${geminiDir}${colors.reset}`);
  console.log(`${colors.bold}📦 Package Source Root:${colors.reset}     ${colors.cyan}${repoRoot}${colors.reset}\n`);

  if (!fs.existsSync(geminiDir)) {
    console.log(`${colors.yellow}Creating new .gemini directory structure...${colors.reset}`);
    if (!isDryRun) {
      fs.mkdirSync(geminiDir, { recursive: true });
    }
  }

  const syncModules = [
    { src: 'skills', dest: 'skills', label: 'Cognitive Skills' },
    { src: 'plugins', dest: 'plugins', label: 'Workflow Plugins' },
    { src: 'rules', dest: 'rules', label: 'Mandatory Rules' },
    { src: 'extensions', dest: 'extensions', label: 'IDE Extensions' },
    { src: 'public', dest: 'public', label: 'Public Assets' },
    { src: 'AGENTS.md', dest: 'AGENTS.md', label: 'Global Agent Protocol' },
    { src: 'GEMINI.md', dest: 'GEMINI.md', label: 'Gemini Context Standard' },
  ];

  let totalCopied = 0;

  console.log(`${colors.bold}🚀 Syncing Modules to .gemini:${colors.reset}`);

  for (const mod of syncModules) {
    const srcPath = path.join(repoRoot, mod.src);
    const destPath = path.join(geminiDir, mod.dest);

    if (fs.existsSync(srcPath)) {
      process.stdout.write(`  • Installing ${colors.cyan}${mod.label}${colors.reset}... `);
      if (!isDryRun) {
        const stats = copyRecursiveSync(srcPath, destPath);
        totalCopied += stats.copied;
        console.log(`${colors.green}✓ Done${colors.reset} (${stats.copied} items)`);
      } else {
        console.log(`${colors.yellow}[DRY-RUN] Would sync${colors.reset}`);
      }
    }
  }

  // Also sync to .gemini/config/ for Antigravity IDE compatibility
  const configDir = path.join(geminiDir, 'config');
  if (!fs.existsSync(configDir) && !isDryRun) {
    fs.mkdirSync(configDir, { recursive: true });
  }

  const configSync = [
    { src: 'skills', dest: path.join(configDir, 'skills') },
    { src: 'plugins', dest: path.join(configDir, 'plugins') },
    { src: 'rules', dest: path.join(configDir, 'rules') },
    { src: 'AGENTS.md', dest: path.join(configDir, 'AGENTS.md') },
  ];

  for (const item of configSync) {
    const srcP = path.join(repoRoot, item.src);
    if (fs.existsSync(srcP) && !isDryRun) {
      copyRecursiveSync(srcP, item.dest);
    }
  }

  console.log(`\n${colors.green}${colors.bold}🎉 Installation Successful!${colors.reset}`);
  console.log(`${colors.dim}Total files synced: ${totalCopied} files.${colors.reset}`);
  console.log(`\n${colors.cyan}Gemini CLI & Antigravity IDE are now ready with full cognitive skills suite.${colors.reset}\n`);
}

main();
