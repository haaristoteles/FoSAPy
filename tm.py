"""
FoSAPy - TM module
Author: Niklas Rieken
"""

import time

class TM():
	""" M = (Q, Sigma, Gamma, delta, q_0, q_f, B) """
	Q = []
	Sigma = []
	Gamma = []
	delta = {}
	q_0 = None
	q_f = None
	B = None


	def __init__(self, Q, Sigma, Gamma, delta, q_0, q_f, B='B'):
		""" Constructor """
		self.Q = Q
		self.Sigma = Sigma
		self.Gamma = Gamma
		self.delta = delta
		self.q_0 = q_0
		self.q_f = q_f
		self.B = B
	

	def __repr__(self):
		""" To string method """
		return "M = (\n\tQ = {0},\n\tSigma = {1},\n\tGamma = {2},\n\tdelta = {3},\n\tq_0 = {4},\n\tq_f = {5},\n\tB = {6}\n)".format(self.Q, self.Sigma, self.Gamma, self.delta, self.q_0, self.q_f, self.B)
	

	def simulate(self, w):
		""" Runs w on M """
		q = self.q_0
		u = ''
		v = w
		print("{0} {1} {2}".format(u, q, v))
		time.sleep(2)
		while q != self.q_f:
			if len(v) == 0:
				v = 'B'
			p = self.delta[q, v[0]][0]
			v = self.delta[q, v[0]][1] + v[1:]
			if self.delta[q, v[0]][2] == 'L':
				if len(u) == 0:
					u = 'B'
				v = u[-1] + v
				u = u[:-1]
			elif self.delta[q, v[0]][2] == 'R':
				if len(v) == 0:
					v = 'B'
				u = u + v[0]
				v = v[1:]
			else:
				pass
			q = p
			print("{0} {1} {2}".format(u, q, v))
			time.sleep(2)
