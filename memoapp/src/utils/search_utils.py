
import re

from django.core.cache import cache

from src.models import Memo


class SearchTrieNode(object):
	__slots__ = ('children', 'character', 'memo_ids')

root = SearchTrieNode()
root.children = {}
root.character = None
root.memo_ids = []

character_re = re.compile('[^a-zA-Z0-9\\\/]|_')

def process_word(word, memo_id):
	if not word:
		return

	cur_node = root
	for character in word:
		if character in cur_node.children:
			cur_node = cur_node.children[character]
		else:
			new_node = SearchTrieNode()
			new_node.character = character
			new_node.children = {}
			new_node.memo_ids = []

			cur_node.children[character] = new_node
			cur_node = new_node

	cur_node.memo_ids.append(memo_id)

def process_note(note, memo_id):
	words = note.split(' ')
	for cur_word in words:
		sub_words = []
		if ',' in cur_word:
			sub_words = cur_word.split(',')
		elif '.' in cur_word:
			sub_words = cur_word.split('.')
		else:
			sub_words = [cur_word]
		for word in sub_words:
			word = re.sub(character_re, '', word)
			process_word(word, memo_id)

def index_notes():
	all_memos = Memo.objects.all()
	for memo in all_memos:
		if not cache.get(memo.id):
			process_note(memo.meeting_notes, memo.id)
			cache.set(memo.id, True)

def get_memos_containing_word(word):
	index_notes()

	cur_node = root
	for character in word:
		if not character in cur_node.children:
			return []
		cur_node = cur_node.children[character]

	return Memo.objects.filter(id__in=cur_node.memo_ids)
