import requests
import time
import re
from lxml import etree
# def main_handler(event,context):
#     print('mt')
username=''
password=''
print("------开始执行mt论坛签到------")
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
session = requests.session()
headers = {'User-Agent': UserAgent,
           'referer':'https://bbs.binmt.cc/',
           }
url='https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
response = session.get(headers=headers, url=url).text
print(response)
response= re.sub(r'^<\?xml.*?\?>', '', response)
html=etree.HTML(response)
print(html)
loginhash=html.xpath('//form[@name="login"]/@id')[0].replace('loginform_','')
formhash=html.xpath('//input[@name="formhash"]/@value')[0]
cookitime=html.xpath('//input[@name="cookietime"]/@value')[0]

# loginhash = re.findall('loginhash=(.*?)">', response, re.S)[0]
# formhash = re.findall('formhash" value="(.*?)".*? />', response, re.S)[0]
# cookietime= re.findall('cookietime" value="(.*?)" .*?/>', response, re.S)[0]
print(loginhash)
print(formhash)
print(cookietime)
url='https://bbs.binmt.cc/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash='+loginhash+'&inajax=1'
data={
    "formhash": formhash,
    "referer": "https://bbs.binmt.cc/",
    "loginfield": "username",
    "username": username,
    "password": password,
    "questionid": "0",
    "answer": "",
    "cookietime": cookietime,
}
response=session.post(url=url,data=data,headers=headers).text
response= re.sub(r'^<\?xml.*?\?>', '', response)
# print(response)
def qiandao():
    getHashurl = 'https://bbs.binmt.cc/k_misign-sign.html'
    page_text = session.get(headers=headers, url=getHashurl).text
    # print(page_text)
    html= etree.HTML(page_text)
    formhash=html.xpath('//input[@name="formhash"]/@value')[0]
    # form = re.findall('formhash" value="(.*?)".*? />', page_text, re.S)[0]
    # 模拟签到
    sign_url = 'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&formhash='+formhash+'&format=empty&inajax=1&ajaxtarget='
    page_text2 = session.get(headers=headers, url=sign_url).text
    # print('11111111111111111111')
    # print(page_text2)
    # 验证是否签到成功
    check = re.findall('<root><(.*?)</root>', page_text2, re.S)
    if (len(check) != 0):
        print(f'签到详情：{check}')
        if ("今日已签" in str(check)):
            jg = "今天已经签到过了~"
            print('今天已经签到过了~')
        elif ("已签到" in str(check)):
            jg = "今天已经签到过了~"
            print('今天已经签到过了~')
        else:
            jg = "签到成功~"
            print('签到成功')
        response = session.get(headers=headers, url=getHashurl).text
        html = etree.HTML(response)
        jfjl=html.xpath('//input[@id="lxreward"]/@value')[0]
        lxqd=html.xpath('//input[@id="lxdays"]/@value')[0]
        qddj=html.xpath('//input[@id="lxlevel"]/@value')[0]
        mz=html.xpath('//a[@class="kmuser"]/span/text()')[0]
        qdpm=html.xpath('//input[@id="qiandaobtnnum"]/@value')[0]
        zts=html.xpath('//input[@id="lxtdays"]/@value')[0]
        jib = re.findall('积分奖励</h4>.*?></span>', response, re.S)
        lxb = re.findall('<h4>连续签到.*?></span>', response, re.S)
        djb = re.findall('签到等级</h4>.*?></span>', response, re.S)
        ztsb = re.findall('签到等级</h4>.*?></span>', response, re.S)

        try:
            # print(f"昵称：{name}\n签到排名：{pm}\n连续签到：{lx}天\n签到等级：LV.{dj}\n获得金币：{jb}\n总天数：{zts}天")
            message = '''⏰当前时间：{}
                        MT论坛签到
                    ####################
                    账号昵称：{}
                    签到排名：{}
                    连续签到：{}天
                    签到等级：LV.{}
                    获得金币：{}
                    总天数：{}天
                    签到结果：签到成功
                    ####################
                    祝您过上美好的一天！'''.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800)),
                mz, qdpm, lxqd, qddj, jfjl, zts)
            print(message)
        except:
            print("获取信息失败")
    else:
        print('签到失败')

def count():
    url='https://bbs.binmt.cc/home.php?mod=spacecp&ac=credit'
    response=session.get(headers=headers,url=url).text
    html=etree.HTML(response)
    jb_count=html.xpath('//li[@class="xi1 cl"]/em/following-sibling::text()')[0].strip()
    print(f'总金币：{jb_count}')
    jf_count=html.xpath('//li[@class="cl"]/em/following-sibling::text()')[0]
    print(f'总积分：{jf_count}')

try:
    p = re.compile(r'errorhandle_login\(\'(.*?)\'')
    result = p.findall(response)[0]
    print(result)
except:
    try:
        p = re.compile(r'succeedhandle_login\(.*?, \'(.*?)\',')
        result = p.findall(response)[0]
        print(result)
        if '登录成功' in result:
            qiandao()
            count()
    except:
        print('mt登录失败')

