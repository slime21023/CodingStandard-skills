---
id: rust/tooling
title: "Dependencies and CI"
summary: "Keep checks and dependencies compatible with the actual supported targets."
language: rust
topic: tooling
tags: [tooling, dependencies, build]
related: [rust/testing]
snippets: unverified
---

# Dependencies and CI

## Summary

Keep checks and dependencies compatible with the actual supported targets. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for dependency management and verification. For testing, see [Testing](testing.md).

## Rules

- **SHOULD** Prefer std before a crate; assess need, security, maintenance, license, MSRV, features, and transitive cost.
- **SHOULD** Enable only necessary features; avoid uncontrolled Git or path dependencies, wildcard versions, and duplicate functionality.
- **SHOULD** Commit Cargo.lock by default for applications and libraries; separately exercise compatible dependency updates for libraries.
- **MUST** Never edit Cargo.lock manually or globally silence lints to pass CI.
- **SHOULD** Test updates and feature combinations that are supported. Use --all-features only if all features can coexist.
- **SHOULD** Validate declared MSRV and claimed targets, including no_std where relevant.
- **SHOULD** Justify scoped lint exceptions and optimize on measurements.

## Recommended Pattern

Use a real package manifest and adapt flags to the workspace.

```toml
# Cargo.toml
[package]
name = "shop"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"
```

```shell
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo doc --workspace --no-deps
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| All features assumed compatible | Can exercise impossible configurations | Test supported combinations |
| Latest toolchain only | Fails to confirm declared MSRV | Check the actual minimum |
| Broad allow on warnings | Hides independent defects | Scope the exception with a reason |

## Checklist

- Scrutinize each added dependency.
- Check declared MSRV and supported features.
- Run formatting, lint, tests, and docs as applicable.
- Report checks and limitations accurately.

## References

- [Cargo Book](https://doc.rust-lang.org/stable/cargo/)
- [Clippy](https://doc.rust-lang.org/clippy/)
