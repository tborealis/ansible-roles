#!/usr/bin/env bash
# Cut a release: promote the CHANGELOG.md [Unreleased] section to a dated version
# heading and bump galaxy.yml to match. Does not commit, branch, push, or tag.
#
# Usage:
#   scripts/cut-release.sh vX.Y.Z
#
# Then:
#   git switch -c release/vX.Y.Z
#   git add galaxy.yml CHANGELOG.md
#   git commit -m "Release vX.Y.Z"
#   # open a PR, merge to main, then:
#   git tag vX.Y.Z && git push origin vX.Y.Z

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

VERSION=${1:-}
[[ "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Version must look like vX.Y.Z" >&2; exit 2; }

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree is not clean. Commit or stash first." >&2
  exit 1
fi

PLAIN=${VERSION#v}
DATE=$(date +%F)

grep -qE '^## \[Unreleased\]' CHANGELOG.md || { echo "No '## [Unreleased]' section in CHANGELOG.md" >&2; exit 1; }

echo "Bumping galaxy.yml to $PLAIN"
sed -i.bak -E "s/^version:.*/version: $PLAIN/" galaxy.yml
rm -f galaxy.yml.bak

echo "Promoting [Unreleased] to [$PLAIN] - $DATE in CHANGELOG.md"
sed -i.bak -E "s/^## \[Unreleased\].*/## [Unreleased]\n\n## [$PLAIN] - $DATE/" CHANGELOG.md
rm -f CHANGELOG.md.bak

cat <<EOF

Release $VERSION staged in galaxy.yml and CHANGELOG.md. Next:

  git switch -c release/$VERSION
  git add galaxy.yml CHANGELOG.md
  git commit -m "Release $VERSION"
  # open a PR, merge to main, then tag main:
  git tag $VERSION && git push origin $VERSION
EOF
