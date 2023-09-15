"""
File: webcrawler.py
Name: Alex
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10900879
Female Number: 7946050
---------------------------
2000s
Male Number: 12977993
Female Number: 9209211
---------------------------
1990s
Male Number: 14146310
Female Number: 10644506
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        
        response = requests.get(url)    # request 是讓 pycharm 連上網路
        html = response.text            # 取出 html 字串
        soup = BeautifulSoup(html)      # 讓上一行的 html 可以用 soup class 的絕招

        # ----- Write your code below this line ----- #

        items = soup.find_all('table', {'class': 't-stripe'})
        # print(items)

        for item in items:
            targets = item.text.split()[13:1013]  # index 13 是第一次出現的 rank,index 1013(實際上是到1012)是最後一個女生number
            # print(targets)
            count = 0
            male_number = 0
            female_number = 0

            for target in targets:
                target = target.replace(',', '')     # replace: 去除掉number中的,符號 (ex:183,172-->183172)
                if count %5 == 2:                    # 餘數為2是男生數目
                    male_number += int(target)
                if count %5 == 4:                    # 餘數為4是女生數目
                    female_number += int(target)
                count += 1
            print(f'Male Number: {male_number}')
            print(f'Female Number: {female_number}')


if __name__ == '__main__':
    main()
