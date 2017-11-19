import hashlib

import boto3
import magic

from memoapp import settings

s3_client = boto3.client(
	's3',
	region_name=settings.S3_REGION,
	aws_access_key_id=settings.AWS_ACCESS_KEY,
	aws_secret_access_key=settings.AWS_SECRET_KEY,
)

def upload_to_s3(image):
	image = image.encode('latin-1')
	mime = magic.from_buffer(image, mime=True)
	file_extension = mime.split('/')[1]

	image_md5 = hashlib.md5()
	image_md5.update(image)
	file_name = str(image_md5.hexdigest()) + '.' + file_extension

	s3_client.put_object(
		ACL='private',
		Body=image,
		Bucket=settings.S3_BUCKET,
		Key=file_name,
		ContentType=mime,
	)

	return file_name

def get_signed_url(s3_path):
	return s3_client.generate_presigned_url(
		ClientMethod='get_object',
		Params={
			'Bucket': settings.S3_BUCKET,
			'Key': s3_path,
		},
		ExpiresIn=1800,
	)
