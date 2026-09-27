#!/bin/bash
# Lanza cada encargo en orden y espera a que termine antes del siguiente.
cd "$(dirname "$0")/../.."
C=~/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/codex-companion.mjs
for f in "$@"; do
  id=$(node $C task --background --write --fresh --effort medium < "$f" 2>&1 | grep -o 'task-[a-z0-9-]*' | head -1)
  echo "== $f -> $id"
  for i in $(seq 1 60); do
    node $C status $id --cwd . 2>&1 | grep -qE "\| (completed|failed|cancelled) \|" && break
    sleep 20
  done
  node $C status $id --cwd . 2>&1 | sed -n '3,4p'
done
