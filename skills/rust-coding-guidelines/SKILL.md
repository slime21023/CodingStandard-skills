---
name: rust-coding-guidelines
description: Apply clear, idiomatic Rust 2024+ Stable coding standards when creating, editing, refactoring, testing, reviewing, or designing Rust (.rs) code, Cargo packages, modules, public APIs, ownership, traits, errors, unsafe code, and async/concurrency. Favor data and functions, explicit borrowing, concrete types, minimal APIs, and readable Code Agent output.
---

# Rust Coding Guidelines

Apply the following standards to Rust work. Follow explicit user requirements and existing supported project constraints first. For detailed edge cases, read `references/full-guidelines.md`.

## Workflow

1. Inspect relevant code, `Cargo.toml`, the project edition, MSRV, features, dependencies, and existing tests before changing anything.
2. Make the smallest coherent change. Preserve public compatibility and established project conventions unless the requested task explicitly changes them.
3. Use idiomatic Rust with clear, unambiguous names. Follow `rustfmt` rather than personal formatting preferences.
4. Add or update focused tests. Run the applicable checks and report exactly which ones passed or could not run.

## Language and organization

- For new projects, use Rust 2024 Edition and Stable Rust. Declare the actual supported `rust-version`; Rust 2024 requires at least Rust 1.85. Do not add nightly-only features.
- Prefer `struct` / `enum` plus functions. Put type-specific behavior in `impl`. Keep modules small and capability-focused; do not add layered architectures or crates speculatively.
- Default to private APIs; use `pub(crate)` for necessary crate-internal sharing and `pub` only for intentional external contracts.
- Use standard naming: `PascalCase` for types, traits and variants, `snake_case` for modules/functions/variables, `SCREAMING_SNAKE_CASE` for constants. Avoid cryptic abbreviations.
- Prefer early returns, `?`, and straightforward branches over deep nesting or overly long combinator chains.

## Ownership and abstraction

- Borrow first: use `&T`, `&mut T`, `&str`, and `&[T]` where appropriate. Use owned `T`, `String`, or `Vec<T>` when data must be retained, transferred, or outlive the caller.
- Do not clone merely to appease the borrow checker. Permit justified clones when they simplify correct lifetime or ownership design. Avoid complex lifetimes solely to eliminate allocations.
- Prefer concrete types. Introduce traits, generics, `impl Trait`, or `dyn Trait` only for actual shared behavior, generic algorithms, extension contracts, or runtime polymorphism.
- Prefer standard traits (`From`, `TryFrom`, `AsRef`, `Debug`, etc.) where they naturally express the API. Do not create one trait per struct or speculative mock abstractions.
- Do not default to `Rc`, `Arc`, `RefCell`, or `Mutex` without a genuine shared-state or ownership requirement.

## Errors

- Use `Result<T, E>` for recoverable errors and `Option<T>` for normal absence; propagate with `?` and retain useful error sources.
- Library public APIs expose meaningful typed errors. Prefer the standard library; use `thiserror` when deriving error implementations reduces meaningful boilerplate.
- Application boundaries may use `anyhow` for contextual diagnostics. Do not unnecessarily leak `anyhow::Error` as a public library contract.
- Never silently discard errors, flatten them all into strings, or hide failures through unconditional defaults.
- Avoid `unwrap()` in production paths. Use `expect()` only for a justified invariant with a meaningful explanation; do not panic for normal user input or I/O failure.

## Async, concurrency, and unsafe

- Use synchronous code by default. Choose async for substantial concurrent I/O, and suitable thread pools or parallel execution for CPU-bound work.
- Let the application own its async runtime. Keep core library logic independent from a specific runtime when practical.
- Bound concurrency and queues; establish task ownership, completion, cancellation, timeouts, and shutdown behavior. Prefer ownership transfer or channels to shared mutable state.
- Do not hold synchronous mutex guards across `.await` or block an async executor with lengthy synchronous work.
- Prefer Safe Rust. Use `unsafe` only for a justified low-level requirement. Minimize each block, explain soundness with `// SAFETY:`, document `unsafe fn` contracts under `# Safety`, and test/review the invariants.
- Never use raw pointers, `transmute`, or `unsafe` to evade a normal ownership or type-design problem.

## Tests, dependencies, and quality

- Test success cases, expected errors, and boundaries. Keep unit tests near code, integration tests under `tests/`, and useful public examples as doctests. Add regression tests for fixes.
- In concurrency code, cover cancellation, completion, timeouts, and resource limits without fragile timing assumptions.
- Prefer `std` before another crate; justify dependency scope, maintenance, license, MSRV, features, and transitive cost. Commit `Cargo.lock` by default; do not edit it manually.
- Run, as applicable:

  ```bash
  cargo fmt --all -- --check
  cargo clippy --workspace --all-targets -- -D warnings
  cargo test --workspace
  cargo doc --workspace --no-deps
  ```

- Verify relevant feature combinations separately. Use `--all-features` only when they can be enabled together. Validate claimed MSRV and additional targets when relevant.
- Scoped lint exceptions require justification; never disable checks globally just to pass CI. Optimize performance only from relevant measurements.

## Mandatory Code Agent conduct

- Avoid unrequested refactors, speculative layers, excessive traits or generics, unnecessary crates, and `async` without a concrete requirement.
- Favor descriptive names, shallow control flow, explicit error handling, and understandable types over terse or clever code.
- Do not cure compiler errors with gratuitous `clone()`, `Arc<Mutex<_>>`, or `unsafe`.
- Explain any new dependency, unsafe invariant, runtime coupling, or deliberate public API change.
- Never claim formatting, Clippy, tests, or build passed unless actually executed; report limitations clearly.
