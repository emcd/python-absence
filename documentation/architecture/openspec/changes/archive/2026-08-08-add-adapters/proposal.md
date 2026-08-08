# Change: Add Dataclass Adaptation Helper

## Why

CLI frameworks like Tyro use `None` for "not provided" arguments, while
absence-based APIs use the `absent` sentinel. Until Tyro supports non-`None`
sentinels natively (see [tyro#382](https://github.com/brentyi/tyro/issues/382)),
users need a helper to bridge CLI dataclass instances to `Absential[T]`
function parameters by stripping fields that match a skip value.

## What Changes

- Add `adapt_dataclass()` function to `sources/absence/adapters.py`
- Extracts fields from a dataclass instance, omitting fields whose value
  matches a configurable skip value (default: `None`)
- Returns `dict[str, Any]` for use with TypedDict + `cast()` at call sites

## Impact

- Affected specs: New `dataclass-adapters` capability
- Affected code: New `sources/absence/adapters.py`, `sources/absence/__init__.py`
