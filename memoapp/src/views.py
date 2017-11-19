# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from src import constants
from src.models import Memo, Users
from src.utils import (get_memos_containing_word, get_signed_url, index_notes,
                       upload_to_s3)

memo_users = lambda memo: [user.name for user in memo.meeting_with.all()]

@require_GET
def index(request):
	return render(request, 'index.html')

@require_POST
def create_memo(request):
	memo_image = request.POST.get('memo-image') or ''
	memo_notes = request.POST.get('memo-notes') or ''
	memo_with = request.POST.get('memo-with') or ''
	memo_date = request.POST.get('memo-date')

	if not (memo_image or memo_notes) or not memo_date:
		return HttpResponseBadRequest('Invalid input')

	if len(memo_image) > constants.MAX_IMAGE_SIZE or len(memo_notes) > constants.MAX_NOTE_SIZE:
		return HttpResponseBadRequest('Image/Note too large')

	memo_image_upload_path = upload_to_s3(memo_image) if memo_image else None

	memo_with_users = []
	for user_name in memo_with.split(','):
		user_name = user_name.strip()
		if user_name:
			memo_with_users.append(Users.objects.get_or_create(name=user_name)[0])

	memo_obj = Memo.objects.create(
		date=memo_date,
		meeting_notes=memo_notes,
		image_path=memo_image_upload_path,
	)
	if memo_with_users:
		memo_obj.meeting_with.add(*memo_with_users)

	try:
		# Assuming single threaded - gotta change if we are multi-threaded
		index_notes()
	except:
		pass

	return HttpResponse('Created')

def _get_datewise_sorted_memo_previews(all_memos):
	datewise_memos = {}
	for memo in all_memos:
		note_preview = memo.meeting_notes[:constants.TRIM_LENGTH] if memo.meeting_notes else ''
		if len(memo.meeting_notes) > constants.TRIM_LENGTH:
			note_preview += '...'
		image_signed_url = get_signed_url(memo.image_path) if memo.image_path else ''
		memo_date = memo.date.strftime('%Y-%m-%d')
		memo_dict = {
			'with': memo_users(memo),
			'notes': note_preview,
			'image': image_signed_url,
			'id': memo.id,
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
	all_memos = Memo.objects.all()
	sorted_datewise_memos = _get_datewise_sorted_memo_previews(all_memos)
	return render(request, 'history.html', context={'memos': sorted_datewise_memos})

@require_GET
def get_memo(request, memo_id):
	memo = Memo.objects.get(id=memo_id)

	image_signed_url = get_signed_url(memo.image_path) if memo.image_path else ''
	res = {
		'with': memo_users(memo),
		'notes': memo.meeting_notes,
		'image': image_signed_url,
		'date': memo.date.strftime('%d %b, %Y'),
	}
	return HttpResponse(json.dumps(res), content_type='application/json')

@require_GET
def search_page(request):
	return render(request, 'search.html')

@require_GET
def search(request):
	date = request.GET.get('date')
	attendees = request.GET.get('with')
	contains = request.GET.get('contains')

	if not (date or attendees or contains):
		return HttpResponseBadRequest('Atleast one search parameter must be supplied')

	list_of_attendees = []
	for attendee in attendees.split(','):
		attendee = attendee.strip()
		list_of_attendees.append(attendee)

	users = Users.objects.filter(name__in=list_of_attendees) if list_of_attendees else None
	date = datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None

	word_to_search = contains.split(' ')[0] # defense against bad input in case someone's meddling with the api
	search_results = get_memos_containing_word(word_to_search) if word_to_search else Memo.objects.all()

	if users:
		search_results = search_results.filter(meeting_with__in=users)

	if date:
		search_results = search_results.filter(date=date)

	if search_results.count() > constants.MAX_SEARCH_RESULTS:
		return HttpResponseBadRequest('More than {} search results'.format(constants.MAX_SEARCH_RESULTS))

	search_preview = _get_datewise_sorted_memo_previews(search_results)

	return HttpResponse(json.dumps(search_preview), content_type='application/json')
