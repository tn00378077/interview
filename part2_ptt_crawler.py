import requests
import time
import json
from bs4 import BeautifulSoup
PTT_URL = 'https://www.ptt.cc'


# let python http have the cookies and get into the ptt page
def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


# parse the ptt gossiping
def get_articles(dom, date):
    soup = BeautifulSoup(dom)

    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    # 儲存取得的文章資料
    articles = []
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').text.strip() == date:
            push_count = 0
            push_str = d.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            if d.find('a'):
                href = d.find('a')['href']
                title = d.find('a').text
                date = d.find('div', 'date').text
                if d.find('div', 'author'):
                    author = d.find('div', 'author').text
                else:
                    author = ''
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count,
                    'author': author,
                    'date': date,
                })
    return articles, prev_url


if __name__ == '__main__':
    current_page = get_web_page(PTT_URL + '/bbs/Gossiping/index.html')
    if current_page:
        articles = []  # 全部的今日文章
        today = time.strftime("%m/%d").lstrip('0')
        current_articles, prev_url = get_articles(current_page, today)
        while current_articles:
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, today)

        # 儲存或處理文章資訊
        print('今天有', len(articles), '篇文章')
        threshold = 50
        print('熱門文章(> {0} 推):'.format(threshold))
        for a in articles:
            if int(a['push_count']) > threshold:
                print(a)
        with open('gossiping.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, sort_keys=True, ensure_ascii=False)
