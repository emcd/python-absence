# Type Safety

## Purpose
The type safety capability provides tools for static type checkers and runtime verification to ensure correct usage of absence sentinels. This includes type predicates for narrowing types and a type alias for expressing optional parameters.

## Requirements

### Requirement: Type Predicates
The package MUST provide type-safe predicate functions for checking absence.

Priority: Critical

#### Scenario: Global Sentinel Check
- **WHEN** `is_absent(value)` is called with the global `absent` sentinel
- **THEN** it returns `True`
- **AND** it returns `False` for any other value (including `None` or custom sentinels)

#### Scenario: General Absence Check
- **WHEN** `is_absence(value)` is called with any absence sentinel (global or custom)
- **THEN** it returns `True`
- **AND** it returns `False` for other objects (including `None`)

#### Scenario: Type Guarding
- **WHEN** `is_absent(value)` is used in a conditional
- **THEN** type checkers narrow the type of `value` to `AbsentSingleton` in the true branch

### Requirement: Absential Type Alias
The package MUST provide an `Absential[T]` type alias to represent a value that can be of type `T` or `absent`.

Priority: Critical

#### Scenario: Type Definition
- **WHEN** `Absential[int]` is used as a type annotation
- **THEN** it accepts integers and the `absent` sentinel
- **AND** it rejects other types (e.g., strings)

#### Scenario: Generic Support
- **WHEN** `Absential[T]` is used with a complex type `T` (e.g., `dict[str, Any]`)
- **THEN** it correctly represents the union of `T` and the sentinel type
