import re
import urllib
import urllib2
import cookielib

from bs4 import BeautifulSoup
from login import WeiboLogin

username = "lzy00789@hotmail.com"
passwd = "Fzyl890705"

#proxy
proxy = urllib2.ProxyHandler({'http':'http://zli:P@ssw0rd@172.29.5.10:8080'})
auth = urllib2.HTTPBasicAuthHandler()
#cookie
cookiejar = cookielib.CookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
#opener
opener = urllib2.build_opener(proxy, auth, cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
                   
loginer = WeiboLogin(opener, username, passwd)

print loginer.login()

starturl = 'http://www.weibo.com/1191220232/follow?from=page_100505&wvr=6&mod=headfollow' #TODO

data  = loginer.get_html(starturl)

data_clean = data.replace("\\\"","\"").replace("\\/","/")

pattern_html = re.compile(r'followTab/index.*"html":"(.*?)\\r\\n"}')

match1 = pattern_html.search(data)  
#TODO : condition for no match #print match1.group(0)

soup = BeautifulSoup(match1.group(0))

taglist = soup.find_all()

for li in taglist:
    print "aa"

print "fin" 

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
