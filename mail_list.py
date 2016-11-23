import os
import re
from difflib import SequenceMatcher as sm
import numpy as np
import collections
#the root location of the Enron email dataset
maildir = '/home/rohit/maildir'
#Opening the file that contains the alternate names. It is used as a hash map to remove the inconsistencies in the email data.
alter_names = open("alter_names.csv",'r')
#the dictionary containing the alternative names.
names_mapper = {}
#reading the alternative names into a hash
for line in alter_names.readlines():
	split = line.split(':')
	names_mapper[split[0]] = split[1]
#regex for to address	
to = re.compile("X-To:(.*)")
#regex for from address
x_from = re.compile("X-From:(.*)")
#regex for date
date = re.compile("Date:(.*)")
#the file containing the final dataset
mail_list = open("email_processed"+".csv",'w')
#iterating through the inbox directories of each employees
for subdirs in os.listdir(maildir):
	
	sender = ""
	reciever = ""
	#getting mail history from inbox
	inbox = "/home/rohit/maildir/"+subdirs+"/inbox/"
	if os.path.isdir(inbox) != True:
		continue
	else:
		for files in os.listdir(inbox):
			try:
				email_file = open(inbox+"/"+files,'r')
			except IOError:
				continue
			multiple = 1	
			email = email_file.readlines()
			for line in email:
				
				#finding to address
				if to.match(line):
					#extracting emaail address
					search_list = re.sub("X-To:","",line)
					reciever = re.sub("<(.+)","",search_list)
					reciever = reciever.strip(' \t\n\r')
					#removing the entries with multiple email addressess
					letters = collections.Counter(reciever)
					if((letters["'"] > 2) or (letters[","] > 1) or (letters["@"] > 1)):
						print reciever
						multiple = 0
						break
					
					#mapping alternative names to the generalized name.	
					reciever = re.sub(r'^"|"$', '', reciever)
					for key in names_mapper:
						if  key in reciever or reciever in names_mapper[key]:
							reciever = key
							break
													
					
				#finding from address	
				if x_from.match(line):
					#extacting the email addresses
					search_list = re.sub("X-From:","",line)
					sender = re.sub("<(.+)","",search_list)
					sender = sender.strip(' \t\n\r')
					#removing the entries with multiple email addresses
					letters = collections.Counter(sender)
					if(letters["'"] > 2 or letters[","] > 1 or letters["@"] > 1):
						print sender
						multiple = 0				
						break
			
					#mapping alternative names to the generalized name.	
					sender = re.sub(r'^"|"$', '', sender)
					for key in names_mapper:
						if key in sender or sender in names_mapper[key]:
							sender = key
							break
				#finding date field			
				if date.match(line):
					#extracting date
					search_list = re.sub("Date:","",line)
					email_date = search_list.strip('\t\n\r')		
					email_date = re.sub(r'^"|"$', '', email_date)
					
					#print "from
			# writes to file only if there is no multiple email addresses in to or from
			if multiple == 1:		
				mail_list.write(reciever+"|"+sender+"|"+email_date+"\n")
			