import { access, lstat, readdir, readFile, realpath } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const CLAUDE_MARKETPLACE_PATH = ".claude-plugin/marketplace.json";
const CODEX_MARKETPLACE_PATH = ".agents/plugins/marketplace.json";
const PLUGIN_NAME_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/u;
const SEMVER_PATTERN = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/u;

type JsonObject = Record<string, unknown>;

interface MarketplacePlugin {
  name: string;
  path: string;
}

function isObject(value: unknown): value is JsonObject {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function asString(value: unknown, field: string): string {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`${field} must be a non-empty string`);
  }

  return value;
}

function asObject(value: unknown, field: string): JsonObject {
  if (!isObject(value)) {
    throw new Error(`${field} must be an object`);
  }

  return value;
}

function asArray(value: unknown, field: string): unknown[] {
  if (!Array.isArray(value)) {
    throw new Error(`${field} must be an array`);
  }

  return value;
}

async function exists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readJson(relativePath: string): Promise<JsonObject> {
  const filePath = path.join(REPO_ROOT, relativePath);
  const parsed = JSON.parse(await readFile(filePath, "utf8")) as unknown;
  return asObject(parsed, relativePath);
}

function validateName(name: string, field: string): void {
  if (!PLUGIN_NAME_PATTERN.test(name)) {
    throw new Error(`${field} must be kebab-case lowercase letters, digits, and hyphens`);
  }
}

function validateRelativePluginPath(sourcePath: string, field: string): void {
  if (!sourcePath.startsWith("./")) {
    throw new Error(`${field} must be a marketplace-root relative path beginning with './'`);
  }

  const normalized = path.posix.normalize(sourcePath.slice(2));
  if (
    normalized === "." ||
    normalized.startsWith("../") ||
    normalized.includes("/../") ||
    sourcePath !== `./${normalized}`
  ) {
    throw new Error(`${field} must not contain path traversal or redundant path segments`);
  }
}

function marketplacePlugins(marketplace: JsonObject, relativePath: string): JsonObject[] {
  const marketplaceName = asString(marketplace.name, `${relativePath}.name`);
  validateName(marketplaceName, `${relativePath}.name`);

  const plugins = asArray(marketplace.plugins, `${relativePath}.plugins`);
  if (plugins.length === 0) {
    throw new Error(`${relativePath}.plugins must not be empty`);
  }

  const seen = new Set<string>();
  return plugins.map((entry, index) => {
    const plugin = asObject(entry, `${relativePath}.plugins[${index}]`);
    const name = asString(plugin.name, `${relativePath}.plugins[${index}].name`);
    validateName(name, `${relativePath}.plugins[${index}].name`);

    if (seen.has(name)) {
      throw new Error(`${relativePath} contains duplicate plugin '${name}'`);
    }
    seen.add(name);

    return plugin;
  });
}

function parseClaudeMarketplace(marketplace: JsonObject): MarketplacePlugin[] {
  const owner = asObject(marketplace.owner, `${CLAUDE_MARKETPLACE_PATH}.owner`);
  asString(owner.name, `${CLAUDE_MARKETPLACE_PATH}.owner.name`);

  return marketplacePlugins(marketplace, CLAUDE_MARKETPLACE_PATH).map((plugin, index) => {
    const name = asString(plugin.name, `${CLAUDE_MARKETPLACE_PATH}.plugins[${index}].name`);
    const source = asString(plugin.source, `${CLAUDE_MARKETPLACE_PATH}.plugins[${index}].source`);
    validateRelativePluginPath(source, `${CLAUDE_MARKETPLACE_PATH}.plugins[${index}].source`);

    if (typeof plugin.description !== "string" || plugin.description.trim() === "") {
      throw new Error(`${CLAUDE_MARKETPLACE_PATH}.plugins[${index}].description must be present`);
    }

    if ("version" in plugin) {
      throw new Error(
        `${CLAUDE_MARKETPLACE_PATH}.plugins[${index}].version must be omitted so git commits drive updates`,
      );
    }

    return { name, path: source };
  });
}

function parseCodexMarketplace(marketplace: JsonObject): MarketplacePlugin[] {
  const marketplaceInterface = asObject(
    marketplace.interface,
    `${CODEX_MARKETPLACE_PATH}.interface`,
  );
  asString(marketplaceInterface.displayName, `${CODEX_MARKETPLACE_PATH}.interface.displayName`);

  return marketplacePlugins(marketplace, CODEX_MARKETPLACE_PATH).map((plugin, index) => {
    const name = asString(plugin.name, `${CODEX_MARKETPLACE_PATH}.plugins[${index}].name`);
    const source = asObject(plugin.source, `${CODEX_MARKETPLACE_PATH}.plugins[${index}].source`);

    if (source.source !== "local") {
      throw new Error(`${CODEX_MARKETPLACE_PATH}.plugins[${index}].source.source must be 'local'`);
    }

    const sourcePath = asString(
      source.path,
      `${CODEX_MARKETPLACE_PATH}.plugins[${index}].source.path`,
    );
    validateRelativePluginPath(sourcePath, `${CODEX_MARKETPLACE_PATH}.plugins[${index}].source.path`);

    const policy = asObject(plugin.policy, `${CODEX_MARKETPLACE_PATH}.plugins[${index}].policy`);
    if (policy.installation !== "AVAILABLE") {
      throw new Error(
        `${CODEX_MARKETPLACE_PATH}.plugins[${index}].policy.installation must be 'AVAILABLE'`,
      );
    }
    if (policy.authentication !== "ON_INSTALL") {
      throw new Error(
        `${CODEX_MARKETPLACE_PATH}.plugins[${index}].policy.authentication must be 'ON_INSTALL'`,
      );
    }
    if (typeof plugin.category !== "string" || plugin.category.trim() === "") {
      throw new Error(`${CODEX_MARKETPLACE_PATH}.plugins[${index}].category must be present`);
    }

    return { name, path: sourcePath };
  });
}

function assertSameMarketplacePlugins(
  claudePlugins: MarketplacePlugin[],
  codexPlugins: MarketplacePlugin[],
): void {
  const claudeByName = new Map(claudePlugins.map((plugin) => [plugin.name, plugin.path]));
  const codexByName = new Map(codexPlugins.map((plugin) => [plugin.name, plugin.path]));

  for (const [name, claudePath] of claudeByName) {
    const codexPath = codexByName.get(name);
    if (codexPath === undefined) {
      throw new Error(`Codex marketplace is missing Claude marketplace plugin '${name}'`);
    }
    if (codexPath !== claudePath) {
      throw new Error(
        `Marketplace plugin '${name}' points to '${claudePath}' for Claude but '${codexPath}' for Codex`,
      );
    }
  }

  for (const name of codexByName.keys()) {
    if (!claudeByName.has(name)) {
      throw new Error(`Claude marketplace is missing Codex marketplace plugin '${name}'`);
    }
  }
}

async function validatePluginBundle(plugin: MarketplacePlugin): Promise<void> {
  const pluginRoot = path.join(REPO_ROOT, plugin.path);
  const requiredPaths = [
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    "skills",
  ];

  for (const relativePath of requiredPaths) {
    const candidate = path.join(pluginRoot, relativePath);
    if (!(await exists(candidate))) {
      throw new Error(`plugin '${plugin.name}' is missing ${path.join(plugin.path, relativePath)}`);
    }
  }

  await validateClaudePluginManifest(plugin);
  await validateCodexPluginManifest(plugin);
}

async function validateClaudePluginManifest(plugin: MarketplacePlugin): Promise<void> {
  const manifestPath = path.join(plugin.path, ".claude-plugin/plugin.json");
  const manifest = await readJson(manifestPath);

  if (asString(manifest.name, `${manifestPath}.name`) !== plugin.name) {
    throw new Error(`${manifestPath}.name must match marketplace plugin name '${plugin.name}'`);
  }

  asString(manifest.description, `${manifestPath}.description`);

  if ("version" in manifest) {
    throw new Error(`${manifestPath}.version must be omitted so git commits drive Claude updates`);
  }

  const author = asObject(manifest.author, `${manifestPath}.author`);
  asString(author.name, `${manifestPath}.author.name`);
  asString(manifest.repository, `${manifestPath}.repository`);
  asString(manifest.license, `${manifestPath}.license`);
}

async function validateCodexPluginManifest(plugin: MarketplacePlugin): Promise<void> {
  const manifestPath = path.join(plugin.path, ".codex-plugin/plugin.json");
  const manifest = await readJson(manifestPath);

  if (asString(manifest.name, `${manifestPath}.name`) !== plugin.name) {
    throw new Error(`${manifestPath}.name must match marketplace plugin name '${plugin.name}'`);
  }

  const version = asString(manifest.version, `${manifestPath}.version`);
  if (!SEMVER_PATTERN.test(version)) {
    throw new Error(`${manifestPath}.version must be strict semver for Codex ingestion`);
  }

  asString(manifest.description, `${manifestPath}.description`);

  const author = asObject(manifest.author, `${manifestPath}.author`);
  asString(author.name, `${manifestPath}.author.name`);

  if (manifest.skills !== "./skills/") {
    throw new Error(`${manifestPath}.skills must be './skills/'`);
  }

  const interfaceMetadata = asObject(manifest.interface, `${manifestPath}.interface`);
  for (const field of [
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "websiteURL",
    "privacyPolicyURL",
    "termsOfServiceURL",
  ]) {
    asString(interfaceMetadata[field], `${manifestPath}.interface.${field}`);
  }

  const capabilities = asArray(interfaceMetadata.capabilities, `${manifestPath}.interface.capabilities`);
  if (capabilities.length === 0 || capabilities.some((capability) => typeof capability !== "string")) {
    throw new Error(`${manifestPath}.interface.capabilities must contain strings`);
  }
}

async function validateSkillMirror(): Promise<void> {
  const pluginSkillsDir = path.join(REPO_ROOT, "plugins/k/skills");
  const rootSkillsDir = path.join(REPO_ROOT, "skills");

  if (!(await exists(rootSkillsDir))) {
    throw new Error("root skills/ directory is required for direct skill consumers");
  }

  const rootSkillsStat = await lstat(rootSkillsDir);
  if (!rootSkillsStat.isDirectory()) {
    throw new Error("skills must be a directory");
  }

  const pluginSkillsRealPath = await realpath(pluginSkillsDir);
  const rootSkillNames = (await readdir(rootSkillsDir, { withFileTypes: true }))
    .filter((entry) => !entry.name.startsWith("."))
    .map((entry) => entry.name)
    .sort((left, right) => left.localeCompare(right));
  const pluginSkillNames = (await readdir(pluginSkillsDir, { withFileTypes: true }))
    .filter((entry) => entry.isDirectory() && !entry.name.startsWith("."))
    .map((entry) => entry.name)
    .sort((left, right) => left.localeCompare(right));

  if (rootSkillNames.join("\0") !== pluginSkillNames.join("\0")) {
    throw new Error("root skills/ symlinks must exactly mirror plugins/k/skills/");
  }

  for (const skillName of rootSkillNames) {
    const rootSkillPath = path.join(rootSkillsDir, skillName);
    const rootSkillStat = await lstat(rootSkillPath);
    if (!rootSkillStat.isSymbolicLink()) {
      throw new Error(`skills/${skillName} must be a symlink into plugins/k/skills`);
    }

    const rootSkillRealPath = await realpath(rootSkillPath);
    if (path.dirname(rootSkillRealPath) !== pluginSkillsRealPath) {
      throw new Error(`skills/${skillName} must point into plugins/k/skills`);
    }
  }
}

export async function runMarketplaceValidation(): Promise<number> {
  try {
    const claudeMarketplace = await readJson(CLAUDE_MARKETPLACE_PATH);
    const codexMarketplace = await readJson(CODEX_MARKETPLACE_PATH);
    const claudePlugins = parseClaudeMarketplace(claudeMarketplace);
    const codexPlugins = parseCodexMarketplace(codexMarketplace);

    assertSameMarketplacePlugins(claudePlugins, codexPlugins);

    for (const plugin of claudePlugins) {
      await validatePluginBundle(plugin);
    }

    await validateSkillMirror();
    console.log("Marketplace validation passed.");
    return 0;
  } catch (error: unknown) {
    console.error(error instanceof Error ? error.message : String(error));
    return 1;
  }
}

if (
  process.argv[1] !== undefined &&
  fileURLToPath(import.meta.url) === path.resolve(process.argv[1])
) {
  process.exit(await runMarketplaceValidation());
}
