---
id: rust/resources-and-memory
title: "Ownership and Borrowing"
summary: "Borrow when a caller retains ownership, and take values when ownership must move."
language: rust
topic: resources-and-memory
tags: [ownership, memory, resources]
related: [rust/data-and-functions]
snippets: unverified
---

# Ownership and Borrowing

## Summary

Borrow when a caller retains ownership, and take values when ownership must move. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when signatures transfer or retain data. For data, functions, and control flow, see [Data, Functions, and Control Flow](data-and-functions.md).

## Rules

- **SHOULD** Borrow with &T, &mut T, &str, or &[T] where appropriate.
- **SHOULD** Use owned T, String, or Vec<T> to retain, transfer, or outlive a caller's data.
- **MUST** Do not clone merely to appease the borrow checker; clones are appropriate for a clearly owned or simpler correct design.
- **SHOULD** Let the compiler infer lifetimes except where the type relationship requires annotation.
- **AVOID** Do not introduce Rc, Arc, RefCell, or Mutex without a genuine sharing need, or complicate lifetimes solely to avoid allocations.

## Recommended Pattern

```rust
// src/orders/invoice.rs
pub struct OrderLine {
    pub quantity: i64,
    pub unit_price_cents: i64,
}

pub struct Order {
    pub id: String,
    pub lines: Vec<OrderLine>,
}

pub struct Invoice {
    pub order_id: String,
    pub total_cents: i64,
}

pub fn order_total_cents(lines: &[OrderLine]) -> i64 {
    lines.iter().map(|line| line.quantity * line.unit_price_cents).sum()
}

pub fn into_invoice(order: Order) -> Invoice {
    let total_cents = order_total_cents(&order.lines);
    Invoice { order_id: order.id, total_cents }
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Clone before reading | Allocates without ownership need | Borrow the slice |
| Owned result storing a caller borrow | Couples result lifetime to caller | Take ownership where required |
| Shared lock by default | Adds synchronization and complexity | Establish one owner |

## Checklist

- Borrow for read-only access.
- Move data that the result will retain.
- Use lifetime elision when sufficient.
- Justify every clone or sharing primitive.

## References

- [Understanding ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)
