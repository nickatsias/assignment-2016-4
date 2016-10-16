
import re

def huffman_code(huffman, x, code=''):
	if ('left' in huffman) and (x in huffman['left']['chars']):		
		code += '0'
		return huffman_code(huffman['left'], x, code)
	elif ('right' in huffman) and (x in huffman['right']['chars']):
		code += '1'
		return huffman_code(huffman['right'], x, code)
	else:
		return code


def huffman_encode(source, huffman_table):
 	return ''.join(list(map(lambda c: huffman_table[c], source)))

def huffman_decode(encoded, huffman_table_inv):
	codes = '|'.join(huffman_table_inv.keys())
	regex_codes = re.compile(codes)
	decoded = ""
	for code in regex_codes.finditer(encoded):
		decoded += huffman_table_inv[code.group()]
	return decoded





source = "hello, world"

freq = {}

for c in source:
	if c in freq:
		freq[c] += 1
	else:
		freq[c] = 1

#print(freq)


huffman_queue = []

for k in freq.keys():
	huffman_queue.append({'chars': k, 'f': freq[k]})

#print(huffman_queue)

while (len(huffman_queue) > 1):
	huffman_queue = sorted(huffman_queue, key=lambda value: value['f'], reverse=True)
	#print(huffman_queue)
	n1 = huffman_queue.pop()
	#print(n1)
	n2 = huffman_queue.pop()
	#print(n2)
	n = {'chars': n1['chars']+n2['chars'], 'f': n1['f']+n2['f'], 'left': n1, 'right': n2}
	#print(n)
	huffman_queue.append(n)
	#print(huffman_queue)


huffman_tree = huffman_queue[0]
#print(huffman_tree)

#print(huffman_code(huffman_tree, 'o'))


huffman_table = {}
huffman_table_inv = {}
for k in freq.keys():
	code = huffman_code(huffman_tree, k)
	huffman_table[k] = code
	huffman_table_inv[code] = k

print(huffman_table)
print(huffman_table_inv)

encoded = huffman_encode(source, huffman_table)
print(encoded)


decoded = huffman_decode(encoded, huffman_table_inv)
print(decoded)
