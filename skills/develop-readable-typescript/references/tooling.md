---
id: typescript/tooling
title: "Tooling Baseline"
summary: "Keep TypeScript and lint checks explicit and project-aware."
language: typescript
topic: tooling
tags: [tooling, formatting, testing]
related: [typescript/testing]
snippets: unverified
---

# Tooling Baseline

## Summary

Keep TypeScript and lint checks explicit and project-aware. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for project tooling or a standalone TypeScript file. For testing and comments, see [Testing and Comments](testing.md).

## Rules

- **SHOULD** Use **Prettier** for uniform formatting.
- **SHOULD** Use **ESLint + typescript-eslint** for code quality checks. Start from `recommendedTypeChecked`; teams comfortable with TypeScript can then consider `strictTypeChecked`.
- **SHOULD** Prioritize checks for unsafe `any`, unhandled Promises, unused variables, and unnecessary type assertions.
- **SHOULD** CI should run at least the TypeScript typecheck, ESLint, the Prettier check, and tests.
- **SHOULD** If a tool rule conflicts with readability, adjust it explicitly as a team rather than disabling rules widely in code.
- **MUST** Without a project configuration, run tsc --strict --noEmit (or bunx tsc --strict --noEmit) against the changed files.

## Recommended Pattern

Integrate these settings into the project's `tsconfig.json`.

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| No config and no checks | Leaves type errors unobserved | Use strict no-emit mode |
| Untyped lint rules only | Misses promise and unsafe type errors | Use typed lint rules |
| Global rule disable | Hides unrelated defects | Agree on narrowly scoped exceptions |

## Checklist

- Inspect existing scripts before running them.
- Retain project compiler options.
- Run typecheck, lint, format checks, and tests as applicable.
- Report failed or unavailable checks.

## References

- [TSConfig reference](https://www.typescriptlang.org/tsconfig/)
- [Typed linting](https://typescript-eslint.io/getting-started/typed-linting/)
- [Prettier versus linters](https://prettier.io/docs/comparison)
