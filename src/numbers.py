from . import math
import operator

class Complex:
	def __init__(self, real, imag):
		self.real = real
		self.imag = imag

	def __str__(self):
		sign = ('+', '-')[self.imag < 0]
		return "{} {} {} * i".format(self.real, sign, abs(self.imag))

	def __repr__(self):
		return "{}({}, {})".format(self.__class__.__name__, self.real, self.imag)

class Fraction:
	def __init__(self, numerator, denominator):
		if denominator < 0:
			numerator = -numerator
			denominator = -denominator
		gcd = math.gcd(abs(numerator), abs(denominator))
		self.numerator = numerator // gcd
		self.denominator = denominator // gcd

	def __str__(self):
		return str(self.numerator) + " / " + str(self.denominator)

	def __repr__(self):
		return "{}({}, {})".format(self.__class__.__name__, self.numerator, self.denominator)

	def __add__(self, other):
		if isinstance(other, int):
			other = Fraction(other, 1)
		return Fraction(self.numerator * other.denominator + other.numerator * self.denominator, self.denominator * other.denominator)

	def __sub__(self, other):
		return self + (-other)

	def __mul__(self, other):
		if isinstance(other, int):
			other = Fraction(other, 1)
		return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

	def __div__(self, other):
		if isinstance(other, int):
			other = Fraction(other, 1)
		return self * other.reciprocal()

	def __abs__(self):
		return Fraction(abs(self.numerator), abs(self.denominator))

	def __neg__(self):
		return Fraction(-self.numerator, self.denominator)

	def __float__(self):
		return float(self.numerator) / float(self.denominator)

	def _cmp(self, other, op):
		return op(float(self), float(other))

	def __lt__(a, b):
		return a._cmp(b, operator.lt)

	def __le__(a, b):
		return a._cmp(b, operator.le)

	def __gt__(a, b):
		return a._cmp(b, operator.gt)

	def __ge__(a, b):
		return a._cmp(b, operator.ge)

	def reciprocal(self):
		return Fraction(self.denominator, self.numerator)
