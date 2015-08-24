import os
import urllib
import urllib2
from PIL import Image
import time
import errno
import subprocess
import threading
import socket

myLocalIP=([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

#Flags for parse
ua='nullDefault';
token='nullDefault';
uuid='nullDefault';
prefill='nullDefault';
funcFlag='0'	

#Throw in list/array to make check easier with an 'if any()'
items=[ua,token,uuid,prefill]

def timeout( p ):
	if p.poll() is None:
        	try:
        		p.kill()
        	        print '20 seconds are up! Error: process taking too long to complete--terminating'
       		except OSError as e: #race condition
                	if e.errno != errno.ESRCH:
                		raise
def outfileParse(items,ua,token,uuid,prefill,funcFlag):
	#Read file
	with open('outfile', 'r') as inF:
	    for index, line in enumerate(inF):
		#Hot word - Narrows our focus
		host = "/bq/blob"
		#Scary string manipulation - hopefully the format is the same for everyone
		if host in line:
			ua=line.split('User-Agent,')[1].split(':')[1].split(',]')[0];
			token="v3"+line.split('X-Snapchat-Client-Auth-Token,')[1].split(':v3')[1].split(',]')[0];
			uuid=line.split('X-Snapchat-UUID,')[1].split(':')[1].split(',]')[0];
			prefill='?'+'id='+line.split('content')[1].split(':id=')[1].split(',')[0];	

	#Update list with possible changed vars
	items=[ua,token,uuid,prefill]
	#Check if any vars in list have default flag
	if any(x in 'nullDefault' for x in items):
		print "Sorry, data not found\nAre you sure you loaded the snap?";
		return funcFlag;
	else:	
		#print "Values should have changed. =)"
		funcFlag='1';
		return items;


baseURL='https://feelinsonice-hrd.appspot.com/bq/blob'
# 200 application/octet-stream


print "Please start snapchat on your device and go to the conversation of the message you wish to save/see. ~~DO NOT 'Tap to Load' yet~~"
print "Continue? (y/n)\n"
#Prompt y or n

#Get user's ip and use as variable for display here VVVVV
print "Route your device's traffic through an http proxy ("+str(myLocalIP)+":8080)..."
raw_input("Please press Enter to begin capture of flows. (you'll 20 seconds)")

##########SUBPROCESS ADDED##################
#Hopefully, mitmdump is capturing flow
print "Capturing flows for 20 seconds"
print "Hit 'Tap to Load' on the desired snap"
#args=['q','-w','outfile']
#wish to see requests? exlude -q
proc = subprocess.Popen(['mitmdump','-q','-w','outfile'])#silent
#proc = subprocess.Popen(['mitmdump','-q','-w','outfile'])#verbose-ish
t = threading.Timer( 20.0, timeout, [proc] )
t.start()
t.join()
#############################################

###PARSE outfile###
items=outfileParse(items,ua,token,uuid,prefill,funcFlag);
##Check if null defual in any index -- if so terminate.
ua=items[0];
token=items[1];
uuid=items[2];
prefill=items[3];
#if funcFlag='0' ~~~ redo term program -- else continue parse



### URLEncoded Form ###
#######################


'''
print "\n~~~ URLEncoded Form data ~~~"
print "Snap post id:"
#check if 'r' in string (last char)
snapid = raw_input('')
#'id' is a reserved word -_-

print "\nReq_token:"
#check length?
req_token = raw_input('')

print "\nUnix timestamp:"
#Convert current time? - 
#eg. 1439057823280
timestamp = raw_input('')

print "\nYour username?"
username = raw_input('')

prefilledURL=str(baseURL)+'?id='+str(snapid)+'&req_token='+str(req_token)+'&timestamp='+str(timestamp)+'&username='+str(username)

#print '\n'+str(prefilledURL)
'''
prefilledURL=str(baseURL)+prefill
snapid = prefill.split('=')[1].split('&')[0];
req_token = prefill.split('=')[2].split('&')[0];
timestamp = prefill.split('=')[3].split('&')[0];
username =  prefill.split('=')[4].split('&')[0];

#Migrated to urllib2 for header capability
req = urllib2.Request(prefilledURL)

'''
#Header
print "\nPlease enter your Auth key:"
RAW_Auth_Token = raw_input('')
Auth_Token=str(str(RAW_Auth_Token).replace('\n','').replace(' ',''))
'''


################NAME,##VALUE###########################
req.add_header('Host', 'feelinsonice-hrd.appspot.com')
req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
req.add_header('Connection', 'keep-alive')

#Prompt for language-Don't assume english
req.add_header('Accept-Locale', 'en_US')
req.add_header('X-Snapchat-Client-Auth-Token', token)
req.add_header('Proxy-Connection', 'keep-alive')
req.add_header('Accept', '*/*')
req.add_header('User-Agent',ua)

#Prompt for language-Don't assume english
req.add_header('Accept-Language', 'en;q=1')
req.add_header('Accept-Encoding', 'gzip')
#req.add_header('Content-Length', '138')
#req.add_header('X-Snapchat-UUID', uuid)

resp = urllib2.urlopen(req).read()
#print resp

snapPathFriendly=snapid.replace('/','_')

#Save picture to subdirectory instead of current folder with src
f=open(os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg','wb')
f.write(resp)
f.close()

print "\nBlob-JPG saved to: "+os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg\nOpening...\n'
img = Image.open(os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg')
img.show()



