from main import Variable

x = Variable("x")

term = x * (x * x) * 5 / 2 * x
term = term.simplify()
print(term)
print(term.diff(x).simplify())
