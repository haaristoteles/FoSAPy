from unittest import TestCase
from dfa import DFA


class TestDFA(TestCase):

    def setUp(self):
        Q = {0, 1}
        Sigma = {'a', 'b'}
        delta = dict()
        delta[0, 'a'] = 1
        delta[0, 'b'] = 0
        delta[1, 'a'] = 1
        delta[1, 'b'] = 0
        q_0 = 0
        F = {1}
        self.trivial_dfa = DFA(Q, Sigma, delta, q_0, F)

    def test_accept(self):
        self.assertTrue(self.trivial_dfa.accept('a'))
        self.assertFalse(self.trivial_dfa.accept('b'))
