# CLI-to-Absential Adaptation

## Overview

Explored solutions for adapting CLI dataclasses (using `None` for absent values) to functions with `Absential` parameters, addressing:
1. Automatic field inspection (no manual dict building)
2. Type safety (TypedDict support)

## The Problem

When using Tyro for CLI generation:
- CLI dataclasses use `None` to represent "not provided" (Tyro-compatible)
- Internal functions use `Absential[T]` with `absent` sentinel
- Need to convert between these representations with type safety

## Solution: Two Approaches

Both approaches require:
- Helper function: `adapt_dataclass(obj, *, skip_value=None) -> dict[str, Any]`
- Manually defined TypedDict matching function signatures

**Key constraint:** TypedDict must be manually defined (unavoidable for static type checking—type checkers need literal type definitions and can't extract `Absential[T] → T` at analysis time).

### Approach 1: Classmethod on TypedDict ✅

Add a `classmethod` to `TypedDict` to eliminate explicit `cast()`.

```python
from typing import TypedDict
from typing_extensions import Self

class UpdateUserKwargs(TypedDict, total=False):
    """TypedDict with built-in adapter."""
    name: str
    email: str | None

    @classmethod
    def from_dataclass(
        cls,
        obj: object,
        *,
        skip_value: object = None,
    ) -> Self:
        """Create from dataclass instance."""
        return adapt_dataclass(obj, skip_value=skip_value)  # type: ignore[return-value]

# Usage
cmd = UpdateUserCommand(name="Alice")
kwargs = UpdateUserKwargs.from_dataclass(cmd)  # No cast() needed!
update_user(**kwargs)
```

**Pros:**
- ✅ No explicit `cast()` at call sites
- ✅ Self-documenting (method shows intent)
- ✅ Cleaner usage
- ✅ Encapsulates adaptation logic

**Cons:**
- ❌ Need `type: ignore` in classmethod implementation
- ❌ Must add classmethod to each TypedDict
- ❌ Unconventional (TypedDict with methods is unusual)
- ❌ More code per TypedDict (+4 lines)

### Approach 2: Cast at Call Site

Use standard TypedDict with explicit `cast()`.

```python
class UpdateUserKwargs(TypedDict, total=False):
    name: str
    email: str | None

# Usage
kwargs = cast(UpdateUserKwargs, adapt_dataclass(cli_args))
update_user(**kwargs)
```

**Pros:**
- ✅ Standard TypedDict (just fields)
- ✅ Minimal TypedDict definition
- ✅ Explicit about type conversion
- ✅ Separation of concerns

**Cons:**
- ❌ Requires `cast()` at each call site
- ❌ More verbose at usage

## Code Size Comparison

### Example: 3-field TypedDict

**Classmethod:**
```python
class UpdateKwargs(TypedDict, total=False):
    name: str
    email: str | None
    age: int | None

    @classmethod
    def from_dataclass(cls, obj, *, skip_value=None) -> Self:
        return adapt_dataclass(obj, skip_value=skip_value)  # type: ignore

# Usage (multiple places in code)
kwargs = UpdateKwargs.from_dataclass(cmd)
kwargs2 = UpdateKwargs.from_dataclass(cmd2)
```

**Cast:**
```python
class UpdateKwargs(TypedDict, total=False):
    name: str
    email: str | None
    age: int | None

# Usage (multiple places in code)
kwargs = cast(UpdateKwargs, adapt_dataclass(cmd))
kwargs2 = cast(UpdateKwargs, adapt_dataclass(cmd2))
```

- Lines saved at definition: **-4 lines** (classmethod is more verbose)
- Lines saved per usage: **+1 line** (no cast needed)
- **Break-even point: 4+ usages per TypedDict**

## Recommendations

### Use Classmethod When:
- ✅ TypedDict will be used in multiple places (4+ call sites)
- ✅ You value clean, intent-revealing call sites
- ✅ You don't mind unconventional TypedDict usage
- ✅ You want adaptation logic encapsulated

### Use Cast When:
- ✅ TypedDict is used in 1-3 places
- ✅ You prefer standard TypedDict (just fields)
- ✅ You value minimal definitions
- ✅ You want explicit type conversion

### Hybrid Approach for Library

Provide **both options** in the `absence` library:

1. **Helper function** for cast approach:
   ```python
   def adapt_dataclass(obj, *, skip_value=None) -> dict[str, Any]:
       """Extract non-sentinel fields from dataclass."""
       ...
   ```

2. **Base class** for classmethod approach:
   ```python
   class AbsentialKwargs(TypedDict, total=False):
       @classmethod
       def from_dataclass(cls, obj, *, skip_value=None) -> Self:
           return adapt_dataclass(obj, skip_value=skip_value)  # type: ignore
   ```

Then users choose:

**Option A (Cast):**
```python
class MyKwargs(TypedDict, total=False):
    field: Type

kwargs = cast(MyKwargs, adapt_dataclass(cmd))
```

**Option B (Classmethod via inheritance):**
```python
class MyKwargs(AbsentialKwargs, total=False):
    field: Type

kwargs = MyKwargs.from_dataclass(cmd)
```

## Key Findings

1. **Both approaches work and pass Pyright strict checking** (verified ✅)
2. **TypedDict must be manually defined** (unavoidable for static type checking)
3. **Classmethod eliminates explicit cast()** at call sites
4. **Trade-off:** Classmethod adds code to TypedDict but cleans up usage
5. **Break-even:** Classmethod worth it at 4+ usages per TypedDict

## Implementation Files

### Proof of Concept Implementations
- **`.auxiliary/pocs/README.md`** - Overview of POC implementations
- **`.auxiliary/pocs/adapt_dataclass_cast.py`** - Cast approach demo (✅ Pyright clean)
- **`.auxiliary/pocs/adapt_dataclass_classmethod.py`** - Classmethod approach demo (✅ Pyright clean)

### Experimental Files
Additional exploration files in `.auxiliary/scribbles/`:
- Various iteration attempts
- Alternative approaches explored
- Intermediate summaries

These can be reviewed later or cleaned up as needed.

## Next Steps

When ready to add to the library:
- Implement `adapt_dataclass(obj, *, skip_value=None) -> dict[str, Any]` helper function
- Optionally provide `AbsentialKwargs` base class for classmethod approach
- Let users choose their preferred pattern based on use case
- Document both approaches with examples

## Opinion

Both approaches are valid. For the library:
- **Provide** the `adapt_dataclass()` function
- **Let users choose** classmethod or cast based on preference

The classmethod approach is clever and cleaner at call sites, but unconventional. The cast approach is more explicit and standard. For critical interfaces with many call sites, the classmethod is worth it. For simple cases, cast is fine.
