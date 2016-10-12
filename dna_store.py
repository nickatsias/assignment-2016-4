source = "hello, world"

freq = {}
for c in source:
	if c in freq:
		freq[c] += 1
	else:
		freq[c] = 1

print(freq)