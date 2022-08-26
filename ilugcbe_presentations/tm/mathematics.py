#!/usr/bin/env python
from __future__ import division
from math import sqrt

def vector_length(vector):
	"""
	|\vecv| = \sqrt \sum _{i=1}^{n}x_{i}^{2}
	Length of a vector is found by squaring each component, adding
	them together, and taking the square root of the sum
	\vecv = [4,11,8,10]
	|vecv| = \sqrt 4^{2} + 11^{2} + 8^{2} + 10^{2} = \sqrt 301 =
	17.35
	"""
	squre = [ v*v for v in vector]
	length = sqrt(sum(squre))

	return length

def vector_addition(*vectors):
	"""
	Adding two vectors means each compinents in \vecv_{1} to the
	component in the corresponding position in \vecv_{2} to get
	a new vector.
	\vecv_{1} = [3,2,1,-2]
	\vec_{2} = [2,-1,4,1]
	\vecv_{1} + \vecv_{2} = [(3+2),(2-1),(1+4),(-2+1)]
	= [5,1,5,-1]
	"""
	return map(sum,zip(*vectors))

def scalar_multiplication(vector,scalar):
	"""
	Multiplying every component by that real number to
	yeald a new vector. 
	\vecv = [3,6,8,4] * 1.5 =
	[(1.5 * 3), (1.5 * 6), (1.5 * 8), (1.5 * 4)] =
	[4.5,9,12,6]
	"""
	newvec = [v * scalar for v in vector]

	return newvec


def inner_product(vector1, vector2):
	"""
	The inner product of two vectors defines multiplication
	of two vectors. Is is done by multiplying each component in 
	\vecv_{1} by the component in \vecv_{2} in the same position
	and adding them all together to get a scalar value.
	(\vecv_{1},\vecv_{2}) or \vecv_{1} . \vecv_{2} 
	(\vecx,\vecy}) = \vecx . \vecy = \sum_{i=1}^{n}x_{i}y_{i}
	if \vecx = [1,6,7,4] and \vecy = [3,2,8,3]
	\vecx . \vecy = 1(3) + 6(2) + 7(8) + 3(4) = 83
	"""
	return sum([x * y for x, y in zip(vector1,vector2)])


def is_othoganal(vector1,vector2):
	"""
	Two vectors are orthoganal to each other if their
	inner product equals zero.
	"""
	if inner_product(vector1,vector2) == 0:
		return True
	else:
		return False


def normal_vector(vector):
	"""
	A normal vector (ubit vector) is avetor of length 1.
	Any vector with an initial length > 0 can be normalized 
	by dividing each component in it by the vector's length.
	if \vecv = [2,4,1,2]
	|\vecv| = \sqrt 2^{2} + 4^{2} + 1^{2} + 2^{2} = \sqrt 25 =5
	Then \vecv = [\frac{2}{5},\frac{4}{5},\frac{1}{5},\frac{1}{5}
	Then |\vecv| = \sqrt [\frac{2}{5},\frac{4}{5},\frac{1}{5},\frac{1}{5}
	= \sqrt \frac{25}{25} = 1
	"""
	length = vector_length(vector)
	divide_b_len = [ x/length for x in vector]
	dbl_sur = [y *y for y in divide_b_len]

	return sum(dbl_sur)

if __name__ == "__main__":
	vec = [4,11,8,10]
	vec1 = [4,11,8,10]
	vec2 = [4,11,8,10]
	len = vector_length(vec)
	print len
	f = vector_addition(vec,vec1,vec2)
	print f
	k = [3,6,8,4]
	s = 1.5
	sm = scalar_multiplication(k,s)
	print sm
	x = [1,6,7,4]
	y = [3,2,8,3]
	j = inner_product(x,y)
	print j
	z = [2,1,-2,4]
	p = [3,-6,4,2]
	ort = is_othoganal(z,p)
	print ort
	ort = is_othoganal(x,y)
	print ort
	fn = [2,4,1,2]
	nv = normal_vector(fn)
	print nv
