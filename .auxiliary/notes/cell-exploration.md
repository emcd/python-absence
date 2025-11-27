# AbsenceCell Design Exploration

## Summary

The `AbsenceCell` concept is sound and provides genuine ergonomic value. It
addresses real pain points in existing code patterns and bridges nicely with
the Optional/None world from CLI libraries.

**Recommendation: Add AbsenceCell to the absence package.**

## Problem Statement

Consider this pattern from real code:

```python
def _linearize_stacktrace_plain(
    auxdata: TextualizerState,
    stacktrace: __.tb.StackSummary,
    columns_max: __.Absential[ int ] = __.absent,
) -> tuple[ str, ... ]:
    infinite_lines = __.is_absent( columns_max )
    # ...
    if infinite_lines or address_size <= columns_max:
        # ...
    # ...
    __.absent if infinite_lines else columns_max - 4
```

Issues:
1. Intermediate boolean (`infinite_lines`) required
2. Repeated conditional logic patterns
3. Verbose when doing conditional transformations

## Solution: AbsenceCell

A container that wraps `Absential[T]` and provides a richer API:

```python
columns_max: AbsenceCell[int] = AbsenceCell()

# Pattern: if infinite_lines or address_size <= columns_max
if columns_max.evaluate_or_true(lambda n: address_size <= n):
    lines.append(address)

# Pattern: absent if infinite_lines else columns_max - 4
adjusted = columns_max.map(lambda n: n - 4)
```

## Key Design Decisions

### Naming
- **Class**: `AbsenceCell` - "Cell" suggests single-value container, "Absence" 
  connects to package namespace
- **Methods**: `evaluate_or_*`, `extract`, `map`, `is_absent`

### Core API

| Method | Purpose |
|--------|---------|
| `AbsenceCell()` | Create empty cell |
| `AbsenceCell(value)` | Create occupied cell |
| `AbsenceCell.of(value)` | Explicit occupied factory |
| `AbsenceCell.empty()` | Explicit empty factory |
| `AbsenceCell.from_optional(x)` | Bridge from Optional[T] |
| `.is_absent()` / `.is_occupied()` | Predicates |
| `.__bool__()` | Truthy if occupied |
| `.value` | Property for raw `Absential[T]` access |
| `.extract()` | Get value or raise |
| `.extract_or(default)` | Get value or default |
| `.extract_or_compute(factory)` | Get value or compute default |
| `.evaluate_or(func, default)` | Apply func or return default |
| `.evaluate_or_true(predicate)` | Predicate or True |
| `.evaluate_or_false(predicate)` | Predicate or False |
| `.map(func)` | Transform value, preserve absence |
| `.flat_map(func)` | Transform to cell, flatten |
| `.filter(predicate)` | Keep value if predicate true |
| `.or_else(alternative)` | Fallback chain |
| `.to_optional()` | Convert to `T | None` |

### Immutability

The cell is immutable. For mutable needs, users can use a regular variable
holding `Absential[T]`. This matches other packages (frigid, accretive) and
the FP paradigm.

### Integration with is_absent()

**Recommendation**: Don't modify the global `is_absent()` function.

- Keep `is_absent(raw_value)` for raw `Absential[T]` values
- Use `cell.is_absent()` method for cells
- Avoids special-casing and keeps both APIs clean

## TypeIs/TypeGuard Analysis

### What Works

Using `is_present()` with `TypeIs[T]` return type enables proper narrowing:

```python
def is_present(value: Absential[T]) -> TypeIs[T]:
    return value is not absent

# In AbsenceCell methods:
def extract(self) -> T:
    if is_present(self._value):
        return self._value  # Narrowed to T - no type: ignore needed!
    raise ValueError("Cannot extract from absent cell")
```

This eliminates almost all `type: ignore` comments from the implementation.

### What Doesn't Work

Direct truthiness narrowing is not possible:

```python
value: Absential[int] = ...
if value:  # Does NOT narrow to int
    print(value + 1)  # Type error
```

This is because:
1. Type checkers don't track "always falsey" types
2. `int` itself can be falsey (0), so Pyright can't eliminate it
3. `TypeIs[T]` cannot be used as `__bool__` return type (Pyright requires 
   type guards to have input parameters)
4. `Literal[False]` as `__bool__` return doesn't help with narrowing

### Recommendation: Add is_present()

Consider adding to the public API:

```python
def is_present(value: Absential[T]) -> TypeIs[T]:
    '''Check if value is present (not absent).'''
    return value is not absent
```

This enables natural positive-form checks with proper type narrowing:

```python
if is_present(name):
    greet(name)  # name narrowed to str
```

## Remaining type: ignore

Only one `type: ignore` remains, in `from_optional` for the `none_is_absent=False`
case. This is unavoidable because when storing `None` as a value, we pass 
`T | None` to a constructor expecting `Absential[T]`, and there's no way to
express this type relationship.

## CLI Bridge Use Case

The `from_optional` factory elegantly solves the Tyro/CLI adaptation problem:

```python
@dataclass
class UpdateCmd:
    name: str | None = None  # CLI uses None for "not provided"

# Convert to Absential world
name_cell = AbsenceCell.from_optional(cmd.name)
update_user(name=name_cell.value)
```

This is cleaner than the `adapt_dataclass` + TypedDict + cast pattern.

## Implementation Notes

### File Location

Suggest adding to `sources/absence/objects.py` alongside `AbsentSingleton` 
and `AbsenceFactory`, or in a new `sources/absence/cell.py`.

### Dependencies

Only needs:
- Standard library (`typing`, `collections.abc`)
- Internal types (`AbsentSingleton`, `absent`)
- `typing_extensions` for `TypeIs` (if supporting Python < 3.13)

### Testing Considerations

- Test all factory methods
- Test predicates with empty/occupied cells
- Test extraction methods (including exception for `extract()`)
- Test all `evaluate_or_*` variants
- Test `map`, `flat_map`, `filter`
- Test `or_else` chaining
- Test `from_optional` with various None scenarios
- Test equality and hashing
