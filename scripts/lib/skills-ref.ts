import { access, readFile, stat } from "node:fs/promises";
import path from "node:path";
import { isMap, parseDocument } from "yaml";

export class SkillError extends Error {}

export class ParseError extends SkillError {}

export class ValidationError extends SkillError {
  readonly errors: string[];

  constructor(message: string, errors: string[] = [message]) {
    super(message);
    this.errors = errors;
  }
}

export interface SkillProperties {
  name: string;
  description: string;
  license?: string;
  compatibility?: string;
  allowedTools?: string;
  metadata: Record<string, string>;
}

type FrontmatterMetadata = Record<string, unknown>;

const MAX_SKILL_NAME_LENGTH = 64;
const MAX_DESCRIPTION_LENGTH = 1024;
const MAX_COMPATIBILITY_LENGTH = 500;
const ALLOWED_FIELDS = new Set([
  "allowed-tools",
  "argument-hint",
  "compatibility",
  "description",
  "disable-model-invocation",
  "license",
  "metadata",
  "name",
]);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function countCharacters(value: string): number {
  return Array.from(value).length;
}

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

function formatAllowedFields(): string {
  return `[${[...ALLOWED_FIELDS]
    .sort()
    .map((field) => `'${field}'`)
    .join(", ")}]`;
}

function escapeXml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

async function exists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

function normalizeMetadata(metadata: FrontmatterMetadata): FrontmatterMetadata {
  const normalized = { ...metadata };
  const metadataField = normalized.metadata;

  if (isRecord(metadataField)) {
    normalized.metadata = Object.fromEntries(
      Object.entries(metadataField).map(([key, value]) => [String(key), String(value)]),
    );
  }

  return normalized;
}

function validateName(name: unknown, skillDir?: string): string[] {
  const errors: string[] = [];

  if (typeof name !== "string" || name.trim() === "") {
    errors.push("Field 'name' must be a non-empty string");
    return errors;
  }

  const normalizedName = name.trim().normalize("NFKC");

  if (countCharacters(normalizedName) > MAX_SKILL_NAME_LENGTH) {
    errors.push(
      `Skill name '${normalizedName}' exceeds ${MAX_SKILL_NAME_LENGTH} character limit (${countCharacters(normalizedName)} chars)`,
    );
  }

  if (normalizedName !== normalizedName.toLowerCase()) {
    errors.push(`Skill name '${normalizedName}' must be lowercase`);
  }

  if (normalizedName.startsWith("-") || normalizedName.endsWith("-")) {
    errors.push("Skill name cannot start or end with a hyphen");
  }

  if (normalizedName.includes("--")) {
    errors.push("Skill name cannot contain consecutive hyphens");
  }

  if (!/^[\p{Letter}\p{Number}-]+$/u.test(normalizedName)) {
    errors.push(
      `Skill name '${normalizedName}' contains invalid characters. Only letters, digits, and hyphens are allowed.`,
    );
  }

  if (skillDir !== undefined) {
    const normalizedDirName = path.basename(skillDir).normalize("NFKC");
    if (normalizedDirName !== normalizedName) {
      errors.push(
        `Directory name '${path.basename(skillDir)}' must match skill name '${normalizedName}'`,
      );
    }
  }

  return errors;
}

function validateDescription(description: unknown): string[] {
  const errors: string[] = [];

  if (typeof description !== "string" || description.trim() === "") {
    errors.push("Field 'description' must be a non-empty string");
    return errors;
  }

  if (countCharacters(description) > MAX_DESCRIPTION_LENGTH) {
    errors.push(
      `Description exceeds ${MAX_DESCRIPTION_LENGTH} character limit (${countCharacters(description)} chars)`,
    );
  }

  return errors;
}

function validateCompatibility(compatibility: unknown): string[] {
  const errors: string[] = [];

  if (typeof compatibility !== "string") {
    errors.push("Field 'compatibility' must be a string");
    return errors;
  }

  if (countCharacters(compatibility) > MAX_COMPATIBILITY_LENGTH) {
    errors.push(
      `Compatibility exceeds ${MAX_COMPATIBILITY_LENGTH} character limit (${countCharacters(compatibility)} chars)`,
    );
  }

  return errors;
}

export function parseFrontmatter(content: string): {
  metadata: FrontmatterMetadata;
  body: string;
} {
  const lines = splitLines(content);

  if (lines[0]?.trim() !== "---") {
    throw new ParseError("SKILL.md must start with YAML frontmatter (---)");
  }

  const closingIndex = lines.findIndex((line, index) => index > 0 && line.trim() === "---");
  if (closingIndex === -1) {
    throw new ParseError("SKILL.md frontmatter not properly closed with ---");
  }

  const frontmatter = lines.slice(1, closingIndex).join("\n");
  const body = lines.slice(closingIndex + 1).join("\n").trim();
  const parsed = parseDocument(frontmatter, { prettyErrors: false });

  if (parsed.errors.length > 0) {
    throw new ParseError(`Invalid YAML in frontmatter: ${parsed.errors[0]?.message ?? "unknown error"}`);
  }

  if (!isMap(parsed.contents)) {
    throw new ParseError("SKILL.md frontmatter must be a YAML mapping");
  }

  const metadata = parsed.toJS();
  if (!isRecord(metadata)) {
    throw new ParseError("SKILL.md frontmatter must be a YAML mapping");
  }

  return {
    metadata: normalizeMetadata(metadata),
    body,
  };
}

export async function findSkillMd(skillDir: string): Promise<string | null> {
  for (const candidate of ["SKILL.md", "skill.md"]) {
    const skillMdPath = path.join(skillDir, candidate);
    if (await exists(skillMdPath)) {
      return skillMdPath;
    }
  }

  return null;
}

export async function readProperties(skillDir: string): Promise<SkillProperties> {
  const skillMdPath = await findSkillMd(skillDir);
  if (skillMdPath === null) {
    throw new ParseError(`SKILL.md not found in ${skillDir}`);
  }

  const content = await readFile(skillMdPath, "utf8");
  const { metadata } = parseFrontmatter(content);

  if (!("name" in metadata)) {
    throw new ValidationError("Missing required field in frontmatter: name");
  }

  if (!("description" in metadata)) {
    throw new ValidationError("Missing required field in frontmatter: description");
  }

  if (typeof metadata.name !== "string" || metadata.name.trim() === "") {
    throw new ValidationError("Field 'name' must be a non-empty string");
  }

  if (typeof metadata.description !== "string" || metadata.description.trim() === "") {
    throw new ValidationError("Field 'description' must be a non-empty string");
  }

  return {
    name: metadata.name.trim(),
    description: metadata.description.trim(),
    license: typeof metadata.license === "string" ? metadata.license : undefined,
    compatibility:
      typeof metadata.compatibility === "string" ? metadata.compatibility : undefined,
    allowedTools:
      typeof metadata["allowed-tools"] === "string" ? metadata["allowed-tools"] : undefined,
    metadata: isRecord(metadata.metadata)
      ? Object.fromEntries(
          Object.entries(metadata.metadata).map(([key, value]) => [key, String(value)]),
        )
      : {},
  };
}

export function validateMetadata(
  metadata: FrontmatterMetadata,
  skillDir?: string,
): string[] {
  const errors: string[] = [];
  const extraFields = Object.keys(metadata).filter((field) => !ALLOWED_FIELDS.has(field));

  if (extraFields.length > 0) {
    errors.push(
      `Unexpected fields in frontmatter: ${extraFields.sort().join(", ")}. Only ${formatAllowedFields()} are allowed.`,
    );
  }

  if (!("name" in metadata)) {
    errors.push("Missing required field in frontmatter: name");
  } else {
    errors.push(...validateName(metadata.name, skillDir));
  }

  if (!("description" in metadata)) {
    errors.push("Missing required field in frontmatter: description");
  } else {
    errors.push(...validateDescription(metadata.description));
  }

  if ("compatibility" in metadata) {
    errors.push(...validateCompatibility(metadata.compatibility));
  }

  return errors;
}

export async function validate(skillDir: string): Promise<string[]> {
  if (!(await exists(skillDir))) {
    return [`Path does not exist: ${skillDir}`];
  }

  const stats = await stat(skillDir);
  if (!stats.isDirectory()) {
    return [`Not a directory: ${skillDir}`];
  }

  const skillMdPath = await findSkillMd(skillDir);
  if (skillMdPath === null) {
    return ["Missing required file: SKILL.md"];
  }

  try {
    const content = await readFile(skillMdPath, "utf8");
    const { metadata } = parseFrontmatter(content);
    return validateMetadata(metadata, skillDir);
  } catch (error) {
    if (error instanceof ParseError) {
      return [error.message];
    }

    throw error;
  }
}

export async function toPrompt(skillDirs: string[]): Promise<string> {
  const entries = await Promise.all(
    skillDirs.map(async (skillDir) => {
      const properties = await readProperties(skillDir);
      const skillMdPath = (await findSkillMd(skillDir)) ?? path.join(skillDir, "SKILL.md");

      return [
        "<skill>",
        "<name>",
        escapeXml(properties.name),
        "</name>",
        "<description>",
        escapeXml(properties.description),
        "</description>",
        "<location>",
        escapeXml(skillMdPath),
        "</location>",
        "</skill>",
      ].join("\n");
    }),
  );

  return ["<available_skills>", ...entries, "</available_skills>"].join("\n");
}
