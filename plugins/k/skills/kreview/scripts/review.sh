#!/usr/bin/env bash
set -euo pipefail

OPENCODE_PERMISSION='{"edit":"deny","bash":"deny","read":"allow","glob":"allow","grep":"allow","skill":"allow"}' \
  opencode run --command "/kreview $*"
