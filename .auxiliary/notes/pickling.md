# Pickling Support for Absence Sentinels

## Current Implementation

Absence sentinels currently raise `OperationValidityError` when pickling is attempted via `__reduce__`. This was a pragmatic decision to avoid the complexity of implementing singleton-preserving pickle support without adequate time to think through the implications.

## The Challenge

Absence sentinels rely on identity checks (`is` operator) for correctness. The `is_absent()` predicate uses `absent is value` to determine if a value is the global absence sentinel. Singleton semantics are critical for this identity-based checking to work reliably.

Python's `pickle` module serializes objects for storage or transmission and recreates them during unpickling. By default, unpickling creates new object instances, which breaks singleton semantics:

- `pickle.loads(pickle.dumps(absent)) is absent` would be `False`
- Multiple "copies" of sentinels would exist after unpickling
- Identity-based checks would fail unpredictably

## Options to Explore

### 1. Implement Singleton-Preserving Pickle Support

Custom `__reduce__` implementations can preserve singleton semantics during unpickling. This requires careful coordination but is achievable.

**Considerations:**
- What should the pickle representation look like?
- How do we ensure the unpickler returns the same singleton instance?
- Does this work across process boundaries (e.g., multiprocessing)?
- What happens if someone unpickles in a process without the absence package?
- How do we handle custom `AbsenceFactory` instances (each is its own singleton)?

**Possible approach:**
```python
def __reduce__(self):
    # Return a callable that will return the singleton on unpickling
    return (self.__class__, ())
```
But this still creates a new instance unless `__new__` returns the existing singleton.

### 2. Keep Current Non-Picklable Behavior

**Arguments for:**
- Absence sentinels represent transient "missing value" states in function calls
- Serializing absence sentinels may indicate design smell in calling code
- Failing explicitly is better than creating subtle identity bugs
- Forces users to handle absence before serialization boundaries
- Simpler implementation with fewer edge cases

**Arguments against:**
- Users cannot serialize data structures containing absence sentinels
- Requires wrapping or transformation before serialization
- May be inconvenient for some use cases (e.g., caching function results)

### 3. Allow Default Pickling (No Custom __reduce__)

**Arguments for:**
- Simpler - let Python handle it
- Inherits behavior from `falsifier.Falsifier` base class
- Less code to maintain

**Arguments against:**
- Breaks singleton semantics silently after unpickling
- Creates subtle bugs where `is` checks fail unexpectedly
- Violates principle of least surprise for sentinel objects
- Need to verify what `falsifier.Falsifier` actually does

## Questions to Answer

1. What are the actual use cases for pickling absence sentinels?
2. Can we examine how other singleton objects in Python handle pickling?
   - `None` (how does it pickle?)
   - `Ellipsis`
   - `NotImplemented`
   - `dataclasses.MISSING`
   - `typing.NoDefault`
3. What does PEP 661 say about pickling sentinels?
4. How do similar libraries (e.g., `attrs`, `cattrs`) handle sentinel pickling?
5. Is there a real-world scenario where pickling an absence sentinel is the right design?

## Next Steps

- Research how Python's built-in singletons handle pickling
- Investigate PEP 661 recommendations
- Survey similar libraries for precedent
- Gather user feedback on whether pickle support is needed
- If implementing pickle support, write comprehensive tests for edge cases
- Consider whether to implement pickle support for `AbsenceFactory` instances

## References

- Current implementation: `sources/absence/objects.py:59-61` (`__reduce__` raises error)
- Exception: `sources/absence/exceptions.py:38-42` (`OperationValidityError`)
