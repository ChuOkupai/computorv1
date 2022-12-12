from .lexer import tokens
from .polynomials import Polynomial
import ply.yacc as yacc

class ParserError(Exception):
	pass

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES'),
	('right', 'POW'),
	('right', 'EQUALS')
)

class Term:
	def __init__(self, coeff, power):
		self.coeff = coeff
		self.power = power

def p_expression(p):
	'''expression : polynomial
		| polynomial EQUALS polynomial'''
	p[0] = p[1]
	if len(p) == 4:
		p[0] -= p[3]

def p_polynomial(p):
	'''polynomial : term
		| signed_term
		| polynomial signed_term'''
	if len(p) == 2:
		p[0] = Polynomial()
		term = p[1]
	else:
		p[0] = p[1]
		term = p[2]
	p[0].add_coefficient(term.coeff, term.power)

def p_signed_term(p):
	'''signed_term : MINUS term
		| PLUS term'''
	p[0] = p[2]
	if p[1] == '-':
		p[0].coeff = -p[0].coeff

def p_term(p):
	'''term : factor
		| term TIMES factor'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = Term(p[1].coeff * p[3].coeff, p[1].power + p[3].power)

def p_factor(p):
	'''factor : const_factor
		| indeterminate_factor'''
	p[0] = p[1]

def p_const_factor(p):
	'''const_factor : float
		| int'''
	p[0] = Term(p[1], 0)

def p_indeterminate_factor(p):
	'''indeterminate_factor : X
		| X POW int'''
	if len(p) == 2:
		p[0] = Term(1, 1)
	else:
		p[0] = Term(1, p[3])

def p_float(p):
	'''float : FLOAT'''
	p[0] = p[1]

def p_int(p):
	'''int : INT'''
	p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
	if not p:
		raise ParserError("Syntax error at end of input")
	raise ParserError("Syntax error near unexpected token '%s' at position %d" % (p.value, p.lexpos))

# Instantiate the parser
_parser = yacc.yacc()

def parse(s: str) -> Polynomial:
	'''Parse a string into a polynomial.'''
	return _parser.parse(s)
