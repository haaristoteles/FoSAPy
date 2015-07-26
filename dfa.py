"""
DFA class
"""

class DFA():
	""" A = (Q, Sigma, delta, q_0, F) """
	Q = {}
	Sigma = {}
	delta = {}
	q_0 = None
	F = {}


	def __init__(self, Q, Sigma, delta, q_0, F):
		self.Q = Q
		self.Sigma = Sigma
		self.delta = delta
		self.q_0 = q_0
		self.F = F


	def accept(self, w):
		q = self.q_0

		for a in w:
			q = self.delta[q, a]

		return q in self.F


	def minimize(self, doc=False):
		if doc:
			print("Minimizing procedure starts")
			print("===========================")

		# init
		Blocks = []
		Blocks.append(self.F)
		Blocks.append(self.Q - self.F)
		i = 0

		while True:
			if doc:
				print("\nRound {0}: Blocks {1}".format(i, Blocks))
				i += 1

			# do the following until change == False holds one whole iteration
			change = False

			for B in Blocks:
				# for each block pick an element (quick and dirty)
				p = B.pop()
				B.add(p)

				if len(B) == 1:
					# we don't checkout singletons, there is nothing to split
					continue
				if doc:
					print("\tCheckout block {0}, take pivot state {1}".format(B, p))

				for a in self.Sigma:
					# check for all symbols
					r = self.delta[p, a]
					E = F = set()

					for C in Blocks:
						# find the block of delta(p, a)
						if r in C:
							D = C

					for q in B:
						# split the block by state equivalence
						if self.delta[q, a] in D:
							E = E | {q}
							if doc:
								print("\t\tstate {0} moves with {1} in block {2}".format(q, a, D))
						else:
							F = F | {q}
							if doc:
								print("\t\tstate {0} moves with {1} not in block {2}".format(q, a, D))

					if len(E) != 0 and len(F) != 0:
						# if there is a non-trivial split apply a refinement
						Blocks.remove(B)
						Blocks.append(E)
						Blocks.append(F)
						change = True
						if doc:
							print("\tfound refinement for block {0} under symbol {1}:\n\t\t{2} and {3} will be added.\n".format(B, a, E, F))
						break
					else:
						if doc:
							print("\tno refinement found for block {0} under symbol {1}".format(B, a))
			if not change:
				break

		return Blocks
