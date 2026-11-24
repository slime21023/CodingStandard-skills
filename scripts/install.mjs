#!/usr/bin/env node

import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

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

// Check if source was provided; default to local root if no source specified
const hasSource = args.some(arg => !arg.startsWith('-'));
const finalArgs = ['skills', 'add'];

if (!hasSource) {
  finalArgs.push(rootDir);
}

finalArgs.push(...args);

// Determine runner: prefer bunx if available, fallback to npx
const runner = process.versions.bun ? 'bunx' : (process.platform === 'win32' ? 'npx.cmd' : 'npx');

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
