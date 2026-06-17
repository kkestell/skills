import assert from "node:assert/strict";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  ParseError,
  readProperties,
  toPrompt,
  validate,
} from "../scripts/lib/skills-ref.js";

async function createSkill(
  rootDir: string,
  dirName: string,
  contents: string,
  fileName = "SKILL.md",
): Promise<string> {
  const skillDir = path.join(rootDir, dirName);
  await mkdir(skillDir, { recursive: true });
  await writeFile(path.join(skillDir, fileName), contents);
  return skillDir;
}

test("validate accepts a minimal valid skill", async (t) => {
  const rootDir = await mkdtemp(path.join(os.tmpdir(), "agent-skills-test."));
  t.after(async () => {
    await rm(rootDir, { recursive: true, force: true });
  });

  const skillDir = await createSkill(
    rootDir,
    "my-skill",
    `---
name: my-skill
description: A test skill
---
Body
`,
  );

  assert.deepEqual(await validate(skillDir), []);
});

test("validate rejects unexpected fields", async (t) => {
  const rootDir = await mkdtemp(path.join(os.tmpdir(), "agent-skills-test."));
  t.after(async () => {
    await rm(rootDir, { recursive: true, force: true });
  });

  const skillDir = await createSkill(
    rootDir,
    "my-skill",
    `---
name: my-skill
description: A test skill
unexpected: true
---
Body
`,
  );

  assert.match(
    (await validate(skillDir))[0] ?? "",
    /Unexpected fields in frontmatter: unexpected/,
  );
});

test("validate supports lowercase unicode names after normalization", async (t) => {
  const rootDir = await mkdtemp(path.join(os.tmpdir(), "agent-skills-test."));
  t.after(async () => {
    await rm(rootDir, { recursive: true, force: true });
  });

  const skillDir = await createSkill(
    rootDir,
    "café",
    `---
name: cafe\u0301
description: Unicode test
---
Body
`,
  );

  assert.deepEqual(await validate(skillDir), []);
});

test("readProperties stringifies metadata values", async (t) => {
  const rootDir = await mkdtemp(path.join(os.tmpdir(), "agent-skills-test."));
  t.after(async () => {
    await rm(rootDir, { recursive: true, force: true });
  });

  const skillDir = await createSkill(
    rootDir,
    "my-skill",
    `---
name: my-skill
description: A test skill
metadata:
  version: 1
---
Body
`,
    "skill.md",
  );

  const properties = await readProperties(skillDir);
  assert.equal(properties.name, "my-skill");
  assert.deepEqual(properties.metadata, { version: "1" });
});

test("toPrompt renders the available_skills XML block", async (t) => {
  const rootDir = await mkdtemp(path.join(os.tmpdir(), "agent-skills-test."));
  t.after(async () => {
    await rm(rootDir, { recursive: true, force: true });
  });

  const skillDir = await createSkill(
    rootDir,
    "my-skill",
    `---
name: my-skill
description: A <test> skill & example
---
Body
`,
  );

  const prompt = await toPrompt([skillDir]);
  assert.match(prompt, /<available_skills>/);
  assert.match(prompt, /A &lt;test&gt; skill &amp; example/);
  assert.match(prompt, /<location>/);
});

test("parse errors are surfaced through validate", async (t) => {
  const rootDir = await mkdtemp(path.join(os.tmpdir(), "agent-skills-test."));
  t.after(async () => {
    await rm(rootDir, { recursive: true, force: true });
  });

  const skillDir = await createSkill(
    rootDir,
    "my-skill",
    `name: my-skill
description: Missing frontmatter fences
`,
  );

  assert.deepEqual(await validate(skillDir), [
    "SKILL.md must start with YAML frontmatter (---)",
  ]);

  await assert.rejects(
    async () => {
      await readProperties(skillDir);
    },
    (error: unknown) => error instanceof ParseError,
  );
});
