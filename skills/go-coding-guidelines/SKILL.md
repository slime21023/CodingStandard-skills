---
name: go-coding-guidelines
description: Apply idiomatic, concise Go coding standards when creating, modifying, refactoring, testing, or reviewing Go (.go) code, and when designing Go packages, struct and method APIs, interfaces, error handling, or concurrency. Favor data and functions, concrete types, simple packages, explicit errors, and readable Code Agent output.
---

# Go Coding Guidelines

Create simple, explicit and maintainable Go code. Follow the user's accepted decisions: **data and independent functions first; interfaces only when necessary; package design starts simple and grows by real functionality**. This skill applies to implementation and code review, not to a mandatory project architecture.

## Workflow

1. Inspect repository instructions, `go.mod`, relevant package boundaries, nearby code and tests. Follow existing contracts and local conventions unless the user asks to change them.
2. Choose the least complex solution that meets the task: concrete structs/functions first; methods for type-owned behavior or state; small consumer-owned interfaces only for a real substitution boundary.
3. Make focused changes. Preserve unrelated code, public behavior and dependencies unless the user explicitly requests expansion.
4. Handle errors, cancellation, resource lifetimes and concurrency explicitly. Add or update meaningful tests for changed behavior.
5. Format changed `.go` files with `gofmt`. When feasible, run `go vet ./...` and `go test ./...`; use `go test -race ./...` for relevant concurrent code. State which checks ran and any limitations.
6. Before delivery, run the review checklist below. Explain any justified departure from SHOULD/AVOID recommendations.

**Review-only or diagnosis requests do not authorize edits.** For those tasks, report grounded findings in severity order and cite file locations; keep optional style observations separate from correctness issues.

## Rule levels

- **MUST:** Non-negotiable for applicable code: correctness, explicit errors, properly synchronized shared state, safe lifetimes and Go formatting.
- **SHOULD:** Default approach; depart only for a concrete benefit or repository convention.
- **AVOID:** Not the default; use only if task constraints justify the extra complexity.

## 1. Naming and formatting

- **MUST** use `gofmt`. Use Go visibility and casing conventions: exported `PascalCase`, unexported `camelCase`; preserve common initialisms, e.g. `userID` and `HTTPClient`.
- **SHOULD** use concise lowercase package names without underscores. Avoid redundant repetition between package and symbol (`user.New` rather than `user.NewUser`).
- **SHOULD** balance clarity with scope. Short Go idioms (`i`, `err`, `ctx`, `db`, `r`, `w`, short receivers) are acceptable when obvious; longer scopes need meaningful names.
- **AVOID** cryptic abbreviations, excessive verbosity and meaningless `common`, `util` or `helpers` packages.

## 2. Structs, functions, and methods

- **SHOULD** represent data and necessary state using `struct`; favor independent functions for transformations not tied to internal state.
- **SHOULD** use methods when behavior naturally belongs to a type, mutates state, preserves invariants, manages a resource or implements an interface.
- **SHOULD** use value receivers for suitable small, value-like types and pointer receivers for mutation or noncopyable state such as mutexes; be consistent per type.
- **SHOULD** leverage meaningful zero values. Introduce constructors only for actual initialization, validation or resource acquisition.
- **AVOID** automatic getters, setters or constructors for every field, hidden global mutable state and unnecessary indirection.

## 3. Interfaces and packages

- **MUST** prefer concrete types until an actual consumer needs a behavioral contract.
- **SHOULD** keep interfaces small and define them near their consumers. Implementations normally return concrete types.
- **SHOULD** organize packages around capabilities or functional responsibilities. Start small; split only when real boundaries emerge. Use `internal/` to protect implementation details where valuable.
- **SHOULD** prefer the standard library when sufficient and keep exported APIs minimal.
- **AVOID** one-interface-per-struct patterns, `IUserService`, `UserServiceImpl`, speculative adapters, mandatory `handler/service/repository` layers and circular imports.

## 4. Functions and flow control

- **SHOULD** give each function a clear responsibility and favor guard clauses/early return to keep the main path shallow.
- **SHOULD** use `switch` for clear multiple branches; omit an `else` after a terminating branch.
- **AVOID** deep nesting, opaque compound conditions, unrelated boolean mode flags, arbitrary function length quotas and named/naked returns without a clarity benefit.

## 5. Error handling

- **MUST** use the native `(T, error)` convention for ordinary failure. Do not invent a generic `Result[T]` framework to mirror another language.
- **MUST** deliberately handle or propagate errors. Never discard errors merely for shorter code.
- **SHOULD** add operation context with `fmt.Errorf`; use `%w` only when exposing the wrapped error to callers is appropriate. Use `errors.Is` and `errors.As` for inspectable errors.
- **SHOULD** use lowercase error text (except proper nouns), usually without terminal punctuation.
- **AVOID** routine business `panic`, fragile error-string comparisons, swallowing errors, and logging plus returning the same error redundantly at every layer.

## 6. Context, concurrency and resources

- **MUST** ensure each goroutine has a clear owner, termination/completion strategy and suitable cancellation or joining. Synchronize access to shared mutable state.
- **SHOULD** pass request-scoped `context.Context` explicitly as the first parameter of I/O functions; do not routinely store it in structs.
- **SHOULD** bound concurrency and resource usage. Use channels for communication/coordination and mutexes for direct shared-state protection as the problem warrants.
- **SHOULD** release resources promptly, e.g. files and HTTP response bodies; check `Close`/flush errors when they affect correctness.
- **AVOID** speculative goroutines, channels, worker pools or performance optimization without evidence.

## 7. Tests and documentation

- **MUST** format touched code and run applicable checks when the environment permits. If blocked, clearly report what was not verified.
- **SHOULD** test business rules, edge cases and error paths with Go's `testing` package, often using table-driven tests. Run `go test -race` for relevant concurrency and consider fuzzing parsers or untrusted input.
- **SHOULD** document exported APIs and explain non-obvious invariants and why decisions were made rather than restating statements.
- **AVOID** chasing coverage percentages without useful tests, brittle full-error-text assertions, or broad unrelated refactoring.

## Code Agent quality checklist

- [ ] Are identifiers readable without unnecessary abbreviation?
- [ ] Is normal control flow shallow and focused?
- [ ] Are concrete structs/functions used without unneeded interfaces, constructors or architecture layers?
- [ ] Are relevant errors handled and wrapped deliberately?
- [ ] Do goroutines, shared state, contexts and resources have safe lifetimes?
- [ ] Are package boundaries meaningful and edits within scope?
- [ ] Were suitable formatting/tests/checks actually run and honestly reported?

## Pattern

Prefer a concrete data transformation and native error:

```go
var ErrInvalidDiscount = errors.New("invalid discount")

type Product struct {
    ID    string
    Price int64
}

func ApplyDiscount(product Product, amount int64) (Product, error) {
    if product.Price < 0 || amount < 0 || amount > product.Price {
        return Product{}, fmt.Errorf("discount product %s: %w", product.ID, ErrInvalidDiscount)
    }
    product.Price -= amount
    return product, nil
}
```

The snippet assumes the `errors` and `fmt` imports; domain code must separately specify monetary units and invariants. Do not add a `ProductService` interface for this transformation without an actual consumer need.

## Official reference points

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go Module Layout](https://go.dev/doc/modules/layout)
- [Go Error Wrapping](https://go.dev/blog/go1.13-errors)
- [Race Detector](https://go.dev/doc/articles/race_detector)
- [Google Go Style Guide](https://google.github.io/styleguide/go/)
