import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DictionaryFileHandler:
	
	def __init__(self,filepath):
		self.filepath = filepath

	def __get_lines_from_file(self):
		local_file = open(self.filepath,"r+")
		lines = local_file.readlines()
		local_file.close()
		return lines
	
	def __does_word_exist_in_file(self,entry):
		lines = self.__get_lines_from_file()
		# ITERATE THROUGH WORDS; IGNORE HEADER LINE
		for line in lines[1:]:
			word = line.split(",")[0]
			if entry == word:
				return True
		return False

	@classmethod
	def create_new_dictionary(cls,filepath):
		logger.info("File does not exist. Creating...")
		local_file = open(filepath, 'w+')
		local_file.write("entry,definition\n")
		local_file.close()
		logger.info("New dictionary created.")
	
	def add_entry_to_file(self,word,definition):
		if not self.__does_word_exist_in_file(word):
			logger.info(word + " does not exist in dictionary")
			local_file = open(self.filepath, 'a')
			local_file.write(word+","+definition+"\n")
			local_file.close()
			logger.info(word + " written to file.")
			return { 
				"word" 		: word,
				"definition" 	: definition
				}
		else:
			raise Exception("WordAlreadyExists: Word already exists! Not adding entry.")
	
	def delete_word_from_file(self,word):
		if self.__does_word_exist_in_file(word):
			logger.info(word + " exists in file. Deleting...")
			self.__remove_word_from_file(word)
			logger.info(word + " deleted from file.")
		else:
			raise Exception("WordNotFound: Word does not exist. Exiting...")	
	
	def __remove_word_from_file(self,word):
		lines 		= self.__get_lines_from_file()
		local_file	= open(self.filepath,"w+")
		
		# ALWAYS WRITE THE HEADER LINE
		local_file.write(lines[0])
		lines		= lines[1:]

		for line in lines:
			entry	= line.split(",")[0]	
			if entry != word:
				local_file.write(line)
		local_file.close()
	
