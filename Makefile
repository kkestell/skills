SKILLS_DIR := $(CURDIR)/skills
CANONICAL_DIR := $(HOME)/.agents/skills
AGENTS := claude-code codex
SKILLS_CLI := npx -y skills@latest

.PHONY: skills

# Sync this repo's skills into Claude Code and Codex: install every skill in
# skills/, then remove any globally installed skill this repo no longer defines.
skills:
	$(SKILLS_CLI) add "$(SKILLS_DIR)" --skill '*' --agent $(AGENTS) --global --yes
	@set -eu; \
	for installed in "$(CANONICAL_DIR)"/*/; do \
		[ -d "$$installed" ] || continue; \
		name=$$(basename "$$installed"); \
		if [ ! -d "$(SKILLS_DIR)/$$name" ]; then \
			echo "Removing skill no longer in this repo: $$name"; \
			$(SKILLS_CLI) remove --skill "$$name" --global --yes; \
		fi; \
	done
