import os
import re
import numpy as np
maildir = '/home/rohit/maildir'
to = re.compile("X-To:(.*)")

for subdirs in os.listdir(maildir):
	names = set()
	sender = ""
	reciever = ""
	alter_names = open("alter_names/"+subdirs+".csv",'w')
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
					reciever = re.sub(r'^"|"$', '', reciever)
					names.add(reciever)
		names = list(names)
		for name in names:
			alter_names.write(name+'|')
#allen_p = open("/home/rohit/ALDA/enron_email_sender/alter_names/allen-p.csv",'r')
#allen_names = set()
#contents = allen_p.readlines()
#for line in contents:
#	allen_names.add(line)
#print list(allen_names)						
