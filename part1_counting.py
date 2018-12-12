import operator

urls = [
    "http://www.google.com/a.txt",
    "http://www.google.com.tw/a.txt",
    "http://www.google.com/download/c.jpg",
    "http://www.google.co.jp/a.txt",
    "http://www.google.com/b.txt",
    "https://facebook.com/movie/b.txt",
    "http://yahoo.com/123/000/c.jpg",
    "http://gliacloud.com/haha.png",
]

scoreTable = {}
for urlTmp in urls:
    filename = urlTmp.rsplit("/", 1)[1]
    if filename in scoreTable:
        scoreTable[filename] += 1
    else:
        scoreTable[filename] = 1
        sorted_by_value = sorted(scoreTable.items(), key=operator.itemgetter(1), reverse=True)
del sorted_by_value[3:]
print(sorted_by_value)
