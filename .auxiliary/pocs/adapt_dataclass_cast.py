#!/usr/bin/env python3
"""Proof of concept: Adapting CLI dataclasses to Absential functions.

Uses cast() approach for type-safe adaptation.
1. Helper function extracts non-None fields from dataclass
2. Manually define TypedDict matching function signature
3. Use cast() at call site to provide type safety

Status: Passes Pyright strict checking (0 errors)
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, TypedDict, cast
import sys
sys.path.insert(0, '/home/me/src/python-absence/sources')

from absence import absent, is_absent, Absential


# ===== The core helper function (truly Pyright-clean) =====

def adapt_dataclass(
    obj: object,
    *,
    skip_value: object = None,
) -> dict[str, Any]:
    """Adapt a dataclass instance to a dict, skipping sentinel values.

    Extracts non-sentinel fields from a dataclass instance. The caller
    should use cast() to convert to a specific TypedDict type.

    Args:
        obj: Dataclass instance to adapt
        skip_value: Value to skip when extracting fields (default: None)

    Returns:
        Dictionary mapping field names to values (excluding skip_value fields)

    Raises:
        TypeError: If obj is not a dataclass instance

    Example:
        >>> @dataclass
        ... class UpdateCommand:
        ...     name: str | None = None
        ...     email: str | None = None
        >>>
        >>> class UpdateKwargs(TypedDict, total=False):
        ...     name: str
        ...     email: str
        >>>
        >>> cmd = UpdateCommand(name="Alice")
        >>> result = adapt_dataclass(cmd)
        >>> kwargs = cast(UpdateKwargs, result)  # Cast at call site
    """
    if not hasattr(obj, '__dataclass_fields__'):
        msg = f"{obj} is not a dataclass instance"
        raise TypeError(msg)

    result: dict[str, Any] = {}
    for field in fields(obj):  # type: ignore[arg-type]
        value = getattr(obj, field.name)
        if value is not skip_value:
            result[field.name] = value

    return result


# ===== Example usage =====

def update_user(
    name: Absential[str] = absent,
    email: Absential[str | None] = absent,
    age: Absential[int | None] = absent,
) -> dict[str, Any]:
    """Update user with partial data."""
    result: dict[str, Any] = {}
    if not is_absent(name):
        result['name'] = name
    if not is_absent(email):
        result['email'] = email
    if not is_absent(age):
        result['age'] = age
    return result


class UpdateUserKwargs(TypedDict, total=False):
    """Type-safe kwargs for update_user.

    Manually maintained to match function signature.
    """
    name: str
    email: str | None
    age: int | None


@dataclass
class UpdateUserCommand:
    """CLI command for update_user."""
    name: str | None = None
    email: str | None = None
    age: int | None = None


# Type-safe adapter wrapper - cast happens here
def adapt_update_user_cmd(cmd: UpdateUserCommand) -> UpdateUserKwargs:
    """Adapt UpdateUserCommand to UpdateUserKwargs."""
    return cast(UpdateUserKwargs, adapt_dataclass(cmd))


def test_basic() -> None:
    print("=== Basic usage (truly Pyright-clean) ===\n")

    cmd = UpdateUserCommand(name="Alice", age=30)
    kwargs = adapt_update_user_cmd(cmd)  # Pyright knows: UpdateUserKwargs
    result = update_user(**kwargs)

    print(f"Command: {cmd}")
    print(f"Kwargs: {kwargs}")
    print(f"Result: {result}")
    print()


# ===== Inline cast variant (also works) =====

def test_inline_cast() -> None:
    print("=== Inline cast (also Pyright-clean) ===\n")

    cmd = UpdateUserCommand(email="bob@example.com")

    # Cast directly at the call site
    kwargs = cast(UpdateUserKwargs, adapt_dataclass(cmd))
    result = update_user(**kwargs)

    print(f"Command: {cmd}")
    print(f"Kwargs: {kwargs}")
    print(f"Result: {result}")
    print()


# ===== Larger example =====

def update_profile(
    username: Absential[str] = absent,
    email: Absential[str | None] = absent,
    age: Absential[int | None] = absent,
    bio: Absential[str | None] = absent,
    verified: Absential[bool] = absent,
) -> dict[str, Any]:
    """Update user profile."""
    result: dict[str, Any] = {}
    if not is_absent(username):
        result['username'] = username
    if not is_absent(email):
        result['email'] = email
    if not is_absent(age):
        result['age'] = age
    if not is_absent(bio):
        result['bio'] = bio
    if not is_absent(verified):
        result['verified'] = verified
    return result


class UpdateProfileKwargs(TypedDict, total=False):
    """Type-safe kwargs for update_profile."""
    username: str
    email: str | None
    age: int | None
    bio: str | None
    verified: bool


@dataclass
class UpdateProfileCommand:
    """CLI command for update_profile."""
    username: str | None = None
    email: str | None = None
    age: int | None = None
    bio: str | None = None
    verified: bool | None = None


def adapt_update_profile_cmd(cmd: UpdateProfileCommand) -> UpdateProfileKwargs:
    """Adapt UpdateProfileCommand to UpdateProfileKwargs."""
    return cast(UpdateProfileKwargs, adapt_dataclass(cmd))


def test_larger() -> None:
    print("=== Larger example (Pyright-clean) ===\n")

    cmd = UpdateProfileCommand(username="charlie", age=30, verified=True)
    kwargs = adapt_update_profile_cmd(cmd)
    result = update_profile(**kwargs)

    print(f"Command: {cmd}")
    print(f"Kwargs: {kwargs}")
    print(f"Result: {result}")
    print()


# ===== Custom sentinel example =====

class UnsetSentinel:
    """Custom sentinel for 'not provided'."""
    def __repr__(self) -> str:
        return 'UNSET'

UNSET = UnsetSentinel()


@dataclass
class AdvancedCommand:
    """Command that distinguishes None from not-provided."""
    name: str | None | UnsetSentinel = UNSET
    clear_email: bool = False


class AdvancedKwargs(TypedDict, total=False):
    """Kwargs for advanced command."""
    name: str | None
    clear_email: bool


def adapt_advanced_cmd(cmd: AdvancedCommand) -> AdvancedKwargs:
    """Adapt AdvancedCommand using UNSET as skip value."""
    return cast(AdvancedKwargs, adapt_dataclass(cmd, skip_value=UNSET))


def test_custom_sentinel() -> None:
    print("=== Custom sentinel (Pyright-clean) ===\n")

    # None is a real value, UNSET means omit
    cmd = AdvancedCommand(name=None, clear_email=True)
    kwargs = adapt_advanced_cmd(cmd)

    print(f"Command: {cmd}")
    print(f"Kwargs: {kwargs}")
    print("Note: name=None is included (not skipped)")
    print()


# ===== Without TypedDict (simpler but less type-safe) =====

def test_without_typeddict() -> None:
    print("=== Without TypedDict (simpler, less type-safe) ===\n")

    cmd = UpdateUserCommand(name="Diana")
    kwargs = adapt_dataclass(cmd)  # Just dict[str, Any]
    result = update_user(**kwargs)

    print(f"Command: {cmd}")
    print(f"Kwargs: {kwargs}")
    print(f"Result: {result}")
    print()


def summary() -> None:
    print("=" * 70)
    print("TRULY PYRIGHT-CLEAN SOLUTION")
    print("=" * 70)
    print("""
The core helper function:

    def adapt_dataclass(
        obj: object,
        *,
        skip_value: object = None,
    ) -> dict[str, Any]:
        '''Extract non-sentinel fields from dataclass.'''
        # ... implementation
        return result

Key insight: cast() must happen at the CALL SITE, not inside the function.

Usage pattern:

    # 1. Define TypedDict (manual, unavoidable)
    class MyKwargs(TypedDict, total=False):
        field1: Type1
        field2: Type2

    # 2. Define typed adapter with cast at call site
    def adapt_my_cmd(cmd: MyCommand) -> MyKwargs:
        return cast(MyKwargs, adapt_dataclass(cmd))

    # 3. Use it
    kwargs = adapt_my_cmd(cli_args)
    my_function(**kwargs)

OR inline:

    kwargs = cast(MyKwargs, adapt_dataclass(cli_args))
    my_function(**kwargs)

This passes Pyright strict checking because:
  ✓ Function returns concrete dict[str, Any]
  ✓ cast() happens at call site with literal type
  ✓ No type variables in function signature
  ✓ All annotations are concrete types

Benefits:
  ✓ Automatic field inspection
  ✓ Type-safe when used with TypedDict + cast
  ✓ Works with custom sentinels
  ✓ Passes strict Pyright checking (verified outside .auxiliary)
  ✓ Minimal boilerplate

Limitation:
  ✗ Still need to manually define TypedDict
    (unavoidable for static type checking)
""")


if __name__ == '__main__':
    test_basic()
    test_inline_cast()
    test_larger()
    test_custom_sentinel()
    test_without_typeddict()
    summary()
