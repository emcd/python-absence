# Absence Sentinel

The package SHALL provide a globally unique `absent` sentinel to enable
reliable identity-based detection of absent values.

## Requirements

### Requirement: Absent Singleton

The package MUST provide a module-level `absent` singleton that is falsey,
immutable, and unique.

#### Scenario: Identity preservation
- **WHEN** `absent` is imported multiple times
- **THEN** all references MUST be the same object (`absent is absent`)

#### Scenario: Falsey behavior
- **WHEN** `absent` is evaluated in a boolean context
- **THEN** it MUST evaluate to `False`

#### Scenario: String representation
- **WHEN** `str(absent)` is called
- **THEN** it MUST return `'absent'`

#### Scenario: Repr representation
- **WHEN** `repr(absent)` is called
- **THEN** it MUST return `'absence.absent'`

### Requirement: Pickle Prevention

Absence sentinels MUST NOT be picklable to guarantee singleton semantics.

#### Scenario: Pickle rejection
- **WHEN** `pickle.dumps(absent)` is attempted
- **THEN** it MUST raise `OperationValidityError`

#### Scenario: Error message clarity
- **WHEN** a pickle error is raised
- **THEN** the message MUST explain why pickling is not supported
