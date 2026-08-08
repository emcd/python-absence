Add ``adapt_dataclass()`` helper to bridge CLI dataclasses (which use ``None`` for not-provided) to functions with ``Absential[T]`` parameters by omitting fields that match a configurable skip value.
