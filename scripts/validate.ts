import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validate as validateSkillDir } from "./lib/skills-ref.js";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS_DIR = path.join(REPO_ROOT, "skills");
const SKILL_BODY_MAX_LINES = 500;
const NAME_PATTERN = /^name:\s*(.+?)\s*$/;

function splitLines(value: string): string[] {
  if (value === "") {
    return [];
  }

  const normalized = value.replaceAll("\r\n", "\n").replaceAll("\r", "\n");
  const lines = normalized.split("\n");
  if (lines.at(-1) === "") {
    lines.pop();
  }

  return lines;
}

async function skillBodyLineCount(skillMdPath: string): Promise<number> {
  const lines = splitLines(await readFile(skillMdPath, "utf8"));

  if (lines.length === 0) {
    return 0;
  }

  if (lines[0]?.trim() !== "---") {
    return lines.length;
  }

  const closingIndex = lines.findIndex((line, index) => index > 0 && line.trim() === "---");
  if (closingIndex === -1) {
    return lines.length - 1;
  }

  return lines.length - closingIndex - 1;
}

async function extractSkillName(skillMdPath: string): Promise<string | null> {
  const lines = splitLines(await readFile(skillMdPath, "utf8"));

  if (lines[0]?.trim() !== "---") {
    return null;
  }

  for (const line of lines.slice(1)) {
    if (line.trim() === "---") {
      return null;
    }

    if (/^[ \t]/.test(line)) {
      continue;
    }

    const match = NAME_PATTERN.exec(line);
    if (match?.[1] !== undefined) {
      return match[1].trim().replace(/^['"]|['"]$/g, "");
    }
  }

  return null;
}

function resolveTarget(raw: string): string {
  return path.isAbsolute(raw) ? raw : path.join(REPO_ROOT, raw);
}

function findSkillRoot(target: string): string | null {
  const resolvedTarget = path.resolve(target);

  if (resolvedTarget === REPO_ROOT || resolvedTarget === SKILLS_DIR) {
    return SKILLS_DIR;
  }

  let candidate = resolvedTarget;
  while (candidate.startsWith(`${SKILLS_DIR}${path.sep}`)) {
    if (path.dirname(candidate) === SKILLS_DIR) {
      return candidate;
    }

    const parent = path.dirname(candidate);
    if (parent === candidate) {
      break;
    }

    candidate = parent;
  }

  return null;
}

async function validateSkill(skillDir: string): Promise<string[]> {
  const skillMdPath = path.join(skillDir, "SKILL.md");
  const relativePath = path.relative(REPO_ROOT, skillDir).split(path.sep).join("/");

  try {
    await readFile(skillMdPath, "utf8");
  } catch {
    return [`skill directory '${relativePath}' is missing SKILL.md`];
  }

  console.log(`Validating skill: ${path.basename(skillDir)}`);
  const errors = await validateSkillDir(skillDir);
  const bodyLines = await skillBodyLineCount(skillMdPath);

  if (bodyLines > SKILL_BODY_MAX_LINES) {
    errors.push(
      `Skill '${path.basename(skillDir)}' SKILL.md body is ${bodyLines} lines (limit is ${SKILL_BODY_MAX_LINES})`,
    );
  }

  return errors;
}

async function validateAll(): Promise<string[]> {
  try {
    const children = await readdir(SKILLS_DIR, { withFileTypes: true });
    const errors: string[] = [];
    const skillNameToDir = new Map<string, string>();
    const skillDirs = children
      .filter((child) => child.isDirectory() && !child.name.startsWith("."))
      .map((child) => child.name)
      .sort((left, right) => left.localeCompare(right));

    if (skillDirs.length === 0) {
      console.log("No skills found. Nothing to validate.");
      return errors;
    }

    for (const skillName of skillDirs) {
      const skillDir = path.join(SKILLS_DIR, skillName);
      errors.push(...(await validateSkill(skillDir)));

      const skillMdPath = path.join(skillDir, "SKILL.md");
      let extractedSkillName: string | null = null;
      try {
        extractedSkillName = await extractSkillName(skillMdPath);
      } catch {
        extractedSkillName = null;
      }

      if (extractedSkillName === null) {
        continue;
      }

      const relativePath = path.relative(REPO_ROOT, skillDir).split(path.sep).join("/");
      const previousPath = skillNameToDir.get(extractedSkillName);
      if (previousPath !== undefined) {
        errors.push(
          `duplicate skill name '${extractedSkillName}' found in ${previousPath} and ${relativePath}`,
        );
      } else {
        skillNameToDir.set(extractedSkillName, relativePath);
      }
    }

    return errors;
  } catch {
    return ["skills/ directory not found"];
  }
}

export async function runValidation(args: string[]): Promise<number> {
  let errors: string[];

  if (args.length > 0) {
    const target = resolveTarget(args[0]);
    const skillRoot = findSkillRoot(target);

    if (skillRoot === null) {
      console.error(`error: could not find a skill at or above ${target}`);
      return 1;
    }

    errors = skillRoot === SKILLS_DIR ? await validateAll() : await validateSkill(skillRoot);
  } else {
    errors = await validateAll();
  }

  for (const error of errors) {
    console.error(`  error: ${error}`);
  }

  if (errors.length > 0) {
    console.log(`\nValidation failed with ${errors.length} error(s).`);
    return 1;
  }

  console.log("\nValidation passed.");
  return 0;
}

if (
  process.argv[1] !== undefined &&
  fileURLToPath(import.meta.url) === path.resolve(process.argv[1])
) {
  const exitCode = await runValidation(process.argv.slice(2));
  process.exit(exitCode);
}
