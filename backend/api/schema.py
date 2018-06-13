from schema import Or, And, Use

BooleanString = Or(
    bool,
    And(str, Use(lambda x: x.lower().strip() in ("true", "1")))
)
PositiveInteger = Use(int, lambda x: x >= 0)
StrippedString = And(str, Use(str.strip))
