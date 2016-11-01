"""
FoSAPy - DFA module
Author: Niklas Rieken
"""

class DFA():
	""" A = (Q, Sigma, delta, q_0, F) """
	Q = set()
	Sigma = set()
	delta = {}
	q_0 = None
	F = set()


	def __init__(self, Q, Sigma, delta, q_0, F):
		""" Constructor """
		self.Q = Q
		self.Sigma = Sigma
		self.delta = delta
		self.q_0 = q_0
		self.F = F


	def __repr__(self):
		""" To string method """
		return "A = (\n\tQ = {0},\n\tSigma = {1},\n\tdelta = {2},\n\tq_0 = {3},\n\tF = {4}\n)".format(self.Q, self.Sigma, self.delta, self.q_0, self.F)


	def accept(self, w, doc=False):
		""" solves the word problem for DFA """
		if doc:
			print("Run {0} on the DFA".format(w))
			print("===={0}===========".format("=" * len(w)))

		# init
		q = self.q_0
		if doc:
			print("\n{0}".format(q), end="")

		for a in w:
			q = self.delta[q, a]
			if doc:
				print(" -{0}-> {1}".format(a, q), end="")

		if doc:
			(print(" in F")) if q in self.F else (print(" not in F"))

		return q in self.F


	def emptinesstest(self, doc=False):
		""" solves the emptiness problem for DFA """
		if doc:
			print("Apply emptiness test on DFA")
			print("===========================")

		reachable_states = [self.q_0]
		if doc:
			print("\nReachable states = {0}".format(reachable_states))

		for q in reachable_states:
			for a in self.Sigma:
				if not self.delta[q, a] in reachable_states:
					reachable_states.append(self.delta[q, a])
					if doc:
						print("Reachable states = {0}".format(reachable_states))

		if doc:
			print("The intersection between {0} and {1} is {2}".format(set(reachable_states), self.F, set(reachable_states) & self.F))

		return len(set(reachable_states) & self.F) == 0


	def universaltest(self, doc=False):
		""" solves the universality problem for DFA """
		self.F = self.Q - self.F
		if doc:
			print("Switch accepting and non-accepting states... Now:")

		out = self.emptinesstest(doc)
		if doc:
			print("L(A) == Sigma* iff\n\tSigma* \ L(A) == emptyset")

		self.F = self.Q - self.F

		return out


	def product(self, other, doc=False):
		""" generic method to compute the product automaton with a second automaton """
		Q = set()
		delta = {}
		q_0 = (self.q_0, other.q_0)

		for p in self.Q:
			for q in other.Q:
				Q.add((p, q))

				for a in self.Sigma:
					delta[((p, q), a)] = (self.delta[p, a], other.delta[q, a])

		return DFA(Q, self.Sigma, delta, q_0, set())


	def union(self, other, doc=False):
		""" computes the product automaton for the union of L(self) and L(other) """
		A = self.product(other, doc)
		for p in self.Q:
			for q in other.Q:
				if p in self.F or q in other.F:
				A.F.add((p, q))

		return A


	def intersection(self, other, doc=False):
		""" computes the product automaton for the intersection of L(self) and L(other) """
		A = self.product(other, doc)
		for p in self.Q:
			for q in other.Q:
				if p in self.F and q in other.F:
					A.F.add((p, q))

		return A


	def minimize(self, doc=False):
		""" minimizes the DFA by block refinement """
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
				if len(B) == 1:
					# we don't checkout singletons, there is nothing to split
					continue

				# for each block pick an element (quick and dirty)
				p = B.pop()
				B.add(p)

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

		# now we compute the new automaton
		# TODO: better string representation
		delta = {}
		q_0 = None
		F = set()

		for B in Blocks:
			if self.q_0 in B:
				q_0 = B

			if B <= self.F:
				F.add(frozenset(B))

			p = B.pop()
			B.add(p)
			for a in self.Sigma:
				q = self.delta[p, a]
				for C in Blocks:
					if q in C:
						delta[frozenset(B), a] = C

		return DFA(Blocks, self.Sigma, delta, q_0, F)
