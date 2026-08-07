import { spawn, type ChildProcess } from 'node:child_process';
import { resolve } from 'node:path';
import type { PlaywrightTestConfig } from '@playwright/test';

const frontendRoot = resolve(__dirname, '..', '..');
const viteEntry = resolve(frontendRoot, 'node_modules', 'vite', 'bin', 'vite.js');
export const shellBaseUrl = 'http://127.0.0.1:4173';

async function isReady(): Promise<boolean> {
  try {
    const response = await fetch(shellBaseUrl);
    return response.ok;
  } catch {
    return false;
  }
}

async function waitUntilReady(child: ChildProcess): Promise<void> {
  const deadline = Date.now() + 30_000;
  while (Date.now() < deadline) {
    if (child.exitCode !== null) {
      throw new Error(`Vite test server exited early with code ${child.exitCode}`);
    }
    if (await isReady()) return;
    await new Promise((resolveDelay) => setTimeout(resolveDelay, 100));
  }
  throw new Error('Vite test server did not become ready within 30 seconds');
}

export async function ensureShellTestServer(): Promise<() => Promise<void>> {
  if (await isReady()) return async () => undefined;

  const child = spawn(
    process.execPath,
    [viteEntry, '--host', '127.0.0.1', '--port', '4173', '--strictPort'],
    { cwd: frontendRoot, stdio: 'ignore', windowsHide: true },
  );
  await waitUntilReady(child);

  return async () => {
    if (child.exitCode === null) child.kill();
  };
}

export const shellTestServer: NonNullable<PlaywrightTestConfig['webServer']> = {
  command: 'node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 4173 --strictPort',
  url: shellBaseUrl,
  reuseExistingServer: false,
  timeout: 30_000,
};
