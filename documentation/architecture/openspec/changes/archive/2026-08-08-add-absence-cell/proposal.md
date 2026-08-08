# Change: Add AbsenceCell Container

## Why

Working with `Absential[T]` values requires intermediate booleans and repeated
conditional logic. Real-world code shows patterns like:

```python
infinite_lines = is_absent(columns_max)
if infinite_lines or address_size <= columns_max:
    ...
absent if infinite_lines else columns_max - 4
```

An `AbsenceCell` container would provide a richer API for these patterns:

```python
cell = AbsenceCell( columns_max )
if cell.evaluate_or_true( lambda n: address_size <= n ):
    ...
adjusted = cell.transform( lambda n: n - 4 )
```

## What Changes

- Add `AbsenceCell` class to `sources/absence/cell.py`
- Immutable container wrapping `Absential[T]`
- Rich API: `transform`, `evaluate_or`, `evaluate_or_true`, `evaluate_or_false`, `extract`, `extract_or`, `extract_or_compute`, `or_else`, `to_optional`, `from_optional`
- Bridges `Optional[T]` (CLI) to `Absential[T]` via `from_optional`

## Impact

- Affected specs: New `absence-cell` capability
- Affected code: New `sources/absence/cell.py`, `sources/absence/__init__.py`
