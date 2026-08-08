#!/usr/bin/env bash

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
compose=(
  docker compose
  --file "$repo_dir/dev/compose.yaml"
)

usage() {
  cat <<'EOF'
Usage: dev/dev.sh <command> [arguments...]

Commands:
  build             Build the development image.
  start             Start the development container in the background.
  exec [command...] Execute a command in the running container (default: bash).
  help              Show this help message.

Examples:
  dev/dev.sh build
  dev/dev.sh start
  dev/dev.sh exec
  dev/dev.sh exec dev/scripts/check.sh
EOF
}

command="${1:-help}"

case "$command" in
  build)
    "${compose[@]}" build
    ;;
  start)
    "${compose[@]}" up --detach lab
    ;;
  exec)
    shift
    if (($# == 0)); then
      set -- bash
    fi
    "${compose[@]}" exec lab "$@"
    ;;
  help | --help | -h)
    usage
    ;;
  *)
    printf 'Unknown command: %s\n\n' "$command" >&2
    usage >&2
    exit 2
    ;;
esac
