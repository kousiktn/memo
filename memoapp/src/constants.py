'''
Related to views
'''

MAX_NOTE_SIZE = 100 * 1024 #100KB

TRIM_LENGTH = 75

MAX_SEARCH_RESULTS = 10

'''
Related to models
'''
class NoteSchemaKeysStr(object):
	DATE = 'date'
	TEXT_NOTE = 'text_note'

TEXT_NOTE_S3_FOLDER_PREFIX = 'text_blobs'
DATE_FORMAT = '%Y-%m-%d'

'''
Related to utils
'''
ALLOWED_LIST_PREFIXES = {TEXT_NOTE_S3_FOLDER_PREFIX}
S3_RESPONSE_CONTENTS_STR = 'Contents'
S3_RESPONSE_KEY_STR = 'Key'
