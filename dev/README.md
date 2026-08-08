# Development environment

This directory contains the shared development image and small workflow
scripts. It should describe a reproducible toolchain, not hold source code or
machine-specific editor settings.

Use Docker Compose from the repository root:

```bash
docker compose -f dev/compose.yaml build
docker compose -f dev/compose.yaml run --rm lab
```

Inside the container, run `dev/scripts/check.sh` to configure, build, and test.
