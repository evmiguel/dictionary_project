import os.path
import boto3
from botocore.exceptions import ClientError
import configparser
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


config = configparser.ConfigParser()
config.read('config.ini')
aws_config = config['aws']

bucket = aws_config['bucket']
filename = aws_config['filename']
s3 = boto3.resource('s3')

path = "/tmp/"+filename

def retrieve_file_from_s3():
	try:
		s3.Bucket(bucket).download_file(filename,path)
	except ClientError as e:
		logger.info("File does not exist. Creating...")
		local_file = open(path, 'w+')
		local_file.write("entry,definition\n")
		local_file.close()
		s3.Object(bucket,filename).upload_file(path)

def add_entry(word,definition):
	retrieve_file_from_s3()
	if not does_word_exist:
		logger.info("Word does not exist in dictionary")
		local_file = open(path, 'a')
		local_file.write(word+","+definition+"\n")
		local_file.close()
		s3.Object(bucket,filename).upload_file(path)
		return { 
			"word" 		: word,
			"definition" 	: definition
			}
	else:
		raise Exception("Word already exists! Not adding entry.")	

def does_word_exist(entry):
	lines = get_lines_from_file()
	for line in lines:
		word = line.split(",")[0]
		if entry == word:
			return True
	return False

def delete_word(word):
	if does_word_exist(word):
		logger.info("Word exists. Deleting...")
		remove_word_from_dictionary(word)
	else:
		raise Exception("Word does not exist. Exiting...")	

def remove_word_from_dictionary(word):
	retrieve_file_from_s3()
	lines 		= get_lines_from_file()
	local_file	= open(path,"w+")
	for line in lines:
		entry	= line.split(",")[0]	
		if entry != word:
			local_file.write(line)
	local_file.close()
	s3.Object(bucket,filename).upload_file(path)

def get_lines_from_file():
	local_file = open(path,"r+")
	lines = local_file.readlines()
	local_file.close()
	return lines

if __name__ == '__main__':
	remove_word_from_dictionary("word")
