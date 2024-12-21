Add ``AbsenceFactory`` class for creating package-specific absence sentinels.
Each instance evaluates to ``False`` in boolean contexts, has unique identity,
and supports customizable string representations.