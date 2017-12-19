# -*- coding: utf-8 -*-

import cPickle as pickle
import re
from nltk.metrics import edit_distance
from soundex import soundex

alpha = 2.0

sound_dict = {}
frequences = {}
total_dict = set()

if __name__ == '__main__':
	with open('souds.bin', 'rb') as sounds:
		sound_dict = pickle.load(sounds)
	with open('freqs.bin', 'rb') as freqs:
		frequences = pickle.load(freqs)
	with open('dict.bin', 'rb') as total:
		total_dict = pickle.load(total)

	query = raw_input()

	while query:
		# print('QUERY: ' + query)

		query = query.strip()
		words = re.split(' |\.|\,', query)

		result = []
		word_probs = []
		for word in words:
			word = word.strip()
			# if word in total_dict:
			# 	result.append(word)
			# 	continue

			mmax = -1
			mfix = word
			sndx = soundex(word)

			p_orig = 1.0
			if word in frequences:
				p_orig = frequences[word]

			# print(sndx)
			# print(sndx in sound_dict)
			if sndx in sound_dict:
				# print(', '.join(sound_dict[sndx]))
				
				for fix in sound_dict[sndx]:
					prob = alpha ** (-edit_distance(fix, word)) * frequences[fix] / p_orig
					if prob > mmax:
						mmax = prob
						mfix = fix
				result.append(mfix)
				# word_probs.append(mmax)

		# print(word_probs)
		# print('\t'.join([query, ' '.join(result)]))
		print(' '.join(result))
		try:
			query = raw_input()
		except:
			break