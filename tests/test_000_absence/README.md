# Test Organization

## Module Numbering

Test modules follow a numbered convention reflecting subsystem priority:

- `test_000_package.py` — Package-level structure (imports, module discovery)
- `test_010_base.py` — Common infrastructure (shared imports)
- `test_100_objects.py` — Sentinel factory, global singleton, predicates
- `test_200_installers.py` — Builtins integration
- `test_300_cell.py` — AbsenceCell container
- `test_400_adapters.py` — Dataclass adaptation helpers

Modules 000 and 010 originate from the project Copier template and should
not be project-modified to avoid future merge conflicts.

## Function Numbering

Within each test module, functions are numbered by component:

- **000–099**: Basic module-level functionality
- **100-blocks**: Each class or functional group gets its own 100-number
  range (e.g., 100–199 for singleton, 200–299 for factory)
- **Increments of 1**: Closely related variations within a block

Example from `test_100_objects.py`:

```
100–104  AbsentSingleton (identity, boolean, strings, pickle, overrides)
200–206  AbsenceFactory  (instantiation, boolean, strings, pickle)
300–301  Predicates      (sentinel recognition, type recognition)
900      Meta            (docstring sanity)
```
