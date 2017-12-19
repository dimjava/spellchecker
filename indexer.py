# -*- coding: utf-8 -*-

import re
from mmh3 import hash as mhash
from soundex import soundex
import cPickle as pickle

if __name__ == '__main__':
	f = open('./queries_all.txt', 'r')

	sound_dict = {}
	frequences = {}
	# frequences of couples of words
	frequences2 = {}
	total_dict = set()

	line = f.readline().strip()

	cnt = 0
	while line:
		# cnt += 1
		# if cnt % 10000 == 0:
		# 	print(cnt)

		vals = line.split('\t')
		query = vals[0]
		correct = vals[-1]	

		correct_words = re.split(' |\.|\,', correct)

		prev = ''
		for word in correct_words:
			word = word.strip()
			if word == '':
				continue

			total_dict.add(mhash(word))

			if prev != '':
				key = mhash('&'.join([prev, word]))
				if key in frequences2:
					frequences2[key] += 1
				else:
					frequences2[key] = 1
			prev = word

			if len(vals) == 2:
				if mhash(word) in frequences:
					frequences[mhash(word)] += 1
				else:
					frequences[mhash(word)] = 1

			sndx = soundex(word)
			if sndx in sound_dict:
				sound_dict[sndx].add(word)
			else:
				sound_dict[sndx] = set([word])

		mistake_words = re.split(' |\.|\,', query)


		prev = ''
		for word in mistake_words:
			word = word.strip()
			if word == '':
				continue

			if prev != '':
				key = mhash('&'.join([prev, word]))
				if key in frequences2:
					frequences2[key] += 1
				else:
					frequences2[key] = 1
			prev = word

			if mhash(word) in frequences:
				frequences[mhash(word)] += 1
			else:
				frequences[mhash(word)] = 1

		line = f.readline().strip()

	with open('souds.bin', 'wb') as sounds:
		pickle.dump(sound_dict, sounds)
	with open('freqs.bin', 'wb') as freqs:
		pickle.dump(frequences, freqs)
	with open('freqs2.bin', 'wb') as freqs2:
		pickle.dump(frequences2, freqs2)
	with open('dict.bin', 'wb') as total:
		pickle.dump(total_dict, total)

 	f.close()