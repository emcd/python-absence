## 1. Core Implementation
- [ ] 1.1 Create `sources/absence/cell.py` with `AbsenceCell` class
- [ ] 1.2 Implement constructors: `__init__`, `of`, `empty`, `from_optional`
- [ ] 1.3 Implement predicates: `is_absent`, `is_present`, `__bool__`
- [ ] 1.4 Implement extraction: `extract`, `extract_or`, `extract_or_compute`
- [ ] 1.5 Implement evaluation: `evaluate_or`, `evaluate_or_true`, `evaluate_or_false`
- [ ] 1.6 Implement transformation: `transform`
- [ ] 1.7 Implement chaining: `or_else`, `to_optional`
- [ ] 1.8 Export `AbsenceCell` from `sources/absence/__init__.py`

## 2. Type Safety
- [ ] 2.1 Verify `TypeIs[T]` narrowing works with `is_present()` in cell methods
- [ ] 2.2 Minimize `type: ignore` comments (target: only `from_optional` with `none_is_absent=False`)

## 3. Testing
- [ ] 3.1 Test all factory methods (`of`, `empty`, `from_optional`)
- [ ] 3.2 Test predicates with empty/occupied cells
- [ ] 3.3 Test extraction methods (including exceptions)
- [ ] 3.4 Test all `evaluate_or_*` variants
- [ ] 3.5 Test `transform`
- [ ] 3.6 Test `or_else` chaining
- [ ] 3.7 Test `from_optional` with various None scenarios
- [ ] 3.8 Test equality and hashing

## 4. Documentation
- [ ] 4.1 Add `AbsenceCell` to API reference
- [ ] 4.2 Add usage examples (CLI bridge, conditional transforms)
- [ ] 4.3 Update README with `AbsenceCell` overview
