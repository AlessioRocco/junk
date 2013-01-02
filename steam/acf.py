#!/usr/bin/env python

import sys
import depotcache
from StringIO import StringIO

# The acf files look like a pretty simple format - I wouldn't be surprised if a
# python parser already exists that can process it (even by chance), but I
# don't know of one offhand so here's a quick one I hacked up

def scan_for_next_token(f):
	while True:
		byte = f.read(1)
		if byte == '':
			raise EOFError
		elif byte in ['"', '{']:
			return byte

def parse_quoted_token(f):
	ret = ''
	while True:
		byte = f.read(1)
		if byte == '':
			raise EOFError
		elif byte == '"':
			return ret
		else:
			ret += byte

def scan_block(f):
	ret = ''
	level = 0
	while True:
		byte = f.read(1)
		if byte == '':
			raise EOFError
		if byte == '{':
			level += 1
		elif byte == '}':
			level -= 1
			if level < 0:
				return ret
		ret += byte

class AcfNode(dict):
	def __init__(self, f):
		while True:
			try:
				token_type = scan_for_next_token(f)
			except EOFError:
				return
			if token_type != '"':
				raise TypeError('Error parsing ACF format - missing node name?')
			name = parse_quoted_token(f)

			token_type = scan_for_next_token(f)
			if token_type == '"':
				self[name] = parse_quoted_token(f)
			elif token_type == '{':
				self[name] = AcfNode(StringIO(scan_block(f)))
			else:
				assert(False)

def parse_acf(filename):
	with file(filename, 'r') as f:
		root = AcfNode(f)
	return root

def main():
	for filename in sys.argv[1:]:
		print parse_acf(filename)


if __name__ == '__main__':
	main()
