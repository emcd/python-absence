# Change: Add `is_present()` Predicate

## Why

The current API provides `is_absent()` for checking if a value is the global
absent sentinel, but lacks a positive-form predicate. Users must write
`not is_absent(value)` which:
- Requires a negation for the common "value is present" check
- Does not enable type narrowing (TypeIs only works in the positive form)
- Leads to `type: ignore` comments when working with `Absential[T]` values

## What Changes

- Add `is_present(value)` function to `sources/absence/objects.py`
- Returns `TypeIs[T]` to enable type narrowing
- Equivalent to `value is not absent`

## Impact

- Affected specs: `type-safety`
- Affected code: `sources/absence/objects.py`, `sources/absence/__init__.py`
