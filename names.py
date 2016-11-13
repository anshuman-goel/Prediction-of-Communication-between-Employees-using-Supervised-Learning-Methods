import os
import re
import numpy as np
import collections
maildir = '/home/rohit/maildir'
to = re.compile("X-To:(.*)")
last_regex = re.compile(r'(\w*)')
alter_names = open("alter_names.csv",'w')
for subdirs in os.listdir(maildir):
	lastname = last_regex.search(subdirs)
	lastname = subdirs[lastname.start():lastname.end()]
	if lastname == "":
		continue
	#print lastname
	names = set()
	sender = ""
	reciever = ""
	#getting mail history from inbox
	inbox = "/home/rohit/maildir/"+subdirs+"/inbox/"
	#print "subdirs"
	if os.path.isdir(inbox) != True:
		#print "fuck scene"
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
					search_list = re.sub("X-To:","",line)
					reciever = re.sub("<(.+)","",search_list)
					reciever = reciever.strip(' \t\n\r')
					reciever.translate(None,"'")
					reciever = re.sub(r'^"|"$', '', reciever)
					letters = collections.Counter(reciever)
					if(letters["'"] > 2 or letters[","] > 1) or letters["@"] > 1:
						continue
					if lastname.upper() in reciever.upper():
						names.add(reciever)
					if '@ENRON.COM' in reciever.upper():
						names.add(reciever)
		names = list(names)
		name_list = ""
		for name in names:
			name_list = name_list + name + "|"
		name_list = name_list[:-1]		 
		alter_names.write(lastname+":"+name_list+"\n")
#allen_p = open("/home/rohit/ALDA/enron_email_sender/alter_names/allen-p.csv",'r')
#allen_names = set()
#contents = allen_p.readlines()
#for line in contents:
#	allen_names.add(line)
#print list(allen_names)						
