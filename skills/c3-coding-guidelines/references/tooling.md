---
id: c3/tooling
title: "Dependencies and Checks"
summary: "Keep C3 dependencies pinned and check the actual build targets."
language: c3
topic: tooling
tags: [tooling, dependencies, build]
related: [c3/testing]
snippets: unverified
---

# Dependencies and Checks

## Summary

Keep C3 dependencies pinned and check the actual build targets. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when building, validating, or managing dependencies. For testing, see [Testing](testing.md).

## Rules

- **SHOULD** Prefer the standard library. Keep third-party dependencies minimal, justified, pinned, and compatible with the compiler.
- **SHOULD** Typical project checks are: c3c build; c3c test; c3c build release. Adapt to actual targets.
- **MUST** Do not silence warnings, weaken checks, or claim success to conceal failures.
- **SHOULD** Benchmark or profile before making readability-reducing performance changes.

## Recommended Pattern

Use the pinned compiler and adapt the target name to the project’s `project.json`.

```shell
c3c build
c3c test
c3c build release
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Latest nightly replaces the pin | Changes language and library assumptions | Use the verified stable project release |
| Safety checks disabled for delivery | Conceals lifetime errors | Keep checks and address the defect |
| Performance change without baseline | Makes results impossible to assess | Measure and compare |

## Checklist

- Confirm the compiler and actual build targets.
- Prefer and inspect standard-library facilities first.
- Justify and pin third-party dependencies.
- Run available builds and tests and report real results.

## References

- [C3 build commands](https://c3-lang.org/build-your-project/build-commands/)
- [C3 language and releases](https://c3-lang.org/)
