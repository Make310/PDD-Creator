#!/usr/bin/env bash
set -e

echo "Setting up PDD Creator dev environment..."

# Git hooks
git config core.hooksPath scripts/hooks
echo "✓ Git hooks configured"

# Make hooks executable
chmod +x scripts/hooks/pre-commit
chmod +x scripts/hooks/pre-push
chmod +x scripts/hooks/post-merge
echo "✓ Hooks made executable"

echo ""
echo "Setup complete. Install dependencies in each module:"
echo "  cd api && uv sync"
echo "  cd worker && uv sync"
