from re import L


class Term:
    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        if not isinstance(other, Term):
            return Mul(other, self)

    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        if not isinstance(other, Term):
            return Add(other, self)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        if not isinstance(other, Term):
            return Div(other, self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        if not isinstance(other, Term):
            return Sub(other, self)

    def is_null(self):
        return False

    def simplify(self):
        return self


class NumberWrapper(Term):
    def __init__(self, number):
        self.number = number

    def diff(self, var):
        return NumberWrapper(0)

    def __repr__(self) -> str:
        return str(self.number)

    def is_null(self):
        return self.number == 0

    def __eq__(self, other):
        if self.number == other:
            return True
        else:
            if isinstance(other, NumberWrapper):
                return other.number == self.number
        return False


class Variable(Term):
    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name

    def diff(self, var):
        if var == self:
            return 1
        else:
            return self

    def __repr__(self) -> str:
        return self.name


class Mul(Term):
    def __init__(self, term_left, term_right):
        if isinstance(term_left, Term):
            self.term_left = term_left
        else:
            self.term_left = NumberWrapper(term_left)

        if isinstance(term_right, Term):
            self.term_right = term_right
        else:
            self.term_right = NumberWrapper(term_right)

    def diff(self, var):
        return (
            self.term_left * self.term_right.diff(var)
            + self.term_left.diff(var) * self.term_right
        )

    def __repr__(self):
        return f"{str(self.term_left)} * {str(self.term_right)}"

    def simplify(self):
        l_simp = self.term_left.simplify()
        r_simp = self.term_right.simplify()
        if isinstance(l_simp, NumberWrapper) and isinstance(
            r_simp, NumberWrapper
        ):
            return NumberWrapper(l_simp.number * r_simp.number)
        if l_simp == 1:
            return r_simp
        if r_simp == 1:
            return l_simp
        return l_simp * r_simp


class Add(Term):
    def __init__(self, term_left, term_right):
        if isinstance(term_left, Term):
            self.term_left = term_left
        else:
            self.term_left = NumberWrapper(term_left)

        if isinstance(term_right, Term):
            self.term_right = term_right
        else:
            self.term_right = NumberWrapper(term_right)

    def diff(self, var):
        return self.term_left.diff(var) + self.term_right.diff(var)

    def __repr__(self):
        return f"({str(self.term_left)} + {str(self.term_right)})"

    def simplify(self):
        l_simp = self.term_left.simplify()
        r_simp = self.term_right.simplify()
        l_null = l_simp.is_null()
        r_null = r_simp.is_null()

        if l_null and r_null:
            return NumberWrapper(0)
        if l_null:
            return r_simp
        if r_null:
            return l_simp
        return l_simp + l_simp


class Div(Term):
    def __init__(self, term_left, term_right):
        if isinstance(term_left, Term):
            self.term_left = term_left
        else:
            self.term_left = NumberWrapper(term_left)

        if isinstance(term_right, Term):
            self.term_right = term_right
        else:
            self.term_right = NumberWrapper(term_right)

    def diff(self, var):
        return (
            self.term_left.diff(var) * self.term_right
            - self.term_left * self.term_right.diff(var)
        ) / (self.term_right * self.term_right)

    def __repr__(self):
        return f"{str(self.term_left)} / ({str(self.term_right)})"


class Sub(Term):
    def __init__(self, term_left, term_right):
        if isinstance(term_left, Term):
            self.term_left = term_left
        else:
            self.term_left = NumberWrapper(term_left)

        if isinstance(term_right, Term):
            self.term_right = term_right
        else:
            self.term_right = NumberWrapper(term_right)

    def diff(self, var):
        return self.term_left.diff(var) - self.term_right.diff(var)
