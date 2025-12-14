# Global Absence Sentinel

## Purpose
The global `absent` sentinel provides a standardized, process-unique object to represent missing values. This addresses the ambiguity of using `None` in scenarios where `None` is a valid value, enabling developers to distinguish between "not provided" and "provided as None".

## Requirements

### Requirement: Singleton Instance
The package MUST provide a globally unique `absent` sentinel available as a module-level singleton.

Priority: Critical

#### Scenario: Identity Check
- **WHEN** the `absent` object is compared with itself using the `is` operator
- **THEN** the result is `True`
- **AND** comparing `absent` with any newly created object returns `False`

#### Scenario: Boolean Evaluation
- **WHEN** the `absent` object is evaluated in a boolean context
- **THEN** it evaluates to `False`

#### Scenario: String Representation
- **WHEN** the `absent` object is converted to a string using `str()`
- **THEN** it returns `'absent'`
- **AND** `repr(absent)` returns `'absence.absent'`

### Requirement: Non-Picklable
The `absent` sentinel MUST NOT be picklable to guarantee singleton semantics and prevent bugs from unpickling multiple instances.

Priority: Critical

#### Scenario: Pickling Attempt
- **WHEN** `pickle.dumps()` is called with the `absent` object
- **THEN** it raises an `OperationValidityError`
- **AND** the error message indicates that pickling is not supported
