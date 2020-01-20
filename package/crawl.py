import requests
from bs4 import BeautifulSoup


class crawler():
    def __init__(self, acct, pwd):  # 模擬登入，取得 cookie
        loginURL = 'https://portal.ncu.edu.tw/login'
        checkURL = 'https://portal.ncu.edu.tw/j_spring_security_check'
        scoreURL = 'https://portal.ncu.edu.tw/system/show/162'
        studentRecordURL = 'https://cis.ncu.edu.tw/ScoreInquiries/student/student_record.php'
        headers = {
            'Host': 'portal.ncu.edu.tw',
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Origin": "https://portal.ncu.edu.tw",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Sec-Fetch-User": "?1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        postData = {
            "j_username": acct,
            "j_password": pwd
        }
        self.session = requests.session()
        self.session.get(loginURL, headers=headers)
        self.session.post(checkURL, data=postData)
        self.session.get(scoreURL)
        # cookies = self.session.cookies.get_dict()
        res = self.session.get(studentRecordURL)
        if res.status_code == requests.codes.ok:
            self.html = res.text
        else:
            print("REPONSE_CODE", res.status_code)

    def parseHTML(self):
        soup = BeautifulSoup(self.html, "html5lib")
        ret = []
        for i, tb in enumerate(soup.select('tbody')):
            dic = []
            for el in tb.select('.list1'):
                dic.append([e.text for e in el.find_all('td')])
            ret.append(dic)
        return ret
