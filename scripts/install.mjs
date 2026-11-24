#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

// List of environment variables that cause `skills` CLI to assume non-interactive agent mode
const AGENT_ENV_VARS = [
  'AI_AGENT',
  'CURSOR_TRACE_ID',
  'CURSOR_AGENT',
  'CURSOR_EXTENSION_HOST_ROLE',
  'GEMINI_CLI',
  'CODEX_SANDBOX',
  'CODEX_CI',
  'CODEX_THREAD_ID',
  'ANTIGRAVITY_AGENT',
  'AUGMENT_AGENT',
  'OPENCODE_CLIENT',
  'CLAUDECODE',
  'CLAUDE_CODE',
  'REPL_ID',
  'COPILOT_MODEL',
  'COPILOT_ALLOW_ALL',
  'COPILOT_GITHUB_TOKEN'
];

// Clean environment to allow interactive skill/agent selection even when running inside AI IDE terminals
const cleanEnv = { ...process.env };
for (const envVar of AGENT_ENV_VARS) {
  delete cleanEnv[envVar];
}

const args = process.argv.slice(2);

// Match skills add's value-taking options; keep the original arguments for the CLI.
const { tokens } = parseArgs({
  args,
  options: {
    agent: { type: 'string', short: 'a' },
    skill: { type: 'string', short: 's' },
    subagent: { type: 'string' },
    metadata: { type: 'string' },
    rename: { type: 'string' },
  },
  strict: false,
  tokens: true,
});
const listOptions = new Set(['agent', 'skill', 'subagent']);
let hasSource = false;
for (let i = 0; i < tokens.length; i++) {
  const token = tokens[i];
  if (token.kind === 'positional' && token.value) {
    hasSource = true;
    break;
  }
  if (token.kind === 'option' && !token.inlineValue && token.value &&
      !token.value.startsWith('-') && listOptions.has(token.name)) {
    while (tokens[i + 1]?.kind === 'positional') i++;
  }
}
const finalArgs = ['skills', 'add'];

if (!hasSource) {
  finalArgs.push(rootDir);
}

finalArgs.push(...args);

let runner = process.versions.bun ? 'bunx' : 'npx';
if (runner === 'npx' && process.platform === 'win32') {
  // Windows cannot spawn npx.cmd directly. Run npm's JS launcher without a shell.
  const nodeDir = path.dirname(process.execPath);
  const npxCli = path.join(nodeDir, 'node_modules', 'npm', 'bin', 'npx-cli.js');
  if (!existsSync(npxCli)) {
    console.error('Cannot find bundled npm. Install Node.js with npm or use bun run install:skills.');
    process.exit(1);
  }
  runner = process.execPath;
  finalArgs.unshift(npxCli);
  // Use the same Node executable when npm's package shim launches the CLI.
  const pathKey = Object.keys(cleanEnv).find(key => key.toUpperCase() === 'PATH') ?? 'Path';
  const inheritedPath = cleanEnv[pathKey];
  cleanEnv[pathKey] = inheritedPath ? `${nodeDir}${path.delimiter}${inheritedPath}` : nodeDir;
}

const child = spawn(runner, finalArgs, {
  stdio: 'inherit',
  env: cleanEnv,
  cwd: process.cwd()
});

child.on('error', (err) => {
  console.error(`Failed to launch ${runner}:`, err.message);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});
