# TODO: There's gotta be a python lib out there for this
class Fraction:

    def __init__(self, numerator, denominator=1):
        self._numerator = numerator
        self._denominator = denominator

    @property
    def numerator(self):
        return self._numerator

    @property
    def denominator(self):
        return self._denominator

    @property
    def quotient(self):
        """ Performs floor division """
        return self._numerator // self._denominator

    @property
    def remainder(self):
        """ Remainder after floor division """
        return Fraction(self._numerator % self._denominator, self._denominator)

    def invert(self):
        return Fraction(self._denominator, self._numerator)

    # TODO
    def to_significant(self):
        pass

    # TODO
    def to_fixed(self):
        pass

    def __add__(self, other):
        other_parsed = other if isinstance(other, Fraction) else Fraction(other)

        if self._denominator == other_parsed.denominator:
            return Fraction(self._numerator - other_parsed.numerator, self._denominator)

        return Fraction((self._numerator * other_parsed.denominator) + (other_parsed.numerator * self._denominator), self._denominator * other_parsed.denominator)

    def __sub__(self, other):
        other_parsed = other if isinstance(other, Fraction) else Fraction(other)

        if self._denominator == other_parsed.denominator:
            return Fraction(self._numerator - other_parsed.numerator, self._denominator)

        return Fraction((self._numerator * other_parsed.denominator) - (other_parsed.numerator * self._denominator), self._denominator * other_parsed.denominator)

    def __mul__(self, other):
        other_parsed = other if isinstance(other, Fraction) else Fraction(other)
        return Fraction(self._numerator * other_parsed.numerator, self._denominator * other_parsed.denominator)

    def __div__(self, other):
        other_parsed = other if isinstance(other, Fraction) else Fraction(other)
        return Fraction(self._numerator * other_parsed.denominator, self._denominator * other_parsed.numerator)

    def __lt__(self, other):
        other_parsed = other if isinstance(other, Fraction) else Fraction(other)
        return (self._numerator * other_parsed.denominator) < (other_parsed.numerator * self._denominator)

    def __gt__(self, other):
        other_parsed = other if isinstance(other, Fraction) else Fraction(other)
        return (self._numerator * other_parsed.denominator) > (other_parsed.numerator * self._denominator)

    def __eq__(self, other):
        other_parsed = other if isinstance(other, Fraction) else Fraction(other)
        return (self._numerator * other_parsed.denominator) == (other_parsed.numerator * self._denominator)

