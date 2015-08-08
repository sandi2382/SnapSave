import os
import urllib
import urllib2

baseURL='https://feelinsonice-hrd.appspot.com/bq/blob'
# 200 application/octet-stream

### URLEncoded Form ###
#######################
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

#Migrated to urllib2 for header capability
req = urllib2.Request(prefilledURL)

#Header
print "\nPlease enter your Auth key:"
RAW_Auth_Token = raw_input('')
Auth_Token=str(str(RAW_Auth_Token).replace('\n','').replace(' ',''))

################NAME,##VALUE###########################
req.add_header('Host', 'feelinsonice-hrd.appspot.com')
req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
req.add_header('Connection', 'keep-alive')

#Prompt for language-Don't assume english
req.add_header('Accept-Locale', 'en_US')
req.add_header('X-Snapchat-Client-Auth-Token', str(Auth_Token))
req.add_header('Proxy-Connection', 'keep-alive')
req.add_header('Accept', '*/*')

#Prompt for version - phone - ios
req.add_header('User-Agent', 'Snapchat/9.13.0.0 (iPhone6,1; iOS 8.1.2; gzip)')

#Prompt for language-Don't assume english
req.add_header('Accept-Language', 'en;q=1')
req.add_header('Accept-Encoding', 'gzip')
#req.add_header('Content-Length', '138')

resp = urllib2.urlopen(req).read()
#print resp

snapPathFriendly=snapid.replace('/','_')

#Save picture to subdirectory instead of current folder with src
f=open(str(snapPathFriendly)+'.jpg','wb')
f.write(resp)
f.close()

print "Blob-JPG saved to: "+os.getcwd()+'/'+str(snapPathFriendly)+'.jpg'

