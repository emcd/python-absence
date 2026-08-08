## 1. Core Implementation
- [x] 1.1 Add `dataclasses` import to `sources/absence/__/imports.py`
- [x] 1.2 Create `sources/absence/adapters.py` with `adapt_dataclass()`
- [x] 1.3 Export `adapt_dataclass` from `sources/absence/__init__.py`

## 2. Testing
- [x] 2.1 Test basic field extraction from occupied dataclass
- [x] 2.2 Test None fields skipped by default
- [x] 2.3 Test custom skip_value
- [x] 2.4 Test error on non-dataclass argument
- [x] 2.5 Test error on dataclass class (not instance)
- [x] 2.6 Test ClassVar fields excluded
- [x] 2.7 Test inherited fields included

## 3. Documentation
- [x] 3.1 Update `sources/absence/README.md` with adapters component
- [x] 3.2 Update `tests/test_000_absence/README.md` with test_400 module
