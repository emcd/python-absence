# Builtins Integration

## Purpose
The builtins integration capability allows optional installation of the absence sentinel and predicate into the Python builtins module. This enables usage without explicit imports in every file, similar to `None` or `True`.

## Requirements

### Requirement: Install Function
The package MUST provide an `install()` function to inject symbols into builtins.

Priority: Medium

#### Scenario: Default Installation
- **WHEN** `install()` is called without arguments
- **THEN** `Absent` is added to builtins (referencing `absent`)
- **AND** `isabsent` is added to builtins (referencing `is_absent`)

#### Scenario: Custom Names
- **WHEN** `install()` is called with `sentinel_name='MyAbsent'` and `predicate_name='is_missing'`
- **THEN** `MyAbsent` and `is_missing` are added to builtins with correct references

#### Scenario: Partial Installation
- **WHEN** `install()` is called with `sentinel_name=None`
- **THEN** the sentinel is not added to builtins
- **AND** the predicate is added (unless also None)

#### Scenario: Non-Conflict
- **WHEN** `install()` is called multiple times with different names
- **THEN** all installed names remain available
