import hashlib

import boto3
import magic

from memoapp import settings
from src import constants

s3_client = boto3.client(
	's3',
	region_name=settings.S3_REGION,
	aws_access_key_id=settings.AWS_ACCESS_KEY,
	aws_secret_access_key=settings.AWS_SECRET_KEY,
)


def upload_to_s3(blob, file_extension='json', path_prefix=''):
	'''
		Upload the given blob to S3
	'''
	blob_md5 = hashlib.md5()
	blob_md5.update(blob)
	file_name = str(blob_md5.hexdigest()) + '.' + file_extension
	file_name = '{}/{}'.format(path_prefix, file_name) if path_prefix else file_name

	s3_client.put_object(
		ACL='private',
		Body=blob,
		Bucket=settings.S3_BUCKET,
		Key=file_name,
	)

	return file_name


def get_from_s3(path):
	response = s3_client.get_object(
		Bucket=settings.S3_BUCKET,
		Key=path,
	)
	return response['Body'].read()


def get_signed_url(s3_path):
	'''
		Get a signed URL that's valid for a temporary time period for the given S3 path
	'''
	return s3_client.generate_presigned_url(
		ClientMethod='get_object',
		Params={
			'Bucket': settings.S3_BUCKET,
			'Key': s3_path,
		},
		ExpiresIn=1800,
	)


def list_keys_with_prefix(prefix):
	if prefix not in constants.ALLOWED_LIST_PREFIXES:
		raise Exception('You dont have permissions to list this prefix')

	contents = s3_client.list_objects(Bucket=settings.S3_BUCKET, Prefix=prefix)[constants.S3_RESPONSE_CONTENTS_STR]
	object_keys = []
	for content in contents:
		object_keys.append(content.get(constants.S3_RESPONSE_KEY_STR))

	return object_keys
