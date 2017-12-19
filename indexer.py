# -*- coding: utf-8 -*-

import re

from soundex import soundex
import cPickle as pickle

if __name__ == '__main__':
	f = open('./queries_all.txt', 'r')

	sound_dict = {}
	frequences = {}
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

		for word in correct_words:
			word = word.strip()
			if word == '':
				continue

			total_dict.add(word)

			if len(vals) == 2:
				if word in frequences:
					frequences[word] += 1
				else:
					frequences[word] = 1

			sndx = soundex(word)
			if sndx in sound_dict:
				sound_dict[sndx].add(word)
			else:
				sound_dict[sndx] = set([word])

		mistake_words = re.split(' |\.|\,', query)

		for word in mistake_words:
			word = word.strip()
			if word == '':
				continue

			if word in frequences:
				frequences[word] += 1
			else:
				frequences[word] = 1

		line = f.readline().strip()

	with open('souds.bin', 'wb') as sounds:
		pickle.dump(sound_dict, sounds)
	with open('freqs.bin', 'wb') as freqs:
		pickle.dump(frequences, freqs)
	with open('dict.bin', 'wb') as total:
		pickle.dump(total_dict, total)

 	f.close()