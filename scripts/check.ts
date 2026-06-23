import { access, mkdtemp, readdir, rm } from "node:fs/promises";
import { spawn } from "node:child_process";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runValidation } from "./validate.js";
import { runMarketplaceValidation } from "./validate-marketplaces.js";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SHELLCHECK_VERSION = "0.10.0";
const ACTIONLINT_VERSION = "1.7.7";

let toolsDir: string | undefined;

interface RunCommandOptions {
  cwd?: string;
  capture?: boolean;
}

async function runCommand(
  command: string,
  args: string[],
  options: RunCommandOptions = {},
): Promise<string> {
  return await new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd: options.cwd,
      env: process.env,
      stdio: options.capture ? ["ignore", "pipe", "pipe"] : "inherit",
    });

    let stdout = "";
    let stderr = "";

    if (options.capture) {
      child.stdout?.on("data", (chunk: Buffer | string) => {
        stdout += chunk.toString();
      });
      child.stderr?.on("data", (chunk: Buffer | string) => {
        stderr += chunk.toString();
      });
    }

    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) {
        resolve(stdout);
        return;
      }

      reject(
        new Error(
          options.capture
            ? stderr.trim() || stdout.trim() || `${command} exited with code ${code ?? "unknown"}`
            : `${command} exited with code ${code ?? "unknown"}`,
        ),
      );
    });
  });
}

async function commandExists(command: string): Promise<boolean> {
  try {
    await runCommand("bash", ["-lc", `command -v ${command} >/dev/null 2>&1`]);
    return true;
  } catch {
    return false;
  }
}

async function fileExists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function ensureToolsDir(): Promise<string> {
  if (toolsDir !== undefined) {
    return toolsDir;
  }

  toolsDir = await mkdtemp(path.join(os.tmpdir(), "agent-skills-tools."));
  return toolsDir;
}

function detectShellcheckAsset(): string {
  switch (`${os.platform()}-${os.arch()}`) {
    case "darwin-arm64":
      return "darwin.aarch64";
    case "darwin-x64":
      return "darwin.x86_64";
    case "linux-arm64":
      return "linux.aarch64";
    case "linux-x64":
      return "linux.x86_64";
    default:
      throw new Error(
        `Unsupported platform for temporary shellcheck download: ${os.platform()} ${os.arch()}`,
      );
  }
}

function detectActionlintAsset(): string {
  switch (`${os.platform()}-${os.arch()}`) {
    case "darwin-arm64":
      return "darwin_arm64";
    case "darwin-x64":
      return "darwin_amd64";
    case "linux-arm64":
      return "linux_arm64";
    case "linux-x64":
      return "linux_amd64";
    default:
      throw new Error(
        `Unsupported platform for temporary actionlint download: ${os.platform()} ${os.arch()}`,
      );
  }
}

async function downloadShellcheck(): Promise<string> {
  const currentToolsDir = await ensureToolsDir();
  const archivePath = path.join(currentToolsDir, "shellcheck.tar.xz");
  const extractedDir = path.join(currentToolsDir, `shellcheck-v${SHELLCHECK_VERSION}`);

  await runCommand("curl", [
    "-fsSL",
    `https://github.com/koalaman/shellcheck/releases/download/v${SHELLCHECK_VERSION}/shellcheck-v${SHELLCHECK_VERSION}.${detectShellcheckAsset()}.tar.xz`,
    "-o",
    archivePath,
  ]);
  await runCommand("tar", ["-xJf", archivePath, "-C", currentToolsDir]);

  return path.join(extractedDir, "shellcheck");
}

async function downloadActionlint(): Promise<string> {
  const currentToolsDir = await ensureToolsDir();
  const archivePath = path.join(currentToolsDir, "actionlint.tar.gz");

  await runCommand("curl", [
    "-fsSL",
    `https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_${detectActionlintAsset()}.tar.gz`,
    "-o",
    archivePath,
  ]);
  await runCommand("tar", ["-xzf", archivePath, "-C", currentToolsDir, "actionlint"]);

  return path.join(currentToolsDir, "actionlint");
}

async function collectShellFiles(): Promise<string[]> {
  const shellFiles: string[] = [];
  const rootScriptsDir = path.join(REPO_ROOT, "scripts");

  try {
    const rootScriptEntries = await readdir(rootScriptsDir, { withFileTypes: true });
    for (const entry of rootScriptEntries) {
      if (entry.isFile() && entry.name.endsWith(".sh")) {
        shellFiles.push(path.join(rootScriptsDir, entry.name));
      }
    }
  } catch {
    // Ignore missing scripts/; validation below will skip if nothing is found.
  }

  const skillsDir = path.join(REPO_ROOT, "skills");
  const skillEntries = await readdir(skillsDir, { withFileTypes: true });
  for (const skillEntry of skillEntries) {
    if ((!skillEntry.isDirectory() && !skillEntry.isSymbolicLink()) || skillEntry.name.startsWith(".")) {
      continue;
    }

    const skillScriptsDir = path.join(skillsDir, skillEntry.name, "scripts");
    try {
      const scriptEntries = await readdir(skillScriptsDir, { withFileTypes: true });
      for (const entry of scriptEntries) {
        if (entry.isFile() && entry.name.endsWith(".sh")) {
          shellFiles.push(path.join(skillScriptsDir, entry.name));
        }
      }
    } catch {
      // Ignore skills without scripts/.
    }
  }

  return shellFiles;
}

async function runShellcheck(): Promise<void> {
  const shellFiles = await collectShellFiles();
  if (shellFiles.length === 0) {
    console.log("No shell scripts found; skipping shellcheck.");
    return;
  }

  const shellcheckBinary = (await commandExists("shellcheck"))
    ? "shellcheck"
    : await downloadShellcheck();

  await runCommand(shellcheckBinary, shellFiles);
}

async function runNodeChecks(): Promise<void> {
  const skillsDir = path.join(REPO_ROOT, "skills");
  const skillEntries = await readdir(skillsDir, { withFileTypes: true });
  const packageJsonPaths: string[] = [];

  for (const skillEntry of skillEntries) {
    if ((!skillEntry.isDirectory() && !skillEntry.isSymbolicLink()) || skillEntry.name.startsWith(".")) {
      continue;
    }

    const skillDir = path.join(skillsDir, skillEntry.name);
    if (await fileExists(path.join(skillDir, "package.json"))) {
      packageJsonPaths.push(path.join(skillDir, "package.json"));
    }
  }

  if (packageJsonPaths.length === 0) {
    console.log("No Node-based skills found; skipping npm validation.");
    return;
  }

  for (const packageJsonPath of packageJsonPaths.sort()) {
    const skillDir = path.dirname(packageJsonPath);
    console.log(`Validating Node skill: ${path.relative(REPO_ROOT, skillDir)}`);

    if (await fileExists(path.join(skillDir, "package-lock.json"))) {
      await runCommand("npm", ["ci", "--prefix", skillDir]);
    } else {
      await runCommand("npm", ["install", "--prefix", skillDir]);
    }

    await runCommand("npm", ["--prefix", skillDir, "run", "--if-present", "typecheck"]);
  }
}

async function runActionlint(): Promise<void> {
  const workflowsDir = path.join(REPO_ROOT, ".github", "workflows");
  let workflowFiles: string[] = [];

  try {
    workflowFiles = (await readdir(workflowsDir, { withFileTypes: true }))
      .filter((entry) => entry.isFile() && /\.(ya?ml)$/u.test(entry.name))
      .map((entry) => path.join(workflowsDir, entry.name));
  } catch {
    workflowFiles = [];
  }

  if (workflowFiles.length === 0) {
    console.log("No workflows found; skipping actionlint.");
    return;
  }

  const actionlintBinary = (await commandExists("actionlint"))
    ? "actionlint"
    : await downloadActionlint();

  await runCommand(actionlintBinary, workflowFiles);
}

async function cleanup(): Promise<void> {
  if (toolsDir !== undefined) {
    await rm(toolsDir, { recursive: true, force: true });
  }
}

async function main(args: string[]): Promise<number> {
  process.chdir(REPO_ROOT);

  await runCommand("npm", ["run", "typecheck"]);
  await runCommand("npm", ["test"]);

  const validationExitCode = await runValidation(args);
  if (validationExitCode !== 0) {
    return validationExitCode;
  }

  const marketplaceValidationExitCode = await runMarketplaceValidation();
  if (marketplaceValidationExitCode !== 0) {
    return marketplaceValidationExitCode;
  }

  await runShellcheck();
  await runNodeChecks();
  await runActionlint();
  return 0;
}

let exitCode = 1;
try {
  exitCode = await main(process.argv.slice(2));
} finally {
  await cleanup();
}

process.exit(exitCode);
