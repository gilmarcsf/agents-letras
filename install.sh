#!/bin/zsh
set -euo pipefail

AGENTS="$(cd "$(dirname "$0")" && pwd)"
AGENTS_HOME="$HOME/.agents"
path=("$HOME/.local/bin" "$HOME/.local/share/mise/shims" "/opt/homebrew/bin" $path)
export PATH

# Create or replace a symlink target. If a real file already exists, keep a
# timestamped backup so the installer is reversible.
link() {
  local source="$1" target="$2"

  mkdir -p "$(dirname "$target")"

  if [[ -L "$target" && "$(readlink "$target")" == "$source" ]]; then
    echo "  [ok] $target"
    return 0
  fi

  if [[ -e "$target" ]]; then
    local backup="$target.bak.$(date +%s)"
    mv "$target" "$backup"
    echo "  [backup] $target → $backup"
  fi

  ln -sf "$source" "$target"
  echo "  [link] $target → $source"
}

sync_skills() {
  if ! command -v skills &>/dev/null; then
    echo "skills CLI is required for the full setup. Install it first, or copy skills manually." >&2
    return 1
  fi

  skills --config "$AGENTS/skills.toml" sync --apply
  link "$AGENTS/.runtime/skills" "$AGENTS_HOME/skills"
}

# Run repo Python helpers with whichever modern Python is available.
run_python_script() {
  if python3 -c "import tomllib" &>/dev/null; then
    python3 "$@"
    return
  fi

  if command -v uv &>/dev/null; then
    uv run python "$@"
    return
  fi

  if [[ -x /opt/homebrew/bin/mise ]]; then
    /opt/homebrew/bin/mise exec -- uv run python "$@"
    return
  fi

  echo "python3 with tomllib or uv is required to run $1" >&2
  return 1
}

link_codex_skills() {
  local source_root="$AGENTS_HOME/skills"
  local target_root="$HOME/.codex/skills"

  mkdir -p "$target_root"

  for existing in "$target_root"/*(N); do
    if [[ -L "$existing" ]]; then
      if [[ "$(readlink "$existing")" == "$source_root"/* && ! -e "$(readlink "$existing")" ]]; then
        rm "$existing"
        echo "  [clean] $existing"
      fi
    fi
  done

  for skill in "$source_root"/*(N); do
    link "$skill" "$target_root/${skill:t}"
  done
}

unlink_managed_codex_prompts() {
  local target="$HOME/.codex/prompts"
  local source="$AGENTS_HOME/codex/prompts"

  if [[ -L "$target" && "$(readlink "$target")" == "$source" ]]; then
    rm "$target"
    echo "  [clean] $target"
  fi
}

configure_git_hooks() {
  if git -C "$AGENTS" rev-parse --is-inside-work-tree &>/dev/null; then
    git -C "$AGENTS" config core.hooksPath .githooks
    echo "  [git] core.hooksPath = .githooks"
  fi
}

echo "agents installer"
echo "================"

# Hub links. Tools point to ~/.agents so the repo can move later without
# rewriting every tool-specific config path.
echo "\n~/.agents/"
link "$AGENTS/AGENTS.md" "$AGENTS_HOME/AGENTS.md"
link "$AGENTS/agents"    "$AGENTS_HOME/agents"
link "$AGENTS/codex"     "$AGENTS_HOME/codex"
link "$AGENTS/claude"    "$AGENTS_HOME/claude"

echo "\nskills"
link "$AGENTS/skills.toml" "$HOME/.config/skills/skills.toml"
sync_skills

echo "\nCodex plugins"
run_python_script "$AGENTS/scripts/sync-codex-plugins.py" --apply

# Tool configs that consume the hub. Machine-specific state stays outside the
# repo.
echo "\ntool configs"
link "$AGENTS_HOME/codex/config.toml"   "$HOME/.codex/config.toml"
link "$AGENTS_HOME/codex/rules/default.rules" "$HOME/.codex/rules/default.rules"
unlink_managed_codex_prompts
link "$AGENTS_HOME/codex/agents"        "$HOME/.codex/agents"
link "$AGENTS_HOME/claude/settings.json" "$HOME/.claude/settings.json"
link "$AGENTS_HOME/claude/claude.json"  "$HOME/.claude.json"
link "$AGENTS_HOME/AGENTS.md"           "$HOME/.codex/AGENTS.md"
link "$AGENTS_HOME/AGENTS.md"           "$HOME/.claude/CLAUDE.md"
link "$AGENTS_HOME/agents"              "$HOME/.claude/agents"
link "$AGENTS_HOME/skills"              "$HOME/.claude/skills"
link_codex_skills

echo "\ngit hooks"
configure_git_hooks

echo "\nDone."
