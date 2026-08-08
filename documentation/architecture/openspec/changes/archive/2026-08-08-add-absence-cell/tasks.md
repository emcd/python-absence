## 1. Core Implementation
- [x] 1.1 Create `sources/absence/cell.py` with `AbsenceCell` class
- [x] 1.2 Implement constructors: `__init__`, `from_optional`
- [x] 1.3 Implement predicates: `is_absent`, `is_present`, `__bool__`
- [x] 1.4 Implement extraction: `extract`, `extract_or`, `extract_or_compute`
- [x] 1.5 Implement evaluation: `evaluate_or`, `evaluate_or_true`, `evaluate_or_false`
- [x] 1.6 Implement transformation: `transform`
- [x] 1.7 Implement chaining: `or_else`, `to_optional`
- [x] 1.8 Export `AbsenceCell` from `sources/absence/__init__.py`

## 2. Type Safety
- [x] 2.1 Verify `TypeIs[T]` narrowing works with `is_absent()` in cell methods
- [x] 2.2 Minimize `type: ignore` comments (target: only `from_optional`)

## 3. Testing
- [x] 3.1 Test all factory methods (`from_optional`)
- [x] 3.2 Test predicates with empty/occupied cells
- [x] 3.3 Test extraction methods (including exceptions)
- [x] 3.4 Test all `evaluate_or_*` variants
- [x] 3.5 Test `transform`
- [x] 3.6 Test `or_else` chaining
- [x] 3.7 Test `from_optional` with various None scenarios
- [x] 3.8 Test equality and hashing

## 4. Documentation
- [x] 4.1 Add `AbsenceCell` to API reference
- [x] 4.2 Add usage examples (conditional transforms)
- [x] 4.3 Update README with `AbsenceCell` overview
