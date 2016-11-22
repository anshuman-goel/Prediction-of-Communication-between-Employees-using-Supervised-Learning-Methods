import os
import re
from difflib import SequenceMatcher as sm
import numpy as np
import collections
maildir = '/home/rohit/maildir'
alter_names = {}
alter = []
#reading the alternative names into a hash
alter_names = open("alter_names.csv",'r')
names_mapper = {}
for line in alter_names.readlines():
	split = line.split(':')
	names_mapper[split[0]] = split[1]
to = re.compile("X-To:(.*)")
x_from = re.compile("X-From:(.*)")
date = re.compile("Date:(.*)")
for subdirs in os.listdir(maildir):
	multiple = 1
	alter = []
	sender = ""
	reciever = ""
	mail_list = open("preprocessed/"+subdirs+".csv",'w') # the mail list files for each employee
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
			email = email_file.readlines()
			#print "files"
			for line in email:
				#print "line"
				if to.match(line):
					#removing the entries with multiple email addressess
					letters = collections.Counter(reciever)
					if(letters["'"] > 2 or letters[","] > 1 or letters["@"] > 1):
						multiple = 0
						break
					search_list = re.sub("X-To:","",line)
					reciever = re.sub("<(.+)","",search_list)
					reciever = reciever.strip(' \t\n\r')
					
					
					
					#mapping alternative names to the generalized name.	
					reciever = re.sub(r'^"|"$', '', reciever)
					for key in names_mapper:
						if  key in reciever or reciever in names_mapper[key]:
							reciever = key
							break
													
					#print "to"
					
				if x_from.match(line):
					#removing the entries with multiple email addresses
					letters = collections.Counter(sender)
					if(letters["'"] > 2 or letters[","] > 1 or letters["@"] > 1):
						multiple = 0				
						break
					search_list = re.sub("X-From:","",line)
					sender = re.sub("<(.+)","",search_list)
					sender = sender.strip(' \t\n\r')
					
					
					#mapping alternative names to the generalized name.	
					sender = re.sub(r'^"|"$', '', sender)
					for key in names_mapper:
						if key in sender or sender in names_mapper[key]:
							sender = key
							break
							
				if date.match(line):
					search_list = re.sub("Date:","",line)
					email_date = search_list.strip('\t\n\r')		
					email_date = re.sub(r'^"|"$', '', email_date)
					
					#print "from
			
			if multiple == 1:		
				mail_list.write(reciever+"|"+sender+"|"+email_date+"\n")
			