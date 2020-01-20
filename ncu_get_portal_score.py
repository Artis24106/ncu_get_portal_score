from package import crawl, emailSender
import json
import pathlib

path = pathlib.Path(__file__).parent.absolute()
with open(f"{path}/config.json") as configF:
    config = json.load(configF)

c = crawl.crawler(config["portal"]["acct"], config["portal"]["pwd"])
score = c.parseHTML()

try:
    with open(f"{path}/score.json", "r+") as s:
        oldScore = json.loads(s.read())
        msgTitle = ["成績", "學期平均", "累計平均"]
        i = 0
        msg = ''
        for now, pre in zip(score, oldScore):
            temp = ''
            for j in range(len(now)):
                if j >= len(pre) or (now[j] != pre[j]):
                    if temp == '':
                        temp = f"{msgTitle[i]}\n"
                    if i == 0:
                        temp += f"學期：{now[j][0]}, 科目：{now[j][2]}, 成績：{now[j][4]}\n"
                    elif i == 1:
                        temp += f"學期：{now[j][0]}, 學期平均：{now[j][1]}, 班排：{now[j][2]}, 系排：{now[j][3]}\n"
                    elif i == 2:
                        temp += f"學期：{now[j][0]}, 累積平均：{now[j][1]}, 班排：{now[j][2]}, 系排：{now[j][3]}\n"
            if temp != '':
                msg += f"{temp}\n"
            i += 1

        # print(msg)

        if msg != '':
            sender = emailSender.sender("Portal 成績更新", config["mail"]["from"], config["mail"]["from_pwd"], config["mail"]["to"])
            sender.send(msg)
except FileNotFoundError:  # First time -> create score.json
    pass

with open(f"{path}/score.json", "w") as s:
    json.dump(score, s, indent=2)
