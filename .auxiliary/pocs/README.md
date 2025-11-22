# Proof of Concept: CLI-to-Absential Adaptation

This directory contains proof-of-concept implementations for adapting CLI dataclasses (using `None` for absent values) to functions with `Absential` parameters.

## Problem

When using Tyro for CLI generation:
- CLI dataclasses use `None` to represent "not provided" (Tyro-compatible)
- Internal functions use `Absential[T]` with `absent` sentinel
- Need to convert between these two representations

## Solutions

### 1. Cast Approach (`adapt_dataclass_cast.py`)

Uses `cast()` at call sites for type safety.

```python
class MyKwargs(TypedDict, total=False):
    field: Type

# Usage
kwargs = cast(MyKwargs, adapt_dataclass(cli_args))
my_function(**kwargs)
```

**Pros:** Minimal TypedDict, standard pattern
**Cons:** Requires `cast()` at each call site

### 2. Classmethod Approach (`adapt_dataclass_classmethod.py`)

Adds `from_dataclass()` classmethod to TypedDict.

```python
class MyKwargs(TypedDict, total=False):
    field: Type

    @classmethod
    def from_dataclass(cls, obj, *, skip_value=None) -> Self:
        return adapt_dataclass(obj, skip_value=skip_value)  # type: ignore

# Usage
kwargs = MyKwargs.from_dataclass(cli_args)  # No cast!
my_function(**kwargs)
```

**Pros:** Cleaner call sites, self-documenting
**Cons:** More code per TypedDict, unconventional pattern

## Key Insight

Both approaches require manually defining TypedDict to match function signatures. This duplication is unavoidable for static type checking—type checkers need literal type definitions and can't extract `Absential[T] → T` at analysis time.

## Verification

Both implementations pass Pyright strict checking (0 errors) when tested outside the `.auxiliary` directory.

## See Also

- `.auxiliary/notes/cli-to-absential-adaptation.md` - Detailed analysis and recommendations
