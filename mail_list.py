import os
import re
from difflib import SequenceMatcher as sm
import numpy as np
maildir = '/home/rohit/maildir'
alter_names = {}
alter = []
to = re.compile("X-To:(.*)")
x_from = re.compile("X-From:(.*)")
for subdirs in os.listdir(maildir):
	alter = []
	sender = ""
	reciever = ""
	mail_list = open("preprocessed/"+subdirs+".csv",'w')
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
					#print "to"
					
				if x_from.match(line):
					search_list = re.sub("X-From:","",line)
					sender = re.sub("<(.+)","",search_list)		
					#print "from"
			sender = sender.strip(' \t\n\r')
			reciever = reciever.strip(' \t\n\r')	
			mail_list.write(reciever+"|"+sender+"\n")
			if(sm(None,subdirs,reciever) >= 0.0):
				alter.append(reciever)
	#getting info from sent folder
	sender = ""
	reciever = ""
	#mail_list.write("********************GOING TO SENT FOLDER***********************************\n")
	sent = "/home/rohit/maildir/"+subdirs+"/sent/"
	if os.path.isdir(sent) != True:
		continue
	else:
		for files in os.listdir(sent):
			print files
			try:
				email_file = open(sent+"/"+files,'r')
			except IOError:
				continue
			email = email_file.readlines()
			#print "files"
			for line in email:
				#print "line"
				if to.match(line):
					search_list = re.sub("X-To:","",line)
					reciever = re.sub("<(.+)","",search_list)
					#print "to"
					
				if x_from.match(line):
					search_list = re.sub("X-From:","",line)
					sender = re.sub("<(.+)","",search_list)		
					#print "from"
			sender = sender.strip(' \t\n\r')
			reciever = reciever.strip(' \t\n\r')	
			mail_list.write(sender+"|"+reciever+"\n")
			#trying to fill the alter_names
			if(sm(None,subdirs,sender) >=  0.0):
				alter.append(sender)
	if len(alter) != 0:
		alter = list(set(alter))
		alter_names[subdirs] = alter
np.save('alter_names_dict.npy', alter_names)
 
				
