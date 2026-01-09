#!/usr/bin/env sh
set -e
chmod +x gradlew
exec gradle "$@"
