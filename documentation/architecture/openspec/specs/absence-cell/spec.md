# AbsenceCell Specification

## Requirements

### Requirement: AbsenceCell Container

The package MUST provide an `AbsenceCell` class as an immutable container
wrapping `Absential[T]` with a rich API for conditional operations.

#### Scenario: Empty cell creation
- **WHEN** `AbsenceCell()` is called with no arguments
- **THEN** it MUST create a cell containing the `absent` sentinel

#### Scenario: Occupied cell creation
- **WHEN** `AbsenceCell(value)` is called with a value
- **THEN** it MUST create a cell containing that value

#### Scenario: Immutability
- **WHEN** a cell is created
- **THEN** its value MUST NOT be modifiable after construction

### Requirement: Cell Predicates

The cell MUST provide predicates for checking its state.

#### Scenario: is_absent on empty cell
- **WHEN** `cell.is_absent()` is called on an empty cell
- **THEN** it MUST return `True`

#### Scenario: is_present on occupied cell
- **WHEN** `cell.is_present()` is called on an occupied cell
- **THEN** it MUST return `True`

#### Scenario: Boolean evaluation
- **WHEN** an occupied cell is evaluated in a boolean context
- **THEN** it MUST evaluate to `True`

#### Scenario: Boolean evaluation of empty cell
- **WHEN** an empty cell is evaluated in a boolean context
- **THEN** it MUST evaluate to `False`

### Requirement: Cell Extraction

The cell MUST provide methods to extract values with fallbacks.

#### Scenario: Extract from occupied cell
- **WHEN** `cell.extract()` is called on an occupied cell
- **THEN** it MUST return the contained value

#### Scenario: Extract from empty cell
- **WHEN** `cell.extract()` is called on an empty cell
- **THEN** it MUST raise `ValueError`

#### Scenario: Extract with default
- **WHEN** `cell.extract_or(default)` is called
- **THEN** it MUST return the contained value if occupied, or `default` if empty

#### Scenario: Extract with computed default
- **WHEN** `cell.extract_or_compute(factory)` is called
- **THEN** it MUST return the contained value if occupied, or call `factory()` if empty

### Requirement: Cell Evaluation

The cell MUST provide methods to apply functions conditionally.

#### Scenario: Evaluate or default
- **WHEN** `cell.evaluate_or(func, default)` is called on an occupied cell
- **THEN** it MUST return `func(value)`

#### Scenario: Evaluate or default on empty cell
- **WHEN** `cell.evaluate_or(func, default)` is called on an empty cell
- **THEN** it MUST return `default`

#### Scenario: Evaluate or true
- **WHEN** `cell.evaluate_or_true(predicate)` is called on an empty cell
- **THEN** it MUST return `True`

#### Scenario: Evaluate or false
- **WHEN** `cell.evaluate_or_false(predicate)` is called on an empty cell
- **THEN** it MUST return `False`

### Requirement: Cell Transformation

The cell MUST provide methods to transform values while preserving absence.

#### Scenario: Transform on occupied cell
- **WHEN** `cell.transform(func)` is called on an occupied cell
- **THEN** it MUST return a new cell containing `func(value)`

#### Scenario: Transform on empty cell
- **WHEN** `cell.transform(func)` is called on an empty cell
- **THEN** it MUST return an empty cell

### Requirement: Cell Chaining

The cell MUST provide methods for fallback chaining.

#### Scenario: Or else with occupied cell
- **WHEN** `cell.or_else(alternative)` is called on an occupied cell
- **THEN** it MUST return the original cell

#### Scenario: Or else with empty cell
- **WHEN** `cell.or_else(alternative)` is called on an empty cell
- **THEN** it MUST return `alternative`

### Requirement: Cell Conversion

The cell MUST provide methods to convert to other representations.

#### Scenario: To optional with occupied cell
- **WHEN** `cell.to_optional()` is called on an occupied cell
- **THEN** it MUST return the contained value

#### Scenario: To optional with empty cell
- **WHEN** `cell.to_optional()` is called on an empty cell
- **THEN** it MUST return `None`

### Requirement: Optional Bridge

The cell MUST provide a factory method for bridging from `Optional[T]` values.

#### Scenario: From optional with None
- **WHEN** `AbsenceCell.from_optional(None)` is called
- **THEN** it MUST return an empty cell

#### Scenario: From optional with value
- **WHEN** `AbsenceCell.from_optional(value)` is called with a non-None value
- **THEN** it MUST return an occupied cell containing that value

#### Scenario: From optional preserving None
- **WHEN** `AbsenceCell.from_optional(None, none_is_absent=False)` is called
- **THEN** it MUST return an occupied cell containing `None`
