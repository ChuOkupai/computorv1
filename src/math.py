def gcd(a, b):
	return a if b == 0 else gcd(b, a % b)

def sqrt(x):
	# Babylonian method
	n = 1
	while True:
		n0 = n
		n = 0.5 * (n + x / n)
		if abs(n - n0) < 1e-10:
			break
	return n
