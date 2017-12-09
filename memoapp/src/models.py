# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from src import constants
from src.utils import get_from_s3, upload_to_s3, list_keys_with_prefix


class Note(object):
	'''
		Captures a unit of entity of a note that might contain different types of content
	'''
	def __init__(self, note_fields):
		self.note_dict = {}
		for key, value in note_fields.iteritems():
			self.note_dict[key] = value

	def serialize_to_text(self):
		return json.dumps(self.note_dict)

	def get(self, key, default=None):
		return self.note_dict.get(key, default)


class Memo(object):
	'''
		A memo is the user representation of a note
		It encompasses everything that *the user* considers as a note
	'''
	def __init__(self, blob_path):
		self.blob_path = blob_path
		self.note = Note(json.loads(get_from_s3(self.blob_path)))

	@classmethod
	def create(cls, date, note_content):
		note = Note(note_fields={
			constants.NoteSchemaKeysStr.DATE: date,
			constants.NoteSchemaKeysStr.TEXT_NOTE: note_content,
		})

		note_blob_str = note.serialize_to_text()
		s3_obj_name = upload_to_s3(note_blob_str, path_prefix=constants.TEXT_NOTE_S3_FOLDER_PREFIX)

		return Memo(s3_obj_name)

	@classmethod
	def list_all(cls):
		memo_keys = list_keys_with_prefix(constants.TEXT_NOTE_S3_FOLDER_PREFIX)

		all_memos = []
		for key in memo_keys:
			all_memos.append(Memo(key))

		return all_memos

	def get_text_content(self):
		return self.note.get(constants.NoteSchemaKeysStr.TEXT_NOTE, '')

	def get_date(self):
		date_str = self.note.get(constants.NoteSchemaKeysStr.DATE, '')
		return datetime.datetime.strptime(date_str, constants.DATE_FORMAT).date()

	def get_id(self):
		'''
			The S3 path is the unique ID for the current memo
		'''
		return self.blob_path
