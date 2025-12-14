# Custom Sentinels

## Purpose
The custom sentinels capability allows developers to create distinct absence sentinels for specific packages or contexts. This prevents conflicts when multiple libraries use sentinels and allows for custom string representations.

## Requirements

### Requirement: Absence Factory
The package MUST provide an `AbsenceFactory` class to create custom absence sentinels.

Priority: High

#### Scenario: Sentinel Creation
- **WHEN** `AbsenceFactory()` is instantiated
- **THEN** it returns a new sentinel object
- **AND** the new sentinel is distinct from the global `absent` sentinel

#### Scenario: Falsey Behavior
- **WHEN** a custom sentinel is evaluated in a boolean context
- **THEN** it evaluates to `False`

#### Scenario: Custom String Representation
- **WHEN** `AbsenceFactory` is instantiated with `repr_function` and `str_function`
- **THEN** `repr(sentinel)` calls the provided `repr_function`
- **AND** `str(sentinel)` calls the provided `str_function`

#### Scenario: Predicate Behavior
- **WHEN** `is_absence(custom_sentinel)` is called
- **THEN** it returns `True`
- **AND** `is_absent(custom_sentinel)` returns `False`
