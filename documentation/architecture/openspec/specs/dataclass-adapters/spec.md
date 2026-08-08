# Dataclass Adapters

## Purpose

Provide a helper for bridging dataclass instances (which use ``None`` or
custom sentinels for "not provided") to functions with ``Absential[T]``
parameters (which default to ``absent``).
## Requirements
### Requirement: Dataclass Adaptation

The package MUST provide an `adapt_dataclass()` function that extracts
fields from a dataclass instance into a dictionary, omitting fields whose
value matches a configurable skip value.

#### Scenario: Basic extraction
- **WHEN** `adapt_dataclass(instance)` is called on a dataclass instance
- **THEN** it MUST return a dictionary mapping field names to values

#### Scenario: Default skip value
- **WHEN** `adapt_dataclass(instance)` is called without a skip_value
- **THEN** it MUST omit fields whose value is `None`

#### Scenario: Custom skip value
- **WHEN** `adapt_dataclass(instance, skip_value=sentinel)` is called
- **THEN** it MUST omit fields whose value matches `sentinel` by identity

#### Scenario: Non-dataclass argument
- **WHEN** `adapt_dataclass(obj)` is called with an object that is not a
  dataclass instance
- **THEN** it MUST raise `OperationValidityError`

#### Scenario: Dataclass class instead of instance
- **WHEN** `adapt_dataclass(SomeClass)` is called with a dataclass type
  rather than an instance
- **THEN** it MUST raise `OperationValidityError`

#### Scenario: Class variables excluded
- **WHEN** `adapt_dataclass(instance)` is called on a dataclass with
  `ClassVar`-annotated fields
- **THEN** the `ClassVar` fields MUST NOT appear in the result

#### Scenario: Inherited fields included
- **WHEN** `adapt_dataclass(instance)` is called on a dataclass that
  inherits from another dataclass
- **THEN** inherited fields MUST appear in the result

