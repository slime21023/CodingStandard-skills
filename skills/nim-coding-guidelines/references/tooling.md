---
id: nim/tooling
title: "Checks and Dependencies"
summary: "Run semantic and compile checks on each relevant entry point."
language: nim
topic: tooling
tags: [tooling, dependencies, build]
related: [nim/testing]
snippets: unverified
---

# Checks and Dependencies

## Summary

Run semantic and compile checks on each relevant entry point. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for build, dependency, and delivery work. For testing, see [Testing](testing.md).

## Rules

- **MUST** Check all relevant entry points and use the project's supported Nim and configuration.
- **MUST** Do not hide warnings, skip necessary tests, or weaken checks to get a passing build.
- **SHOULD** Lock the tested dependency version; an unconstrained requires line is not a lock.
- **SHOULD** Use a release entry for an executable and a meaningful test or example entry for a library.

Note: `--styleCheck:error` checks compiler-enforced identifier style, not every rule in this skill.

## Recommended Pattern

Adapt paths to the actual package and retain its dependency workflow.

```shell
nim check --styleCheck:error src/shop.nim
nimble test
nim c -d:release src/main.nim
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Only checks a leaf module | May miss entry-point integration | Exercise all public entry points |
| Assumes requires pins a version | Builds can resolve differently | Use the project lock mechanism |
| StyleCheck treated as full review | Checks limited compiler style rules | Apply topic rules in review |

## Checklist

- Check project and Nimble configuration.
- Use the supported minimum compiler.
- Compile the relevant library or executable entry.
- Report which checks actually ran.

## References

- [Nim compiler options](https://nim-lang.org/docs/nimc.html)
- [Nimble](https://nim-lang.github.io/nimble/)
