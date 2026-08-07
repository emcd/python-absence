## ADDED Requirements

### Requirement: is_present Predicate

The package MUST provide a positive-form predicate `is_present()` for checking
if a value is not the global absent sentinel, with proper type narrowing support.

#### Scenario: Present value check
- **WHEN** `is_present(value)` is called with a non-absent value
- **THEN** it MUST return `True`

#### Scenario: Absent value check
- **WHEN** `is_present(value)` is called with the global `absent` sentinel
- **THEN** it MUST return `False`

#### Scenario: Type narrowing
- **WHEN** `is_present(value)` returns `True` for a value of type `Absential[T]`
- **THEN** type checkers MUST narrow the type to `T`
