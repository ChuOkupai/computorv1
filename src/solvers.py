from . import math
from .numbers import Complex, Fraction

class EquationSolverOptions():
	"""Options for the EquationSolver class"""

	def __init__(self, no_labels=False, quiet=False, show_steps=False, use_fractions=True):
		"""Create a new EquationSolverOptions object with the given options"""
		self.no_labels = no_labels
		self.quiet = quiet
		self.show_steps = show_steps
		self.use_fractions = use_fractions

class EquationSolver():
	"""Class for solving equations"""

	def __init__(self, options: EquationSolverOptions):
		"""Initialize the equation solver"""
		self.options = options

	def _as_frac(self, num, den):
		"""Try to convert a number to a fraction"""
		if self.options.use_fractions:
			if isinstance(num, float) and num.is_integer():
				num = int(num)
			if isinstance(den, float) and den.is_integer():
				den = int(den)
			if isinstance(num, int) and isinstance(den, int):
				f = Fraction(num, den)
				return f if f.denominator != 1 else f.numerator
		return num / den

	def _can_show_labels(self):
		"""Check if the labels can be shown"""
		return not self.options.quiet and not self.options.no_labels

	def _can_show_steps(self):
		"""Check if the steps can be shown"""
		return not self.options.quiet and self.options.show_steps

	def _get_coefficients(self, p):
		"""Get the coefficients of the polynomial"""
		return [p.coefficients[i] for i in reversed(range(len(p.coefficients)))]

	def _labelized_output(self, label, content):
		"""Print the labelized output"""
		if self._can_show_labels():
			print(label, end=': ')
		print(content)

	def _try_show_steps(self, variables, equation_form, solutions, discriminant=None):
		"""Show the steps of the solution"""
		if len(variables) > 26:
			raise ValueError("Too many variables")
		if not self._can_show_steps():
			return
		self._labelized_output('Variables', ', '.join("{} = {}".format(
			chr(ord('a') + i), v) for i, v in enumerate(variables)))
		self._labelized_output('Equation form', equation_form)
		if discriminant is not None:
			self._labelized_output('Discriminant', discriminant)
		if len(solutions) > 1:
			if self._can_show_labels():
				print("Solutions form:")
			for i, s in enumerate(solutions):
				print("X{} = {}".format(i + 1, s))
		else:
			self._labelized_output("Solution form", "X = " + solutions[0])

class ConstantEquationSolver(EquationSolver):
	"""Class for solving constant equations"""

	def __init__(self, options: EquationSolverOptions):
		super().__init__(options)

	def solve(self, polynomial):
		"""Solve the equation"""
		a, = self._get_coefficients(polynomial)
		if self._can_show_steps():
			self._try_show_steps([a], "a", ["All real numbers if a = 0"])
		s = ["There is no solution.", "All real numbers are solution."]
		print(s[a == 0])

class LinearEquationSolver(EquationSolver):
	"""Class for solving linear equations"""

	def __init__(self, options: EquationSolverOptions):
		super().__init__(options)

	def solve(self, polynomial):
		"""Solve the linear equation"""
		a, b = self._get_coefficients(polynomial)
		self._try_show_steps([a, b], "a * X + b", ["-b / a"])
		self._labelized_output("The solution is", self._as_frac(-b, a))

class QuadraticEquationSolver(EquationSolver):
	"""Class for solving quadratic equations"""

	def __init__(self, options: EquationSolverOptions):
		super().__init__(options)

	def solve(self, polynomial):
		"""Solve the quadratic equation"""
		a, b, c = self._get_coefficients(polynomial)
		d = b * b - 4 * a * c
		if d == 0:
			solutions = ["-b / (2 * a)"]
		elif d > 0:
			solutions = ["(-b + sqrt(delta)) / (2 * a)", "(-b - sqrt(delta)) / (2 * a)"]
		else:
			solutions = [
				"(-b / (2 * a)) + sqrt(-delta) / (2 * a) * i",
				"(-b / (2 * a)) - sqrt(-delta) / (2 * a) * i"
			]
		self._try_show_steps([a, b, c], "a * X^2 + b * X + c", solutions, d)
		if self._can_show_labels():
			print("Discriminant is ", end='')
		if d == 0:
			if self._can_show_labels():
				print("zero, the solution is:")
			print(self._as_frac(-b, 2 * a))
		else:
			sdelta = math.sqrt(abs(d))
			if d > 0:
				sign = 'positive'
				solutions = [ self._as_frac(-b + sdelta, 2 * a), self._as_frac(-b - sdelta, 2 * a)]
			else:
				sign = 'negative'
				num, den = self._as_frac(-b, 2 * a), self._as_frac(sdelta, 2 * a)
				solutions = [ Complex(num, den), Complex(num, -den) ]
			if self._can_show_labels():
				print("stricly {}, the two solutions are:".format(sign))
			[print(s) for s in solutions]

class EquationSolverFactory():
	"""Factory for creating equation solvers"""

	solvers = [
		ConstantEquationSolver,
		LinearEquationSolver,
		QuadraticEquationSolver
	]
	max_degree = len(solvers) - 1

	@staticmethod
	def create(degree: int, options: EquationSolverOptions):
		"""Create a solver for the given degree"""
		max_deg = EquationSolverFactory.max_degree
		if degree > max_deg:
			raise NotImplementedError(
				"The polynomial degree is stricly greater than {}, I can't solve."
				.format(max_deg))
		return EquationSolverFactory.solvers[degree](options)
