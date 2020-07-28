#!/bin/env/python 3
import argparse
from os.path import exists, isdir
from Wordlist import wordlist

parser = argparse.ArgumentParser()
parser.add_argument('input', help='Read input from string or file')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable verbose logging')
parser.add_argument('-s', '--skim', dest='skim', help='Skim first X words from wordlist', type=int, default=0, action='store')
args = parser.parse_args()

if args.verbose == True:
	def verbose_out(flag, message):
		if flag == 0:
			log = '\t[ ]\t'
		elif flag == 1:
			log = '\t[*]\t'
		elif flag == 2:
			log = '\t\t'
		log += message
		print(log)
else:
	def verbose_out(flag, message):
		return None

def readInput(argument):
	cipher_list = []
	if exists(argument):
		with open(argument, 'r') as file:
				temp = file.read().split(' ')
	else:
		temp = argument.split(' ')
	for word in temp:
		cipher_list.append(makeUniform(word))
	return cipher_list

def rot(input, key):
	cypher_text = ''
	for char in input:
		if char.isalpha():
			if char.islower():
				end = 'z'
				begin = 'a'
			elif char.isupper():
				end = 'Z'
				begin = 'A'
			num = ord(char)
			if (num + key) > ord(end):
				x = (num + key) - ord(end)
				cypher_text += chr(x + ord(begin) - 1)
			elif ((num + key <= ord(end))):
				cypher_text += chr(num + key)
		else:
			cypher_text += char
	return cypher_text

def findByLen(list, length, skim):
	matches = []
	for item in list:
		if len(item) == length:
			if len(matches) < skim or skim == 0:
				matches.append(item)
			else:
				return matches
	return matches

def makeUniform(string):
	uniform_string = []
	for c in list(string):
		if c.isalpha():
			uniform_string.append(c.lower())
	return ''.join(uniform_string)

def longestString(list):
	length = 0
	for item in list:
		if len(item) > length:
			length = len(item)
	return length

def crackCipher(cipher_list, cipher_index, wordlist, wordlist_index, key, length, max_len, skim):
	cipher_targets = findByLen(cipher_list, length, 0)
	if len(cipher_targets) == 0:
		return (cipher_list, cipher_index, wordlist, wordlist_index, key, length + 1, max_len, skim)
	wordlist_guesses = findByLen(wordlist, length, skim)

	verbose_out(0, f'Trying Bruteforce with settings cipher_index = {cipher_index}, wordlist_index = {wordlist_index}, key = {key}, length = {length}')
	attempt = rot(makeUniform(wordlist_guesses[wordlist_index]), key)
	target = makeUniform(cipher_targets[cipher_index])
	
	if attempt == target:
		verbose_out(1, f'Found key = {key}')
		return key

	elif cipher_index < len(cipher_targets) - 1:
		return (cipher_list, cipher_index + 1, wordlist, wordlist_index, key, length, max_len, skim)

	elif wordlist_index < len(wordlist_guesses) - 1:
		return (cipher_list, 0, wordlist, wordlist_index + 1, key, length, max_len, skim)

	elif key < 25:
		return (cipher_list, 0, wordlist, 0, key + 1, length, max_len, skim)

	elif length < max_len:
		return (cipher_list, 0, wordlist, 0, 0, length + 1, max_len, skim)

	else:
		return None

cipher_list = readInput(args.input)
max_len = longestString(cipher_list)
skim = args.skim
key = (cipher_list, 0, wordlist, 0, 0, 1, max_len, skim)

while type(key) != int and key != None:
	key = crackCipher(*key)

if key == None:
	print("Could not find the cipher key")
elif key != None:
	print("Key found!")
	print(f'\tKey = {key}')
	verbose_out(0, f'Decrypting text...')
	decrypted_text = rot(args.input, key)
	print(f'Decrypted text:\n\t{decrypted_text}')