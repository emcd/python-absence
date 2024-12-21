Add ``absent`` sentinel, a falsey singleton that represents absence in contexts
where ``None`` might be a valid value. The sentinel maintains global uniqueness,
supports proper equality comparison, and can be installed as a builtin.