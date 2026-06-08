# Type Safety

The package SHALL provide type-safe predicates and type aliases for absence
detection with static type checker support.

## Requirements

### Requirement: Type Predicate Functions

The package MUST provide type-safe predicates for checking absence that enable
type checkers to narrow types correctly.

#### Scenario: Global sentinel check
- **WHEN** `is_absent(value)` is called with the global `absent` sentinel
- **THEN** it MUST return `True`

#### Scenario: Non-sentinel check
- **WHEN** `is_absent(value)` is called with any value other than `absent`
- **THEN** it MUST return `False`

#### Scenario: Any absence check
- **WHEN** `is_absence(value)` is called with any `AbsenceFactory` instance
- **THEN** it MUST return `True`

#### Scenario: Type narrowing support
- **WHEN** predicates are used in conditional checks
- **THEN** type checkers MUST narrow the type correctly via `TypeIs`

### Requirement: Absential Type Alias

The package MUST provide an `Absential[T]` type alias for expressing
optional-but-not-None parameters in type signatures.

#### Scenario: Type equivalence
- **WHEN** `Absential[int]` is used in a type annotation
- **THEN** it MUST be equivalent to `int | AbsentSingleton`

#### Scenario: Generic type support
- **WHEN** `Absential[dict[str, Any]]` is used
- **THEN** type checkers MUST recognize it as accepting `dict[str, Any]` or `absent`

#### Scenario: Type narrowing after check
- **WHEN** a value of type `Absential[T]` is checked with `is_absent()`
- **THEN** type checkers MUST narrow the type to `T` in the else branch
