import re
f = open("BaiduDictionary.txt", encoding="UTF-8")
lines = f.readlines()
word = list()
word.append("构")  # 数据处理时第一行的构会被删掉
max_len = 0
for line in lines:  # 数据处理
    if line[2:-1]:
        word.append(line[2:-1])
    max_len = max(len(line[2:-1]), max_len)  # 删掉前两个字符和最后的换行符

while True:
    print("请输入一个句子以分词：")
    a = input()
    a = re.sub(r'[（）：，、—●。”“《》？！]', "", a)  # 删掉标点符号
    flag1 = 0  # 判断是否有错误
    flag2 = 0
    res1 = []  # 保存分词结果
    res2 = []
    err1 = []  # 保存错误数据
    err2 = []

    # 前向
    left = 0
    while left <= len(a) - 1:
        if len(a) == 1 and a not in word:
            err1.append(a)
            flag1 = 1
            break
        if left + max_len - 1 > len(a) - 1:
            right = len(a) - 1
        else:
            right = left + max_len - 1
        for i in range(right, left - 1, -1):
            if a[left: i + 1] not in word and left == i:
                err1.append(a[left: i + 1])
                flag1 = 1
                left += 1
                break
            if a[left: i + 1] in word:
                res1.append(a[left:i + 1])
                left += len(a[left:i + 1])
                break

    # 后向
    right = len(a)
    while right > 0:
        if len(a) == 1 and a not in word:
            err2.append(a)
            flag2 = 1
            break
        if right - max_len < 0:
            left = 0
        else:
            left = right - max_len
        for i in range(left, right + 1):
            if a[i:right] not in word and i == right - 1:
                err2.append(a[i:right])
                flag2 = 1
                right -= 1
                break
            if a[i:right] in word:
                res2.append(a[i:right])
                right -= len(a[i:right])
    # 输出
    print("前向： ", end='')
    if flag1 == 0:
        print(res1)
    else:
        print("分词失败！下列词语未录入词库！", end='')
        print(err1)
    print("后向： ", end='')
    if flag2 == 0:
        print(res2[::-1])
    else:
        print("分词失败！下列词语未录入词库！", end='')
        print(err2[::-1])
