# Custom Sentinels

The package SHALL provide an `AbsenceFactory` for creating package-specific
absence sentinels.

## Requirements

### Requirement: AbsenceFactory

The package MUST provide an `AbsenceFactory` to enable creation of
package-specific absence sentinels for specialized contexts.

#### Scenario: Factory creation
- **WHEN** `AbsenceFactory()` is called
- **THEN** it MUST create a new falsey sentinel instance

#### Scenario: Custom representations
- **WHEN** `AbsenceFactory(repr_function=..., str_function=...)` is provided
- **THEN** the sentinel MUST use those functions for `__repr__` and `__str__`

#### Scenario: Falsey behavior
- **WHEN** any `AbsenceFactory` instance is evaluated in a boolean context
- **THEN** it MUST evaluate to `False`

#### Scenario: Pickle rejection
- **WHEN** `pickle.dumps(factory_instance)` is attempted
- **THEN** it MUST raise `OperationValidityError`

#### Scenario: Absence detection
- **WHEN** `is_absence(custom_sentinel)` is called
- **THEN** it MUST return `True`

#### Scenario: Not global sentinel
- **WHEN** `is_absent(custom_sentinel)` is called
- **THEN** it MUST return `False`
