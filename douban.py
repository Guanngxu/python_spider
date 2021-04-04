import requests
from bs4 import BeautifulSoup

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
url = 'https://movie.douban.com/top250?start='

for i in range(0, 250, 25):
    req = requests.get(url + str(i), headers=headers)
    soup = BeautifulSoup(req.text)
    movies = soup.select('.grid_view li div.item')
    for movie in movies:
        # 电影在豆瓣的链接
        link = movie.select('a')[0]['href']
        # 电影对应的海边
        img = movie.select('img')[0]['src']
        # 电影的名称
        name = movie.select('.hd a span')[0].text
        # 导演、年份、地区、类型等信息，使用 strip() 把两头的空格去掉
        movie_info = movie.select('.bd p')[0].text.strip()
        # 导演信息和其它信息分在两行，所以可以使用换行符将导演信息切割出来
        temp_info = movie_info.split('\n')
        # 导演信息与主演信息中间是用 \xa0\xa0\xa0 进行隔开的，使用 \xa0\xa0\xa0 将导演信息隔开
        # 之后得到的信息是【导演: 奥利维·那卡什 Olivier Nakache】，再使用 : 切开取第二个，就是导演的姓名了
        director = temp_info[0].split('\xa0\xa0\xa0')[0].split(':')[1]
        # 第二行的 年份、地区、类型 信息之间是用 / 隔开的，用 / 隔开分别取就可以得到对应信息
        other = temp_info[1].split('/')
        year = other[0].strip()
        area = other[1].strip()
        tye = other[2].strip()
        # 评分信息
        score = movie.select('.rating_num')[0].text
        # 电影的描述信息，有的影片没有描述信息，所以会导致数组越界，因此使用 if 作判断，没有描述信息则自动补充一个 无
        desc = movie.select('.inq')[0].text if movie.select('.inq') else '无'
        info = {'名称': name, '链接': link, '图片': img, '评分': score, '导演': director, '年份': year, '地区': area, '类型': tye, '描述': desc}
        print(info)