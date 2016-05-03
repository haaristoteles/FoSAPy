file = sys.argv[1]
f = open(file, "r")

head = f.readline()
if head != "DFA0":
	print("Error")

line = f.readline()
while line == "" or line[0] == 'c':
	line = f.readline()
else:
	Sigma = set(line.split())

Q = set()
F = set()
delta = {}
q_0 = None
for line in f:
	if line[0] == 'c':
		continue
	
	if line[0] == '(':
		pass
	
	if q_0 == None:
		q_0 = 
