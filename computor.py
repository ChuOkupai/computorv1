from src.parser import parse
from src.solvers import EquationSolverFactory, EquationSolverOptions
import argparse, sys

cmdparser = argparse.ArgumentParser(
	description='Solve polynomial equations up to degree {}.'
		.format(EquationSolverFactory.max_degree),
	epilog="Example: python3 computor.py '- 9.3 * X^2 + 4 * X + 5 = 1'",
	formatter_class=argparse.MetavarTypeHelpFormatter)

cmdparser.add_argument(
	'polynomials',
	help='the polynomial equation to solve',
	metavar='POLYNOMIAL',
	nargs='+',
	type=str)

cmdparser.add_argument(
	'--version',
	action='version',
	version='%(prog)s 1.0')

cmdparser.add_argument(
	'-f', '--use-fractions',
	action='store_true',
	help='use fractions instead of floats if possible')

cmdparser.add_argument(
	'-n', '--no-labels',
	action='store_true',
	help='do not show the labels of the output')

cmdparser.add_argument(
	'-q', '--quiet',
	action='store_true',
	help='show only the solution')

cmdparser.add_argument(
	'-r', '--reduced',
	action='store_true',
	help='show only the reduced form of the polynomial')

cmdparser.add_argument(
	'-s', '--show-steps',
	action='store_true',
	help='show the intermediate steps of the solution')

env = cmdparser.parse_args()
exit_code = 0
for i, p in enumerate(env.polynomials):
	if i > 0:
		print('-' * 8)
	try:
		polynomial = parse(p)
		degree = polynomial.get_degree()
		if not env.quiet:
			print("{}{} = 0".format(('Reduced form: ', '')[env.no_labels], polynomial))
			if env.reduced:
				continue
			print("{}{}".format(('Polynomial degree: ', '')[env.no_labels], degree))
		options = EquationSolverOptions(env.no_labels, env.quiet, env.show_steps, env.use_fractions)
		solver = EquationSolverFactory.create(degree, options)
		solver.solve(polynomial)
	except Exception as e:
		print("{}: {}: {}".format(cmdparser.prog, p, e), file=sys.stderr)
		exit_code = 1
exit(exit_code)
