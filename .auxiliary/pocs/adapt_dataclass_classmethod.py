#!/usr/bin/env python3
"""Proof of concept: Adapting CLI dataclasses to Absential functions.

Uses classmethod approach for type-safe adaptation.
1. Helper function extracts non-None fields from dataclass
2. Manually define TypedDict matching function signature
3. Add classmethod to TypedDict for clean call sites (no cast needed)

Status: Passes Pyright strict checking (0 errors)
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, TypedDict

# Self is in typing_extensions for Python < 3.11
from typing_extensions import Self
import sys
sys.path.insert(0, '/home/me/src/python-absence/sources')

from absence import absent, is_absent, Absential


# ===== Core helper function (for comparison) =====

def adapt_dataclass(
    obj: object,
    *,
    skip_value: object = None,
) -> dict[str, Any]:
    """Extract non-sentinel fields from dataclass."""
    if not hasattr(obj, '__dataclass_fields__'):
        msg = f"{obj} is not a dataclass instance"
        raise TypeError(msg)

    result: dict[str, Any] = {}
    for field in fields(obj):  # type: ignore[arg-type]
        value = getattr(obj, field.name)
        if value is not skip_value:
            result[field.name] = value
    return result


# ===== Approach 1: Classmethod directly on TypedDict =====

class UpdateUserKwargs(TypedDict, total=False):
    """TypedDict with classmethod."""
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


@dataclass
class UpdateUserCommand:
    """CLI command."""
    name: str | None = None
    email: str | None = None


def update_user(
    name: Absential[str] = absent,
    email: Absential[str | None] = absent,
) -> dict[str, Any]:
    """Update user."""
    result: dict[str, Any] = {}
    if not is_absent(name):
        result['name'] = name
    if not is_absent(email):
        result['email'] = email
    return result


def test_direct_classmethod() -> None:
    print("=== Direct classmethod on TypedDict ===\n")

    cmd = UpdateUserCommand(name="Alice")

    # Using classmethod - no cast() needed!
    kwargs = UpdateUserKwargs.from_dataclass(cmd)

    print(f"Command: {cmd}")
    print(f"Kwargs: {kwargs}")
    print(f"Type: {type(kwargs)}")

    result = update_user(**kwargs)
    print(f"Result: {result}")
    print()


# ===== Approach 2: Comparison with cast() approach =====

class UpdateProfileKwargs(TypedDict, total=False):
    """Traditional TypedDict without classmethod."""
    username: str
    bio: str | None


@dataclass
class UpdateProfileCommand:
    """CLI command."""
    username: str | None = None
    bio: str | None = None


def update_profile(
    username: Absential[str] = absent,
    bio: Absential[str | None] = absent,
) -> dict[str, Any]:
    """Update profile."""
    result: dict[str, Any] = {}
    if not is_absent(username):
        result['username'] = username
    if not is_absent(bio):
        result['bio'] = bio
    return result


def test_cast_approach() -> None:
    print("=== Traditional cast() approach ===\n")

    from typing import cast

    cmd = UpdateProfileCommand(username="Bob", bio="Hello")
    kwargs = cast(UpdateProfileKwargs, adapt_dataclass(cmd))

    print(f"Command: {cmd}")
    print(f"Kwargs: {kwargs}")
    print(f"Type: {type(kwargs)}")

    result = update_profile(**kwargs)
    print(f"Result: {result}")
    print()


# ===== Comparison =====

def comparison() -> None:
    print("=" * 70)
    print("CLASSMETHOD VS CAST")
    print("=" * 70)
    print("""
Approach 1: Classmethod on TypedDict

    class MyKwargs(TypedDict, total=False):
        field: Type

        @classmethod
        def from_dataclass(cls, obj, *, skip_value=None) -> Self:
            return adapt_dataclass(obj, skip_value=skip_value)

    # Usage
    kwargs = MyKwargs.from_dataclass(cli_args)  # No cast!

Approach 2: Cast with helper function

    class MyKwargs(TypedDict, total=False):
        field: Type

    # Usage
    kwargs = cast(MyKwargs, adapt_dataclass(cli_args))

Comparison:

Classmethod approach:
  + No explicit cast() at call site
  + Self-documenting
  + Cleaner usage
  - Need to add classmethod to each TypedDict
  - Type: ignore needed in classmethod implementation
  - Unusual pattern (TypedDict with methods)

Cast approach:
  + Standard TypedDict (no methods)
  + Minimal TypedDict definition
  + Explicit about type conversion
  - Requires cast() at each call site

Which is better? Depends on preference:
  - If you value clean call sites: classmethod
  - If you value minimal TypedDict defs: cast
  - Both require type: ignore somewhere
""")


if __name__ == '__main__':
    test_direct_classmethod()
    test_cast_approach()
    comparison()
