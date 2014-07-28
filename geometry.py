import random

def roll(r, d=6):
	return [random.randint(1,d) for x in xrange(r)]

levels = [
	[],
	[3, 5, 7],
	[11, 13, 17],
	[19, 23, 29],
	[31, 37, 41],
	[43, 47, 53],
	[59, 61, 67],
	[71, 73, 79],
	[83, 89, 97],
	[101, 103, 107],
	[109, 113, 127], # extrapolated 10th+ spell level
	[131, 137, 139],
	[149, 151, 157],
	[163, 167, 173],
	[179, 181, 191],
]

def cast(level, ranks, calculating=False):
	d = 8 if calculating else 6
	pool = roll(ranks, d)
	tree = MathTree(pool[0], pool[1:])
	for x, m in tree:
		if x in levels[level]:
			return x, m
	return None, None

TRIALS = 10000

def odds(level, ranks, calculating=False):
	t = 0
	for _ in xrange(TRIALS):
		x, m = cast(level, ranks, calculating)
		if x:
			t += 1
	return t

class MathLeaf(object):
	def __init__(self, x, m):
		self.value = x
		self.m = m
	def __iter__(self):
		yield self

class MathTree(object):
	def __init__(self, x, l, m=None):
		self.value = x
		self.l = l
		if not m:
			m = str(x)
		self.m = m

	def build_tree(self):
		x = self.value
		l = self.l
		m = self.m
		if len(l) > 1:
			self.add = MathTree(x+l[0], l[1:], m+' + {0}'.format(l[0]))
			self.sub = MathTree(x-l[0], l[1:], m+' - {0}'.format(l[0]))
			self.mul = MathTree(x*l[0], l[1:], m+' * {0}'.format(l[0]))
			self.div = MathTree(x/l[0], l[1:], m+' / {0}'.format(l[0]))
		else:
			self.add = MathLeaf(x+l[0], m+' + {0}'.format(l[0]))
			self.sub = MathLeaf(x-l[0], m+' - {0}'.format(l[0]))
			self.mul = MathLeaf(x*l[0], m+' * {0}'.format(l[0]))
			self.div = MathLeaf(x/l[0], m+' / {0}'.format(l[0]))
	def __iter__(self):
		self.build_tree()
		for node in [self.add, self.sub, self.mul, self.div]:
			for leaf in iter(node):
				if isinstance(leaf, MathLeaf):
					yield leaf.value, leaf.m
				else:
					yield leaf

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='A simple program for rolling and solving PF\'s Sacred Geometry feat')
	parser.add_argument('level', metavar='N', type=int, nargs='?')
	parser.add_argument('ranks', metavar='R', type=int, nargs='?')
	parser.add_argument('--calculating', '-c', action='store_true')
	args = parser.parse_args()

	x, m = cast(args.level, args.ranks, args.calculating)
	if x:
		print 'success!', m, '=', x
	else:
		print 'failure'




