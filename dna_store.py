
import argparse
import csv
import re

def huffman_code(huffman, x, code=''):
	if ('0' in huffman) and (x in huffman['0']['chars']):		
		code += '0'
		return huffman_code(huffman['0'], x, code)
	elif ('1' in huffman) and (x in huffman['1']['chars']):
		code += '1'
		return huffman_code(huffman['1'], x, code)
	elif ('2' in huffman) and (x in huffman['2']['chars']):
		code += '2'
		return huffman_code(huffman['2'],x,code)
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


def dna_encode(trits_code):
	dna_table = {
		'A': ['C', 'G', 'T'],
		'C': ['G', 'T', 'A'],
		'G': ['T', 'A', 'C'],
		'T': ['A', 'C', 'G']
	}
	last = 'A'
	encoded = ""
	for t in trits_code:
		last = dna_table[last][int(t)]
		encoded += last

	return encoded


def dna_decode(dna_code):
	dna_table = {
		'A': ['C', 'G', 'T'],
		'C': ['G', 'T', 'A'],
		'G': ['T', 'A', 'C'],
		'T': ['A', 'C', 'G']
	}

	last = 'A'
	trits_code = ''
	for g in dna_code:
		t = dna_table[last].index(g)
		trits_code += str(t)
		last = g

	return trits_code


def print_huffman_tree(parent_nodes):
	children_nodes = []
	for node in parent_nodes:
		print(' [' + node['chars'].replace('\n', chr(182), 1) + ']' + str(node['f']) + ' ', end='')
		if '0' in node:
			children_nodes.append(node['0'])
			children_nodes.append(node['1'])
			children_nodes.append(node['2'])
	print()
	if len(children_nodes) > 0:
		print_huffman_tree(children_nodes)



source = open('1984.txt', 'r').read()

freq = {}

for c in source:
	if c in freq:
		freq[c] += 1
	else:
		freq[c] = 1

if (len(freq.keys()) % 2) == 0:
	freq[''] = 0

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
	n3 = huffman_queue.pop()
	#print(n3)
	n = {'chars': n1['chars']+n2['chars']+n3['chars'], 'f': n1['f']+n2['f']+n3['f'], '0': n1, '1': n2, '2':n3}
	#print(n)
	huffman_queue.append(n)
	#print(huffman_queue)


huffman_tree = huffman_queue[0]
#print_huffman_tree(huffman_tree)

#print(huffman_code(huffman_tree, 'o'))


huffman_table = {}
huffman_table_inv = {}
for k in freq.keys():
	if k != '':
		code = huffman_code(huffman_tree, k)
		huffman_table[k] = code
		huffman_table_inv[code] = k

#print(huffman_table)
#print(huffman_table_inv)

encoded = huffman_encode(source, huffman_table)

encoded = dna_encode(encoded)
print(encoded)

with open('1984_enc.txt', 'w') as fo:
	fo.write(encoded)
	fo.close()


with open('1984_huffman.csv', 'w', newline='') as fo:
    csv_writer = csv.writer(fo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for k in huffman_table.keys():
    	csv_writer.writerow([k, huffman_table[k]])
    fo.close()

huffman_encoded = dna_decode(encoded)
print(huffman_encoded)


huffman_table_inv2 = {}
with open('1984_huffman.csv', 'r', newline='') as fo:
    csv_reader = csv.reader(fo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        huffman_table_inv2[row[1]] = row[0]


print(huffman_table_inv2)


decoded = huffman_decode(huffman_encoded, huffman_table_inv)
print(decoded)
