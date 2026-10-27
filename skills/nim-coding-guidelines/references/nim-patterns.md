# Nim Patterns and Checks

Use these examples only when the task involves new package structure, public APIs, expected errors, or test setup. Adapt names and paths; do not add a template structure to an existing simple package without need.

## Feature-oriented package

```text
project/
├── project.nimble
├── src/
│   ├── project.nim
│   └── project/
│       ├── users.nim
│       └── storage.nim
└── tests/
    ├── t_users.nim
    └── t_storage.nim
```

Minimal Nimble settings:

```nim
srcDir = "src"
requires "nim >= 2.2"
requires "results"
```

Use a dependency lockfile or another explicit project mechanism for a tested dependency version. Do not claim that adding an unconstrained dependency pins its version.

## Minimal API and typed expected failures

```nim
# src/project/users.nim
import results

type
  UserError* {.pure.} = enum
    EmptyName

  User* = object
    name*: string

func createUser*(name: string): Result[User, UserError] =
  ## Create a user or return a validation error.
  if name.len == 0:
    return Result[User, UserError].err(UserError.EmptyName)

  Result[User, UserError].ok(User(name: name))
```

```nim
# src/project.nim
import project/users

export users.User, users.UserError, users.createUser
```

Callers that inspect the Result using its helper API should also import `results`. In new code, prefer an error enum or domain-specific type over parsing error messages.

### Missing values are not failures

```nim
import std/options

func findName(names: openArray[string]; target: string): Option[string] =
  for name in names:
    if name == target:
      return some(name)

  none(string)
```

Use `Option` for an ordinary empty search result. Reserve `Result` for an operation that can genuinely fail.

### Convert exceptions at an adapter boundary

```nim
import results

type
  FileError {.pure.} = enum
    CannotRead

proc loadText(path: string): Result[string, FileError] =
  try:
    return Result[string, FileError].ok(readFile(path))
  except IOError, OSError:
    return Result[string, FileError].err(FileError.CannotRead)
```

Catch the smallest meaningful exception set. Keep unexpected exceptions visible; never catch `Defect` merely to return a regular validation error. If operational diagnostics matter, preserve relevant context in a richer error type.

## Style and behavior checks

- Before patching, inspect the existing tests, exports and Nimble options.
- Add test cases for success, expected failure and edge cases. Use `std/unittest` by default.
- For a simple project, build checks may be:

```sh
nim check --styleCheck:error src/project.nim
nimble test
nim c -d:release src/main.nim
```

Adapt commands to actual entry points and run each meaningful entry. For pure libraries, use an example or test entry instead of inventing `src/main.nim`.

- `--styleCheck:error` checks compiler-enforced identifier style; it does not automatically enforce every rule in this skill.
- `{.raises: [].}` can support exception guarantees on suitable synchronous code; it does not provide the same guarantee for `std/asyncdispatch` async procedures.
- Await or explicitly supervise Futures. For `std/asyncdispatch`, use `asyncCheck` rather than `discard` when intentional background tasks must report failure.

## Authoritative references

- [Nim style guide (NEP-1)](https://nim-lang.org/docs/nep1.html)
- [Nim manual](https://nim-lang.org/docs/manual.html)
- [Nim memory management](https://nim-lang.org/docs/mm.html)
- [Compiler options](https://nim-lang.org/docs/nimc.html)
- [Nimble](https://nim-lang.github.io/nimble/)
- [nim-results](https://github.com/arnetheduck/nim-results)
