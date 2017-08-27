import configparser, sys, logging
from botocore.exceptions import ClientError
from file_handler.handler import DictionaryFileHandler
from aws_handler.s3_handler import S3Handler

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


config = configparser.ConfigParser()
config.read('config.ini')
aws_config = config['aws']
bucket = aws_config['bucket']
filename = aws_config['filename']
path = "/tmp/"+filename

def lambda_handler(event, context):
	# CHECK LAMBDA EVENT ARGS BEFORE PROCEEDING
	if 'action' not in event:
		raise Exception("No API action specified! Must add action in body.")
	
	if 'word' not in event:
		raise Exception("No word specified!")

	action			= event['action']
	word			= event['word']
	dictionary_handler	= DictionaryFileHandler(path)
	s3_handler		= S3Handler(bucket,filename,path)

	if action == 'add':
		if 'definition' not in event:
			raise Exception("DefinitionNotFound: \
				No definition specified! Must add definition to body.")
		definition = event['definition']
		return add_entry(word, definition,dictionary_handler,s3_handler)

	elif action == 'delete':
		return delete_entry(word, dictionary_handler, s3_handler)

	else:
		raise Exception("APIMethodNotFound: Did not find API method.")
	
def retrieve_file_from_s3(s3handler):
	try:
		s3handler.download_file_from_s3(bucket,filename,path)
	except ClientError as e:
		DictionaryFileHandler.create_new_dictionary(path)
		s3handler.upload_file_to_s3(bucket,filename,path)

def add_entry(word,definition,filehandler,s3handler):
	retrieve_file_from_s3(s3handler)
	response = filehandler.add_entry_to_file(word,definition)
	s3handler.upload_file_to_s3(bucket,filename,path)
	return response

def delete_entry(word,filehandler,s3handler):
	retrieve_file_from_s3(s3handler)
	response = filehandler.delete_word_from_file(word)
	s3handler.upload_file_to_s3(bucket,filename,path)
	return response



if __name__ == '__main__':
	lambda_handler({"action":"delete",
			"word":"entry", 
			"definition" : "the word's definition"}, "context")
