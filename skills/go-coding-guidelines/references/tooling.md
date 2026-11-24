---
id: go/tooling
title: "Formatting and Checks"
summary: "Format changed Go files and run checks relevant to the change."
language: go
topic: tooling
tags: [formatting, tooling, testing]
related: [go/testing]
snippets: unverified
---

# Formatting and Checks

## Summary

Format changed Go files and run checks relevant to the change. Use the project module and supported toolchain, and state any limits.

## When to Use

Use this before handing off changes. For testing, see [Testing](testing.md).

## Rules

- **MUST** Format touched .go files with gofmt.
- **MUST** Run applicable checks when possible and explain what was not verified.
- **SHOULD** Run go vet ./... and go test ./... when feasible; use go test -race ./... for relevant concurrent changes.

## Recommended Pattern

```shell
gofmt -w orders/discount.go orders/discount_test.go
go vet ./...
go test ./...
# For changes involving concurrent access:
go test -race ./...
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Formatting unrelated packages | Widens the patch | Format touched files |
| Vet only for behavior changes | Static analysis does not execute tests | Run relevant tests too |
| Unreported race-check limitations | Creates false confidence | State what ran and what did not |

## Checklist

- Check the target go.mod and existing scripts.
- Format touched source files.
- Run relevant vet and test commands.
- Report unavailable checks without claiming success.

## References

- [Command gofmt](https://pkg.go.dev/cmd/gofmt)
- [Go command](https://go.dev/cmd/go/)
- [Go race detector](https://go.dev/doc/articles/race_detector)
