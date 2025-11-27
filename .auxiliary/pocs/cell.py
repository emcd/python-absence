#!/usr/bin/env python3
"""AbsenceCell implementation using is_present() for type narrowing.

This version eliminates type: ignore comments by using a TypeIs predicate.

Status: Passes Pyright strict checking (0 errors, 1 type: ignore for edge case)
"""

from __future__ import annotations

from typing import TypeVar, Generic, Callable, overload
from typing_extensions import TypeIs

# ============================================================================
# Absence types
# ============================================================================

class AbsentSingleton:
    _instance: AbsentSingleton | None = None
    
    def __new__(cls) -> AbsentSingleton:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __bool__(self) -> bool:
        return False
    
    def __repr__(self) -> str:
        return 'absent'

absent = AbsentSingleton()

T = TypeVar('T')
U = TypeVar('U')
Absential = T | AbsentSingleton


# ============================================================================
# Type guard predicates
# ============================================================================

def is_absent(value: Absential[T]) -> TypeIs[AbsentSingleton]:
    """Check if value is absent. Narrows type in both branches."""
    return value is absent


def is_present(value: Absential[T]) -> TypeIs[T]:
    """Check if value is present. Narrows to T when True."""
    return value is not absent


def _is_not_none(value: T | None) -> TypeIs[T]:
    """Check if value is not None. Used for from_optional narrowing."""
    return value is not None


# ============================================================================
# AbsenceCell
# ============================================================================

class AbsenceCell(Generic[T]):
    """Container for potentially absent values.
    
    Provides a rich API for working with potentially absent values,
    reducing boilerplate around absence checking and conditional logic.
    
    Similar in spirit to Option/Maybe monads, but integrated with the
    absence package's paradigm where `absent` is distinct from `None`.
    
    Uses is_present() TypeIs predicate for type narrowing, eliminating
    the need for type: ignore comments in most methods.
    
    Examples:
        # Create cells
        empty = AbsenceCell()              # or AbsenceCell.empty()
        filled = AbsenceCell(42)           # or AbsenceCell.of(42)
        from_opt = AbsenceCell.from_optional(maybe_none)
        
        # Check state
        if cell:  # truthy if occupied
        if cell.is_absent():
        if cell.is_occupied():
        
        # Extract values
        value = cell.extract()             # raises if absent
        value = cell.extract_or(default)   # returns default if absent
        
        # Transform (returns new cell)
        new_cell = cell.map(lambda x: x * 2)
        
        # Evaluate with default
        result = cell.evaluate_or(lambda x: x > 0, default=True)
        fits = columns_max.evaluate_or_true(lambda n: size <= n)
    """
    
    __slots__ = ('_value',)
    
    def __init__(self, value: Absential[T] = absent) -> None:
        self._value: Absential[T] = value
    
    # -------------------------------------------------------------------------
    # Factory Methods
    # -------------------------------------------------------------------------
    
    @classmethod
    def of(cls, value: T) -> AbsenceCell[T]:
        """Create an occupied cell containing the given value."""
        return cls(value)
    
    @classmethod
    def empty(cls) -> AbsenceCell[T]:
        """Create an empty (absent) cell."""
        return cls(absent)
    
    @overload
    @classmethod
    def from_optional(cls, value: T | None) -> AbsenceCell[T]: ...
    
    @overload
    @classmethod
    def from_optional(cls, value: T | None, *, none_is_absent: bool) -> AbsenceCell[T] | AbsenceCell[T | None]: ...
    
    @classmethod
    def from_optional(cls, value: T | None, *, none_is_absent: bool = True) -> AbsenceCell[T] | AbsenceCell[T | None]:
        """Create a cell from an Optional[T] value.
        
        By default, None is treated as absent. This is the common case when
        bridging from CLI libraries like Tyro that use None for omitted args.
        
        Args:
            value: The optional value.
            none_is_absent: If True (default), None becomes empty cell.
                           If False, None is stored as a value.
        """
        if none_is_absent:
            if _is_not_none(value):
                return cls(value)  # Narrowed to T by TypeIs
            return cls(absent)
        # When none_is_absent=False, None is a valid value to store
        # We need ignore here because T|None can't narrow to exclude None
        return cls(value)  # type: ignore[arg-type]
    
    # -------------------------------------------------------------------------
    # Predicates
    # -------------------------------------------------------------------------
    
    def is_absent(self) -> bool:
        """Return True if the cell is empty (contains no value)."""
        return self._value is absent
    
    def is_occupied(self) -> bool:
        """Return True if the cell contains a value."""
        return self._value is not absent
    
    def __bool__(self) -> bool:
        """Return True if the cell is occupied. Allows `if cell:` checks."""
        return self._value is not absent
    
    # -------------------------------------------------------------------------
    # Value Access
    # -------------------------------------------------------------------------
    
    @property
    def value(self) -> Absential[T]:
        """Access the raw contained value (which may be absent).
        
        Use this when you need to pass the value to functions expecting
        Absential[T].
        """
        return self._value
    
    def extract(self) -> T:
        """Extract the contained value, raising if absent.
        
        Raises:
            ValueError: If the cell is absent.
        """
        if is_present(self._value):
            return self._value  # Narrowed to T by TypeIs
        raise ValueError("Cannot extract from absent cell")
    
    def extract_or(self, default: T) -> T:
        """Extract the value if occupied, otherwise return the default."""
        if is_present(self._value):
            return self._value  # Narrowed to T by TypeIs
        return default
    
    def extract_or_compute(self, factory: Callable[[], T]) -> T:
        """Extract the value if occupied, otherwise compute a default."""
        if is_present(self._value):
            return self._value  # Narrowed to T by TypeIs
        return factory()
    
    # -------------------------------------------------------------------------
    # Evaluation Methods
    # -------------------------------------------------------------------------
    
    def evaluate_or(self, func: Callable[[T], U], default: U) -> U:
        """Apply func to the value if occupied, else return default."""
        if is_present(self._value):
            return func(self._value)  # Narrowed to T by TypeIs
        return default
    
    def evaluate_or_true(self, predicate: Callable[[T], bool]) -> bool:
        """Apply predicate if occupied, else return True.
        
        Useful for constraints where absence means "no constraint".
        
        Example:
            if columns_max.evaluate_or_true(lambda n: address_size <= n):
                lines.append(address)
        """
        return self.evaluate_or(predicate, True)
    
    def evaluate_or_false(self, predicate: Callable[[T], bool]) -> bool:
        """Apply predicate if occupied, else return False."""
        return self.evaluate_or(predicate, False)
    
    # -------------------------------------------------------------------------
    # Transformation Methods
    # -------------------------------------------------------------------------
    
    def map(self, func: Callable[[T], U]) -> AbsenceCell[U]:
        """Apply func to the value if occupied, returning a new cell.
        
        If absent, returns an empty cell (of the new type).
        
        Example:
            adjusted = columns_max.map(lambda n: n - 4)
        """
        if is_present(self._value):
            return AbsenceCell[U](func(self._value))  # Narrowed to T by TypeIs
        return AbsenceCell[U](absent)
    
    # Alias for those who prefer the more explicit name
    evaluate_or_absent = map
    
    def flat_map(self, func: Callable[[T], AbsenceCell[U]]) -> AbsenceCell[U]:
        """Apply func returning a cell, flatten the result.
        
        Like map, but func returns an AbsenceCell. Avoids nested cells.
        """
        if is_present(self._value):
            return func(self._value)  # Narrowed to T by TypeIs
        return AbsenceCell[U](absent)
    
    def filter(self, predicate: Callable[[T], bool]) -> AbsenceCell[T]:
        """Keep the value only if predicate returns True."""
        if is_present(self._value):
            if predicate(self._value):  # Narrowed to T by TypeIs
                return self
        return AbsenceCell[T](absent)
    
    # -------------------------------------------------------------------------
    # Fallback Methods
    # -------------------------------------------------------------------------
    
    def or_else(self, alternative: AbsenceCell[T]) -> AbsenceCell[T]:
        """Return self if occupied, else return alternative.
        
        Useful for fallback chains:
            effective = user_pref.or_else(system_default).or_else(hardcoded)
        """
        if is_present(self._value):
            return self
        return alternative
    
    def or_compute(self, factory: Callable[[], AbsenceCell[T]]) -> AbsenceCell[T]:
        """Return self if occupied, else compute alternative lazily."""
        if is_present(self._value):
            return self
        return factory()
    
    # -------------------------------------------------------------------------
    # Conversion Methods
    # -------------------------------------------------------------------------
    
    def to_optional(self) -> T | None:
        """Convert to Optional[T], where absent becomes None."""
        if is_present(self._value):
            return self._value  # Narrowed to T by TypeIs
        return None
    
    # -------------------------------------------------------------------------
    # Dunder Methods
    # -------------------------------------------------------------------------
    
    def __repr__(self) -> str:
        if is_present(self._value):
            return f'AbsenceCell({self._value!r})'
        return 'AbsenceCell()'
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, AbsenceCell):
            if is_absent(self._value) and is_absent(other._value):
                return True
            if is_present(self._value) and is_present(other._value):
                return self._value == other._value
            return False
        return NotImplemented
    
    def __hash__(self) -> int:
        if is_present(self._value):
            return hash(self._value)
        return hash(absent)


# ============================================================================
# Test
# ============================================================================

def test_all_methods() -> None:
    """Test that everything works at runtime."""
    
    # Empty cell
    empty: AbsenceCell[int] = AbsenceCell()
    assert empty.is_absent()
    assert not empty
    assert empty.extract_or(0) == 0
    assert empty.evaluate_or(lambda x: x + 1, -1) == -1
    assert empty.map(lambda x: x * 2).is_absent()
    
    # Occupied cell
    full: AbsenceCell[int] = AbsenceCell(42)
    assert full.is_occupied()
    assert full
    assert full.extract() == 42
    assert full.extract_or(0) == 42
    assert full.evaluate_or(lambda x: x + 1, -1) == 43
    assert full.map(lambda x: x * 2).extract() == 84
    
    # Chaining
    result = (
        AbsenceCell(100)
        .filter(lambda x: x > 0)
        .map(lambda x: x - 4)
        .extract_or(0)
    )
    assert result == 96
    
    # from_optional
    assert AbsenceCell.from_optional(None).is_absent()
    assert AbsenceCell.from_optional("hello").extract() == "hello"
    
    # Fallbacks
    empty_cell: AbsenceCell[int] = AbsenceCell()
    default_cell: AbsenceCell[int] = AbsenceCell(10)
    assert empty_cell.or_else(default_cell).extract() == 10
    
    print("All tests passed!")


if __name__ == '__main__':
    test_all_methods()
