# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from src import constants
from src.models import Memo, Users
from src.utils import upload_to_s3


# Create your views here.
def index(request):
	return render(request, 'index.html')

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
		memo_with_users.append(Users.objects.get_or_create(name=user_name)[0])

	memo_obj = Memo.objects.create(
		date=memo_date,
		meeting_notes=memo_notes,
		image_path=memo_image_upload_path,
	)
	memo_obj.meeting_with.add(*memo_with_users)

	return HttpResponse('Created')
