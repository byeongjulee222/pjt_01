# 감독명을 활용하여 상세정보를 수집
# 필요 정보 : 영화인 코드, 영화인 명, 분야, 필모리스트
# 

import requests
from decouple import config
from pprint import pprint
import csv

Cd_list = []
with open('movie.csv', newline='', encoding='utf-8') as f:  # 
    reader = csv.DictReader(f)      
    for row in reader:
        Cd_list.append(row['directors'])

# pprint(Cd_list)

