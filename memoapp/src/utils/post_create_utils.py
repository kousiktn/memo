import boto3

polly_client = boto3.client(
	'polly',
	region_name=settings.S3_REGION,
	aws_access_key_id=settings.AWS_ACCESS_KEY,
	aws_secret_access_key=settings.AWS_SECRET_KEY,
)
