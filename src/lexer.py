import ply.lex as lex

class LexerError(Exception):
	pass

tokens = (
	# Simple tokens
	'EQUALS',
	'MINUS',
	'PLUS',
	'POW',
	'TIMES',
	'X',
	# Complex tokens
	'FLOAT',
	'INT'
)

# Regular expression rules for simple tokens
t_EQUALS	= r'='
t_MINUS		= r'-'
t_PLUS		= r'\+'
t_POW		= r'\^'
t_TIMES		= r'\*'
t_X			= r'X'

# Regular expression rules for complex tokens

def t_FLOAT(t):
	r'(\d+[.,]\d*|[.,]\d+)([eE][-+]?\d+)?'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
	raise LexerError("Illegal character '%s' at position %d" % (t.value[0], t.lexpos))

# Instantiate the lexer
_lexer = lex.lex()
