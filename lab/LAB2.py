import re
import numpy as np
# 三个概率
init_dic = dict()
emmission = dict()
transform = dict()
# 辅助计算的字典
cnt_head_ch = dict()
cnt_ch = dict()
cnt_dual_ch = dict()
bigram = dict()
length = 0


# lexicon.txt
print('training emmission')
f = open('lexicon.txt')
for line in f.readlines():
    line = re.sub(r'[0-9]','',line)
    line = line.strip().split()
    for i,ch in enumerate(line[0]):
        if ch not in emmission:
            emmission[ch] = dict()
            emmission[ch][line[1+i]] = 1
        else:
            if line[1+i] in emmission[ch]:
                emmission[ch][line[1+i]] += 1
            else:
                emmission[ch][line[1+i]] = 1
f.close()
# 发射概率
for key in emmission:
    s = sum(emmission[key].values())
    for key2 in emmission[key]:
        emmission[key][key2] = np.log(emmission[key][key2]/s)
print('emmission done')


# toutiao.txt
print('training init and transform')
f = open('toutiao_cat_data.txt',encoding='utf-8')
for line in f.readlines():
    line = line.strip().split("_!_")
    line = line[3:]
    for l in line:
        l = re.sub('[a-zA-Z0-9——|’!"#$%&\'()（）：「」*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', '', l)
        if not l:
            continue
        if l[0] in cnt_head_ch:
            cnt_head_ch[l[0]] += 1
        else:
            cnt_head_ch[l[0]] = 1
        pre = ''
        for i in l:
            if i in cnt_ch:
                cnt_ch[i] += 1
            else:
                cnt_ch[i] = 1
            if pre != '':
                if pre + i in cnt_dual_ch:
                    cnt_dual_ch[pre+i] += 1
                else:
                    cnt_dual_ch[pre+i] = 1
            pre = i
        length += 1
f.close()
# 初始概率
for key in cnt_head_ch:
    init_dic[key] = np.log(cnt_head_ch[key]/length)
# 转移概率
for i in cnt_dual_ch:
    transform[i] = np.log(cnt_dual_ch[i] / cnt_ch[i[0]])
print('all done')

# 拼音字典
pinyin_to_chinese = dict()
f = open('pinyin2hanzi.txt',encoding='utf-8')
for line in f.readlines():
    line = re.sub(r'[\ufeff]','',line)
    line = line.strip().split()
    pinyin_to_chinese[line[0]] = line[1]
f.close()


# 维特比算法
def viterbi(pinyin):
    delta = list()
    psi = list()
    flag = 0
    for i in pinyin:
        if i not in pinyin_to_chinese:
            flag = 1
    if flag == 1:
        print("please input a correct pinyin!")
        return
    # 初始化
    delta.append([init_dic.get(x, -50.0) + emmission.get(x, {}).get(pinyin[0], -50.0) for x in pinyin_to_chinese[pinyin[0]]])
    psi.append([0 for i in range(len(pinyin_to_chinese[pinyin[0]]))])
    # 归纳运算
    for i in range(1, len(pinyin)):
        delta.append([])
        psi.append([])
        for j in range(len(pinyin_to_chinese[pinyin[i]])):
            delta[i].append(-3000)
            psi[i].append(0)
            next = pinyin_to_chinese[pinyin[i]][j]
            for k in range(len(pinyin_to_chinese[pinyin[i - 1]])):
                pre = pinyin_to_chinese[pinyin[i - 1]][k]
                if delta[i][j] < delta[i-1][k] + transform.get(pre + next, -50.0):
                    delta[i][j] = delta[i-1][k] + transform.get(pre + next, -50.0)
                    psi[i][j] = k
            delta[i][j] = delta[i][j] + emmission.get(next, {}).get(pinyin[i], -50.0)
    i = max(delta[-1])
    index = delta[-1].index(i)
    ans = ''
    for j in range(len(psi) - 1, -1, -1):
        ans += pinyin_to_chinese[pinyin[j]][index]
        index = psi[j][index]
    return ans[::-1]


# 准确度测试
def accuracy():
    f = open("测试集.txt")
    flag = 1
    predict = list()
    label = list()
    for l in f.readlines():
        if flag == 1:
            l = l.lower()
            predict.append(viterbi(l.split()))
            flag = 0
        else:
            label.append(l)
            flag = 1
    error_word_cnt = 0
    word_cnt = 0
    error_sentence_cnt = 0
    word_acc_rate = list()
    for i in range(len(predict)):
        word_cnt += len(predict[i])
        label[i] = label[i].strip()
        if predict[i] != label[i]:
            error_sentence_cnt += 1
            print(predict[i],label[i])
        for j in range(len(predict[i])):
            if predict[i][j] != label[i][j]:
                error_word_cnt+=1
        word_acc_rate.append(1-(error_word_cnt/word_cnt))
    print("word accuracy: ", np.mean(word_acc_rate))
    print("sentence accuracy: ", 1-(error_sentence_cnt/len(predict)))


if __name__ == '__main__':
    accuracy()
    while True:
        print("please input a pinyin: ")
        pinyin = input().split()
        ans = viterbi(pinyin)
        if ans:
            print(ans)





