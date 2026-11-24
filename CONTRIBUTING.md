# Contributing

## File layout

Each `skills/<skill>/` contains `SKILL.md`, the catalog `references/index.md`, one file per topic at `references/<topic>.md`, and any existing `agents/` and `assets/` files. Keep references inside each skill so they are bundled when installing that skill on its own. The root authoring guides, template, and checker are for this repository, not the installed skill.

| Skill directory | ID prefix | `language` / code tag |
| --- | --- | --- |
| `go-coding-guidelines` | `go` | `go` |
| `rust-coding-guidelines` | `rust` | `rust` |
| `c3-coding-guidelines` | `c3` | `c3` |
| `cpp-coding-guidelines` | `cpp` | `cpp` |
| `develop-readable-typescript` | `typescript` | `typescript` |
| `python-coding-guidelines` | `python` | `python` |
| `kotlin-coding-guidelines` | `kotlin` | `kotlin` |
| `nim-coding-guidelines` | `nim` | `nim` |
| `testing-principles` | `testing` | `any` (no own code tag) |

## Front matter

Start with [the topic template](templates/topic.md). Write content in English. Keep these keys in order:

- `id`: `<prefix>/<topic>`.
- `title`: matches the only H1.
- `summary`: one sentence, 1–200 characters; double-quote the YAML value if it contains a colon.
- `language`: value from the table above.
- `topic`: filename without `.md`, from the topic vocabulary below.
- `tags`: a YAML array of 1–6 tags from the vocabulary below, in flow style (`[a, b]`).
- `related`: a YAML array of topic IDs within this skill, or `[]`.
- `snippets`: always `unverified`. The repository checks document structure, not compilation.

**Topics:** `naming-and-formatting`, `data-and-functions`, `control-flow`, `types`, `null-safety`, `errors`, `modules-and-api`, `abstraction`, `resources-and-memory`, `concurrency`, `unsafe-and-ffi`, `lambdas-and-scope-functions`, `collections-and-idioms`, `testing`, `tooling`, `test-scope`, `test-design`, `test-delivery`. The last three are for `testing-principles` only.

**Tags:** `naming`, `formatting`, `data`, `functions`, `control-flow`, `types`, `null-safety`, `errors`, `result`, `option`, `exceptions`, `modules`, `public-api`, `interfaces`, `generics`, `metaprogramming`, `classes`, `ownership`, `memory`, `resources`, `concurrency`, `async`, `cancellation`, `unsafe`, `ffi`, `lambdas`, `collections`, `testing`, `tooling`, `dependencies`, `build`, `documentation`, `review`.

## Topic structure

Use these exact H2 headings in this order, without duplicates. Omit optional sections that have no useful content. Use unique H3/H4 headings only in `Recommended Pattern` and `Testing`.

| H2 | Required | Content |
| --- | --- | --- |
| `Summary` | Yes | Problem and recommendation in 2–4 sentences. |
| `When to Use` | Yes | Applicability and one alternative case linked to another topic in the skill. |
| `Rules` | Yes | Flat list of normative rules, with the prefixes below. |
| `Dependencies` | No | Third-party packages and the reason for each. |
| `Tooling` | No | Relevant tool configuration; omit in the `tooling` topic. |
| `Recommended Pattern` | Except for `any` | A focused implementation with the code conventions below. |
| `Pitfalls` | Yes | A `Smell / Why / Fix` table with 3–8 data rows. |
| `Testing` | No | How to test the pattern, with a code example; omit in the `testing` topic. |
| `Checklist` | Yes | 4–10 imperative review bullets without rule-level prefixes. |
| `Related` | No | Relative links to topics, each with a one-line reason. |
| `References` | Except for `any` | Links to official sources using HTTPS. |

Preserve existing `**MUST**`, `**SHOULD**`, and `**AVOID**` levels. Mark Kotlin review prompts `**REVIEW SIGNAL**`; they are not requirements. For unlabelled source rules, map prohibitions and explicit requirements to `**MUST**`, avoidances to `**AVOID**`, and preferences and other imperatives to `**SHOULD**`. Put clarifications and exceptions after the flat list in paragraphs beginning `Note:` or `Exceptions:`. Keep distinct normative rules in one topic each; merge duplicates using the more specific wording. Keep workflow, agent conduct, reporting, and a short global rule summary in `SKILL.md`.

## Code conventions

- Tag every fenced block with the skill's code tag or `shell`, `text`, `json`, `toml`, `yaml`, or `cmake`. Keep each block to at most 40 lines.
- Except for `tooling`, the first block in `Recommended Pattern` is a complete source file in the skill's language, including applicable declarations and imports. Start it with a path comment: `# <path>` for Python and Nim, `// <path>` for the other languages. For examples with multiple files, give the paths and explain how the files fit together.
- For `tooling`, use configuration files and shell commands. Put the filename in a path comment when the format permits; for JSON, identify the filename in the preceding sentence.
- Use the shared shop domain: `catalog` for products and lookup, `orders` for order lines, status and shipping, and `billing` for payment boundaries. Express money in integer minor units and use the language's normal casing. Show the language's own failure and absence conventions; do not copy another language's abstraction.
- Check unfamiliar APIs and syntax against the linked references. Document dependency or toolchain requirements. Do not leave placeholders in example code or imply that the structure checker compiles it.

Use the same scenario for a shared topic when it fits the language. Define only the data the example needs; a checked-out application is not a prerequisite.

| Topic | Scenario |
| --- | --- |
| `naming-and-formatting` | Catalog lookup by product ID with a maximum of 50 search results. |
| `data-and-functions` | Sum order-line quantities times their unit prices in a separate calculation. |
| `control-flow` | Label order statuses exhaustively; use guard clauses when shipping is cancelled or the address is absent. |
| `types`, `null-safety` | Represent finite order states, narrow external data, or handle an absent shipping address. |
| `errors` | Apply a discount and distinguish a negative amount from one exceeding the price. Use the language's failure model; Kotlin need not adopt a Result type. |
| `modules-and-api` | Publish one operation for placing an order and keep its helper private. |
| `abstraction` | Model a real payment gateway boundary with one charge operation. |
| `resources-and-memory` | Contrast borrowing and ownership, or show deterministic cleanup for a catalog resource. |
| `concurrency` | Bound concurrent price lookups or batch processing and show how work completes or is cancelled. |
| `unsafe-and-ffi` | Show a narrow native boundary with explicit safety and lifetime contracts. |
| `lambdas-and-scope-functions`, `collections-and-idioms` | Configure a request, select active products, or separate collection transforms from side effects. |
| `testing` | Exercise discount success, the exact-price boundary, and the two expected failure cases. |
| `tooling` | Show the existing standard's configuration and verification commands. |

## Links and catalogs

Use relative links within the skill. Refer to independently installed skills by name, not by relative link. Update `references/index.md` with exactly one row per topic: `Doc | Summary | Topic | Tags`. Link the title to `<topic>.md`, copy the front matter summary, and put the topic and comma-separated tags in inline code. Match the catalog title `# <Display> Topic Index`.

Run `bash scripts/check-topics.sh` from the repository root before committing. See [mq recipes](AGENTS.md#mq-queries) for retrieval checks.
