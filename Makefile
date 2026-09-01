SKILLS_DIR := $(CURDIR)/skills
CANONICAL_DIR := $(HOME)/.agents/skills
AGENTS := claude-code codex
SKILLS_CLI := npx -y skills@latest

# Agent profiles to sync, as <Claude Code config dir>:<Codex home> pairs. The
# work machine has the Star Tribune profiles alongside the personal ones; the
# home machine has only the personal ones.
PERSONAL_PROFILE := $(HOME)/.claude:$(HOME)/.codex
STRIB_PROFILE := $(HOME)/.claude-strib:$(HOME)/.codex-strib

.PHONY: skills-home skills-work

# Sync every skill in skills/ into the profiles in $(1), then remove any globally
# installed skill this repo no longer defines. Skills under wip/ are unfinished
# and deliberately left out.
#
# The skills CLI keeps one copy in $(CANONICAL_DIR), symlinks it into each Claude
# Code profile, and lets Codex read $(CANONICAL_DIR) directly. Per-profile
# isolation therefore does not exist for Codex: every skill installed here is
# visible from every profile.
define sync_skills
@set -eu; \
for profile in $(1); do \
	claude_dir=$${profile%%:*}; codex_dir=$${profile#*:}; \
	echo "Installing skills into $$claude_dir and $$codex_dir"; \
	CLAUDE_CONFIG_DIR="$$claude_dir" CODEX_HOME="$$codex_dir" \
		$(SKILLS_CLI) add "$(SKILLS_DIR)" --skill '*' --agent $(AGENTS) --global --yes; \
done; \
for installed in "$(CANONICAL_DIR)"/*/; do \
	[ -d "$$installed" ] || continue; \
	name=$$(basename "$$installed"); \
	if [ ! -d "$(SKILLS_DIR)/$$name" ]; then \
		echo "Removing skill no longer in this repo: $$name"; \
		for profile in $(1); do \
			claude_dir=$${profile%%:*}; codex_dir=$${profile#*:}; \
			CLAUDE_CONFIG_DIR="$$claude_dir" CODEX_HOME="$$codex_dir" \
				$(SKILLS_CLI) remove --skill "$$name" --global --yes; \
		done; \
	fi; \
done
endef

# Home machine: personal Claude Code and Codex profiles only.
skills-home:
	$(call sync_skills,$(PERSONAL_PROFILE))

# Work machine: personal and Star Tribune Claude Code and Codex profiles.
skills-work:
	$(call sync_skills,$(PERSONAL_PROFILE) $(STRIB_PROFILE))
