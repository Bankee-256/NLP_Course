import re
import jieba
cnt = dict()


def init():
    total_word = 0
    f = open("199801.txt", encoding="UTF-8")
    print("Generating... Please wait a minute")
    lines = f.readlines()
    for line in lines:
        line = line[21:]  # 删除前面的一串
        line = re.sub(r'/', "", line)  # 删除斜杠
        line = re.sub(r'\[]', "", line)
        line = re.sub(r'[a-zA-Z]', "", line)  # 删除字母
        line = re.sub(r'[（）：，、—●。”“《》？！]', "", line)  # 删除符号
        line = line.split(" ")
        line = line[1:-1]
        for word in reversed(line):
            if word == '':
                line.remove('')
        if line:
            line.append('EOS')  # 加入句首句尾标识符
            line.insert(0, 'BOS')
            pre = ''  # 用于二元模型的建立
            for word in line:
                if word in cnt.keys():
                    cnt[word] += 1
                    if pre != '':
                        if pre + word in cnt.keys():
                            cnt[pre + word] += 1
                        else:
                            cnt[pre + word] = 1
                    pre = word
                else:
                    total_word += 1  # 每发现一个新词，加一
                    cnt[word] = 1
                    if pre != '':
                        if pre + word in cnt.keys():
                            cnt[pre + word] += 1
                        else:
                            cnt[pre + word] = 1
                    pre = word
            # print(line)
    print("Model Successfully Generated")
    return total_word


def calculate(str1, word_cnt):
    seg_list = list(jieba.cut(str1))
    seg_list.insert(0, 'BOS')
    seg_list.append('EOS')
    ans = 1
    pre = ''
    for word in seg_list:
        if pre != '':
            # 计算分子
            if pre + word in cnt.keys():
                up = cnt[pre + word] + 1  #加法平滑
            else:
                up = 1
            # 计算分母
            if pre in cnt.keys():
                down = cnt[pre] + word_cnt  #加法平滑
            else:
                down = word_cnt
            ans *= up / down
        pre = word
    print(ans)


# 统计词的个数（不包含重复词），并且初始化
word_cnt = init()
while True:
    print("请输入一句中文以预测概率：")
    str1 = input()
    calculate(str1, word_cnt)
