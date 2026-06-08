# Builtins Integration

The package SHALL provide an `install()` function to optionally add the
absence sentinel and predicate to Python's builtins.

## Requirements

### Requirement: Builtins Installation

The package MUST provide an `install()` function to optionally add `absent`
to builtins for use without imports in frequently-used contexts.

#### Scenario: Default installation
- **WHEN** `install()` is called with no arguments
- **THEN** it MUST add `Absent` and `isabsent` to builtins

#### Scenario: Custom sentinel name
- **WHEN** `install(sentinel_name='CustomName')` is called
- **THEN** it MUST add the sentinel as `builtins.CustomName`

#### Scenario: Custom predicate name
- **WHEN** `install(predicate_name='custom_check')` is called
- **THEN** it MUST add the predicate as `builtins.custom_check`

#### Scenario: Skip sentinel installation
- **WHEN** `install(sentinel_name=None)` is called
- **THEN** it MUST NOT add the sentinel to builtins

#### Scenario: Skip predicate installation
- **WHEN** `install(predicate_name=None)` is called
- **THEN** it MUST NOT add the predicate to builtins

#### Scenario: Multiple calls with different names
- **WHEN** `install()` is called multiple times with different names
- **THEN** each call MUST add its symbols without conflicting with previous calls
