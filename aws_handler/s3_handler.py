import boto3, sys, logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class S3Handler(object):

	s3 = boto3.resource('s3')

	def __init__(self, bucket, key, filepath):
		self.bucket = bucket
		self.key = key
		self.filepath = filepath
	
	def download_file_from_s3(self, bucket, key, filepath):
		self.s3.Bucket(self.bucket).download_file(self.key, self.filepath)

	def upload_file_to_s3(self, bucket,key,filepath):
		logger.info("Uploading file to S3...")
		self.s3.Object(self.bucket,self.key).upload_file(self.filepath)
		logger.info("Uploaded new file to S3!")
		
		
