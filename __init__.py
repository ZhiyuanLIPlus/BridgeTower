import re
import urllib
import urllib2
import cookielib
import threading
import time

from bs4 import BeautifulSoup
from login import WeiboLogin

#global variables
username = "user"
passwd = "pwd"
expandLevel = 1

dicID_Name = dict()
dicID_Count= dict()
dicID_Img  = dict()
tlock = threading.Lock()
temp_count = 0
Total_threadSize = 300

# OpenLink thread
class OpenLinkThread(threading.Thread):
    def __init__(self, uid,actuallevel):
        self.uid          = uid
        self.actuallevel  = actuallevel
        threading.Thread.__init__(self)
    def run(self):
        global tlock
        global temp_count
        global dicID_Name
        global dicID_Count
        global dicID_Img
        global Total_threadSize

        print "\nNew thread begins:"+self.uid
        starturl = 'http://www.weibo.com/%s/follow?from=page_100505&wvr=6&mod=headfollow'%self.uid
        data  = loginer.get_html(starturl)
        data_clean = data.replace("\\\"","\"").replace("\\/","/")

        pattern_html = re.compile(r'followTab/index.*"html":"(.*?)\\r\\n"}')
        pattern_nextpagelink = re.compile(r'class="page next S_txt1 S_line1" href="(.*?)">')

        match1 = pattern_html.search(data_clean)
        #no follwers: quit
        if match1 is None:
            print "No followers"
            return
        followerlist = match1.group(1)

        nextfollowetPage = pattern_nextpagelink.search(data_clean)

        #ZLI: Get a div with all followers
        while not nextfollowetPage is None:
            nextlink = nextfollowetPage.group(1)
            nextlink = "http://www.weibo.com" + nextlink
            #print nextlink
            nextdata = loginer.get_html(nextlink)
            nextdata_clean = nextdata.replace("\\\"","\"").replace("\\/","/")
            #ZLI
            #prerequis: next page will always contain a "pl.content.followTab.index"
            if pattern_html.search(nextdata_clean) is None:
                return
            nextfollowerlist = pattern_html.search(nextdata_clean).group(1)
            #print nextfollowerlist
            followerlist = followerlist + nextfollowerlist
            #print followerlist
            nextfollowetPage = pattern_nextpagelink.search(nextdata_clean)

        soup = BeautifulSoup(followerlist)
        flist = soup.find_all("img")

        tlock.acquire()                          # Lock; or wait if other thread is holding the lock
        print "\nThread %s Locked"%self.uid
        for li in flist:
            temp_count += 1
            try:
                #print "Perf01:%f"%time.time()
                userid = re.search(r"\d+",li['usercard']).group(0)
                #print "Perf02:%f"%time.time()
                #print "\nThread:"+ self.uid + "->" + userid
                #print li['alt']," ",li['src']," ",userid
                if userid not in dicID_Name:
                    dicID_Name[userid] = li['alt']
                if userid not in dicID_Img:
                    dicID_Img[userid] = li['src']
                if userid not in dicID_Count:
                    dicID_Count[userid] = 1
                else:
                    dicID_Count[userid] = dicID_Count[userid] + 1
                #print "Perf03:%f"%time.time()
                if self.actuallevel < expandLevel:
                    #print "level:%d"%self.actuallevel
                    while True:
                        if threading.activeCount()<Total_threadSize:
                            break
                        time.sleep(0.2)

                    new_thread = OpenLinkThread(userid,self.actuallevel + 1)
                    new_thread.start()
            except KeyError:
                pass
        tlock.release()
        print "\nThread %s Released"%self.uid

        print "\nThread ", self.uid , "is Over"

start = time.clock()
#proxy
proxy = urllib2.ProxyHandler({'http':'http://zli:Passw0rd@172.29.5.10:8080'})
auth = urllib2.HTTPBasicAuthHandler()
#cookie
cookiejar = cookielib.CookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
#opener
opener = urllib2.build_opener(proxy, auth, cookie_support, urllib2.HTTPHandler)
#opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
                   
loginer = WeiboLogin(opener, username, passwd)

print loginer.login()

#startid = "2859682070" #YannJiang
#startid = "3790747401" #Meizi
#startid = "1898526801" #PangZi
startid = "1224138841" #Jin


print "\nBefore:%d"%threading.activeCount()
new_thread = OpenLinkThread(startid,0)
new_thread.start()
print "\nAfter:%d"%threading.activeCount()

new_thread.join()

while True:
    time.sleep(1)
    print threading.activeCount()
    if threading.activeCount() == 1:
        break

print "\nAll:%d"%temp_count

#print dicID_Count['1898526801']
#print "TEST1"
#print sorted(dicID_Count.values())[-1:-11:-1]
#print "\nTest2"
#test = []
result = sorted(dicID_Count.items(), key=lambda d: d[1])

#print result[-1:-11:-1]
print "####################### TOP 10 ##########################"
for k in range(len(result)-1,len(result)-11,-1):
    strID = result[k][0]
    print strID + ":%d"%result[k][1]
    #print dicID_Name[strID]
#print dicID_Name
#print dicID_Img
#print dicID_Count


done = time.clock()

print "Time cost:"
print done - start