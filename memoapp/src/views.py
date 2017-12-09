# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from src import constants
from src.models import Memo
# from src.utils import (get_memos_containing_word, get_signed_url, index_notes, upload_to_s3)

# memo_users = lambda memo: [user.name for user in memo.meeting_with.all()]

@require_GET
def index(request):
	return render(request, 'index.html')

@require_POST
def create_memo(request):
	'''
		This function creates a new memo
		(memo_image/memo_notes) and memo_date are mandatory parameters

		memo_image can't exceed 2MB
		memo_notes can't exceed 100KB

		memo_with is an optional parameter to say who the meeting attendees were
	'''
	memo_notes = request.POST.get('memo-notes') or ''
	memo_date = request.POST.get('memo-date')

	if len(memo_notes) > constants.MAX_NOTE_SIZE:
		return HttpResponseBadRequest('Sorry - Request too large')

	if not memo_notes or not memo_date:
		return HttpResponseBadRequest('Invalid input')

	memo_obj = Memo.create(
		memo_date,
		memo_notes,
	)

	# try:
	# 	# Assuming single process/worker for now - gotta change if we are multi-threaded
	# 	index_notes()
	# except:
	# 	pass

	return HttpResponse('Created')


def _get_datewise_sorted_memo_previews(all_memos):
	'''
		Given a list of memos this function nicely formats each one of them into a preview-like format
	'''
	datewise_memos = {}
	for memo in all_memos:
		text_content = memo.get_text_content()
		note_preview = text_content[:constants.TRIM_LENGTH] + '...' if text_content else ''

		memo_date = memo.get_date().strftime('%Y-%m-%d')
		memo_dict = {
			'notes': note_preview,
			'id': memo.get_id(),
		}
		if memo_date in datewise_memos:
			datewise_memos[memo_date].append(memo_dict)
		else:
			datewise_memos[memo_date] = [memo_dict]

	all_dates = datewise_memos.keys()
	all_dates.sort()
	descending_dates = all_dates[::-1]

	sorted_datewise_memos = [(date, datewise_memos[date]) for date in descending_dates]
	return sorted_datewise_memos


@require_GET
def history(request):
	'''
		View function for history page
	'''
	all_memos = Memo.list_all()
	sorted_datewise_memos = _get_datewise_sorted_memo_previews(all_memos)
	return render(request, 'history.html', context={'memos': sorted_datewise_memos})


@require_GET
def get_memo(request):
	'''
		View function to get details about a single memo
		If we get more requirements like this and the app has multiple models, should
		probably consider using Django Rest Framework.
	'''
	id = request.GET.get('id')

	if not id:
		return HttpResponseBadRequest('Invalid memo ID')

	memo = Memo(id)

	res = {
		'notes': memo.get_text_content(),
		'date': memo.get_date().strftime('%d %b, %Y'),
	}
	return HttpResponse(json.dumps(res), content_type='application/json')

# @require_GET
# def search_page(request):
# 	'''
# 		Search page - pretty basic
# 	'''
# 	return render(request, 'search.html')

# @require_GET
# def search(request):
# 	'''
# 		Search api
# 		It mandates that any one of the search parameters be given

# 		Limits results to a max value(look at constants)
# 	'''
# 	date = request.GET.get('date')
# 	attendees = request.GET.get('with')
# 	contains = request.GET.get('contains')

# 	if not (date or attendees or contains):
# 		return HttpResponseBadRequest('Atleast one search parameter must be supplied')

# 	list_of_attendees = []
# 	for attendee in attendees.split(','):
# 		attendee = attendee.strip()
# 		list_of_attendees.append(attendee)

# 	users = Users.objects.filter(name__in=list_of_attendees) if list_of_attendees else None
# 	date = datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None

# 	word_to_search = contains.split(' ')[0] # defense against bad input in case someone's meddling with the api
# 	search_results = get_memos_containing_word(word_to_search) if word_to_search else Memo.objects.all()

# 	if users:
# 		search_results = search_results.filter(meeting_with__in=users)

# 	if date:
# 		search_results = search_results.filter(date=date)

# 	if search_results.count() > constants.MAX_SEARCH_RESULTS:
# 		return HttpResponseBadRequest('More than {} search results'.format(constants.MAX_SEARCH_RESULTS))

# 	search_preview = _get_datewise_sorted_memo_previews(search_results)

# 	return HttpResponse(json.dumps(search_preview), content_type='application/json')
