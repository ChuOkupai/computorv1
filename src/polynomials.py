class Polynomial:
	def __init__(self, coefficients = []):
		'''Initialize a polynomial with the given coefficients.
		coefficients[0] is the constant term, coefficients[1] is the coefficient of X, etc.'''
		self.coefficients = coefficients if coefficients else [0]
		self.__reduce()

	def __reduce(self):
		'''Remove trailing zeros from the coefficients.'''
		i = self.get_degree()
		while i > 0 and self.coefficients[i] == 0:
			i -= 1
		self.coefficients = self.coefficients[:i + 1]

	def __str__(self):
		'''Return a string representation of the polynomial.'''
		s = ''
		for i in reversed(range(len(self.coefficients))):
			coeff = self.coefficients[i]
			if coeff == 0:
				continue
			else:
				if len(s) > 0:
					s += ' ' + ('+', '-')[coeff < 0] + ' '
				elif coeff < 0:
					s += '- '
				if i == 0 or coeff != 1:
					s += str(abs(coeff))
				if i > 0:
					if coeff != 1:
						s += ' * '
					s += 'X'
					if i > 1:
						s += '^' + str(i)
		if len(s) == 0:
			s = '0'
		return s

	def __repr__(self):
		return "Polynomial(" + str(self.coefficients) + ")"

	def __add__(self, other):
		if isinstance(other, int):
			other = Polynomial([other])
		min_len = min(len(self.coefficients), len(other.coefficients))
		if len(self.coefficients) > len(other.coefficients):
			coeffs_to_add = self.coefficients[min_len:]
		else:
			coeffs_to_add = other.coefficients[min_len:]
		return Polynomial([self.coefficients[i] + other.coefficients[i] for i in range(min_len)] + coeffs_to_add)

	def __sub__(self, other):
		return self + (-other)

	def __neg__(self):
		return Polynomial([-coeff for coeff in self.coefficients])

	def add_coefficient(self, coeff, degree):
		'''Add the given coefficient to the coefficient of the given degree.'''
		if degree < len(self.coefficients):
			coeff += self.coefficients[degree]
		self.set_coefficient(coeff, degree)

	def get_degree(self):
		'''Return the degree of the polynomial.'''
		return len(self.coefficients) - 1

	def set_coefficient(self, coeff, degree):
		'''Set the coefficient of the given degree. If the degree is higher than the current degree, the polynomial is extended with zeros.'''
		if degree >= len(self.coefficients):
			self.coefficients += [0] * (degree - self.get_degree())
		self.coefficients[degree] = coeff
		self.__reduce()

	def set_degree(self, degree):
		'''Set the degree of the polynomial. The polynomial will be truncated if necessary.'''
		self.coefficients = self.coefficients[:degree + 1]
		self.__reduce()
