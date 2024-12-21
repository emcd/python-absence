Add ``is_absent`` and ``is_absence`` predicates for type-safe checking of
absence sentinels. These can distinguish between the global sentinel and
factory-produced sentinels, and support installation as builtins.