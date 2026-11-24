---
id: go/testing
title: "Testing"
summary: "Test behavior and inspectable failure categories."
language: go
topic: testing
tags: [testing, errors]
related: [go/errors]
snippets: unverified
---

# Testing

## Summary

Test behavior and inspectable failure categories. Table-driven tests work well when each case follows the same observable contract.

## When to Use

Use this after changing behavior or fixing a defect. For errors, see [Errors](errors.md).

## Rules

- **SHOULD** Test business rules, edge cases, and error paths with testing; use table-driven tests where helpful.
- **SHOULD** Run go test -race for relevant concurrency and consider fuzzing parsers and untrusted inputs.
- **AVOID** Avoid arbitrary coverage targets, brittle full-error-text assertions, and unrelated changes.

## Recommended Pattern

Save the test beside `discount.go` from [Errors](errors.md#recommended-pattern), then run `go test ./...`.

```go
// orders/discount_test.go
package orders

import (
    "errors"
    "testing"
)

func TestApplyDiscount(t *testing.T) {
    product := Product{ID: "p1", PriceCents: 500}
    tests := []struct {
        name string
        amountCents int64
        wantCents int64
        wantErr error
    }{
        {"partial discount", 200, 300, nil},
        {"full discount", 500, 0, nil},
        {"negative amount", -1, 0, ErrNegativeAmount},
        {"above price", 501, 0, ErrExceedsPrice},
    }
    for _, test := range tests {
        t.Run(test.name, func(t *testing.T) {
            got, err := ApplyDiscount(product, test.amountCents)
            if !errors.Is(err, test.wantErr) {
                t.Fatalf("error = %v; want %v", err, test.wantErr)
            }
            if err == nil && got.PriceCents != test.wantCents {
                t.Fatalf("price = %d; want %d", got.PriceCents, test.wantCents)
            }
        })
    }
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Error message assertion | Breaks on harmless context changes | Assert errors.Is |
| Only successful case | Misses contract boundaries | Include exact price and invalid inputs |
| Uncontrolled goroutine ordering | Makes tests flaky | Synchronize the test explicitly |

## Checklist

- Check the successful partial discount.
- Check the exact-price boundary.
- Check both invalid discount categories.
- Use the race detector for shared-state changes.

## References

- [Package testing](https://pkg.go.dev/testing)
- [Go race detector](https://go.dev/doc/articles/race_detector)
