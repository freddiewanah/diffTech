f = open('relations1.txt')
lines = f.readlines()
count = 0
for line in lines:
	if line.startswith('('):
		count += 1

f.close()
print(str(count))
print(str(int(3.6)))

ana = sorted([1,4,5,2,7])
print(ana[0:2])