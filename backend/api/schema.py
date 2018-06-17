from schema import Or, And, Use

# Schema per stringa booleana ('true' o '1')
BooleanString = Or(
    bool,
    And(str, Use(lambda x: x.lower().strip() in ("true", "1")))
)

# Schema per intero positivo
PositiveInteger = Use(int, lambda x: x >= 0)

# Schema per stringa non vuota (rimuove anche gli spazi)
StrippedString = And(str, Use(str.strip))
