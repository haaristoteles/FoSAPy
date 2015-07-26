# RegPy
A python module with algorithms for regular languages and finite automata.

## Deterministic Finite Automata (DFA)
The DFA module is inside /dfa.py. Note that there no parser for any human-readable representation of DFAs implemented. For instance
```python
Q = {0, 1, 2}
Sigma = {'a', 'b'}
delta = {
	(0, 'a'): 1,
	(0, 'b'): 2,
	(1, 'a'): 1,
	(1, 'b'): 0,
	(2, 'a'): 1,
	(2, 'b'): 1
}
q_0 = 0
F = {1}
```
can be passed as arguments in the constructor:
```python
import dfa
A = dfa.DFA(Q, Sigma, delta, q_0, F)
```
Some basic algorithms are already implemented:
```python
A.accept('abbaa')		# return True iff 'abbaa' is accepted by A
A.minimize()			# computes a minimal automaton recognizing the same language
A.minimize(doc=True)	# gives explanations of each step in the algorithm
```

## Roadmap
Still a lot to do...
