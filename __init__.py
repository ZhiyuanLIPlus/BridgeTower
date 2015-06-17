import re
import urllib
import urllib2
import cookielib

from bs4 import BeautifulSoup
from login import WeiboLogin

username = "username"
passwd = "psw"

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

startid = "1676582524"


#BlackBox begins
starturl = 'http://www.weibo.com/%s/follow?from=page_100505&wvr=6&mod=headfollow'%startid 

data  = loginer.get_html(starturl)

data_clean = data.replace("\\\"","\"").replace("\\/","/")

pattern_html = re.compile(r'followTab/index.*"html":"(.*?)\\r\\n"}')
pattern_nextpagelink = re.compile(r'class="page next S_txt1 S_line1" href="(.*?)">')

match1 = pattern_html.search(data_clean)
#TODO : condition for no match
#print match1.group(1)

#if match1 is None:

followerlist = match1.group(1)

nextfollowetPage = pattern_nextpagelink.search(data_clean)

#ZLI: Get a div with all followers
while not nextfollowetPage is None:
    nextlink = nextfollowetPage.group(1)
    nextlink = "http://www.weibo.com" + nextlink
    print nextlink
    nextdata = loginer.get_html(nextlink)
    nextdata_clean = nextdata.replace("\\\"","\"").replace("\\/","/")
    #ZLI 
    #prerequis: next page will always contain a "pl.content.followTab.index"
    #TODO: maybe need a condition
    nextfollowerlist = pattern_html.search(nextdata_clean).group(1)
    #print nextfollowerlist
    followerlist = followerlist + nextfollowerlist
    #print followerlist
    nextfollowetPage = pattern_nextpagelink.search(nextdata_clean)

soup = BeautifulSoup(followerlist)
flist = soup.find_all("img")
tem = 0
for li in flist:
    tem += 1
    try:
        print li['alt']," ",li['src']," ",li['usercard']
    except KeyError:
        pass
print "fin:%s"%tem

    
'''
testurl = "http://www.weibo.com/p/1035051282005885/follow?page=6#Pl_Official_HisRelation__60"

test  = loginer.get_html(testurl)
test_clean = test.replace("\\\"","\"").replace("\\/","/")

match1 = pattern_html.search(test_clean) 

soup = BeautifulSoup(match1.group(1))
#print(soup.prettify())
'''

'''
taglist = soup.find_all("img")

for li in taglist:
    #soup_followunit = BeautifulSoup(li)
    #img_tag = soup_followunit.find_all("img")
    #print type(li)
    print li['alt']," ",li['src']," ",li['usercard'] 
print "fin" 
'''

#next_page = soup.find_all("a","page next S_txt1 S_line1")


'''
pattern_html = re.compile(r'(  .*?)"})') 

data_focus = re.search('(?<=abc)def', data)
print data_focus.group(0)


data_clean = data.replace("\\\"","\"").replace("\\/","/")
#print data_clean

soup = BeautifulSoup(data_clean)
#print(soup.prettify())

taglist = soup.find_all('li')

for li in taglist:
    print "aa"

print "fin" 
'''

'''
conn = urllib2.urlopen('http://weibo.com/1610062637/follow?from=page_100505&wvr=6&mod=headfollow')
s1 = conn.read()

print s1
'''

'''

def login_hook(opener, **kw):
    username = "lzy00789@hotmail.com"
    passwd = "Fzyl890705"
    
    loginer = WeiboLogin(opener, username, passwd)
    return loginer.login()

url_patterns = UrlPatterns(
    Url(r'http://weibo.com/aj/mblog/mbloglist.*', 'micro_blog', MicroBlogParser),
    Url(r'http://weibo.com/aj/.+/big.*', 'forward_comment_like', ForwardCommentLikeParser),
    Url(r'http://weibo.com/\d+/info', 'user_info', UserInfoParser),
    Url(r'http://weibo.com/\d+/follow.*', 'follows', UserFriendParser),
    Url(r'http://weibo.com/\d+/fans.*', 'fans', UserFriendParser)
)

def get_job_desc():
    return JobDescription('sina weibo crawler', url_patterns, MechanizeOpener, user_config, 
                          starts, unit_cls=WeiboUserBundle, login_hook=login_hook)
    
if __name__ == "__main__":
    from cola.context import Context
    ctx = Context(local_mode=True)
    ctx.run_job(os.path.dirname(os.path.abspath(__file__)))
'''
