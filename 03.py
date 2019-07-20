# 프로그래밍 과정
# 감독명을 활용하여 상세정보를 수집
# 필요 정보 : 영화인 코드, 영화인 명, 분야, 필모리스트
# 1. mmovie.csv에서 감독이름 가져오기('r')
# 2. 감독이름과 일치하는 목록 추출
# 3. director.csv 파일 작성('w')

import requests
from decouple import config
from pprint import pprint
import csv

# 이전에 작성해 둔 movie.csv파일에서 'directors'에 대한 정보를 담을 빈 리스트 작성
people_list = []
with open('movie.csv', newline='', encoding='utf-8') as f:  #  읽어들일때는 'r'을 생략할 수 있다.
    reader = csv.DictReader(f)      
    # 읽어온 데이터 내에서 반복문을 실행
    for row in reader:
        # 이름 사이에 공백이 있는 경우 붙여진 모양으로 주소에 입력되는 것에 따라 대입할 값 조작
        people_list.append(row['directors'].replace(" ", ""))

# pprint(people_list)
key = config('MOVIE_KEY')
result_2 = {}
for name in people_list:
    # API상 max값이 100이기 때문에 &itemPerPage=100 추가
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={key}&peopleNm={name}&itemPerPage=100'
    result_2[name] = requests.get(url).json()

# pprint(result_2)

# 최종 결과물을 담을 빈 딕셔너리 작성
movie_list = {}
# 딕셔너리 peopleList 안에 있는 각각의 키 값에 맞는 value를 뽑아내기 위해 1씩 카운트하는 방법을 활용
count = 0
for tag in people_list:
    people = result_2[tag]['peopleListResult']['peopleList']
    for i in range(len(people)):
        # 뽑아낸 자료와 뽑을 자료명('감독')이 일치하는 것만 딕셔너리에 추가
        # 이 부분을 찾아내는데에 시간이 오래걸림
        if people[i]['repRoleNm'] == '감독':
            #### 이 부분에서 각 항목들을 추가하는 방법을 생각하는데에 어려움이 있었음 ####
            movie_list[count] = {
                'peopleCd': people[i]['peopleCd'],
                'peopleNm': people[i]['peopleNm'],
                'repRoleNm': people[i]['repRoleNm'],
                'filmoNames': people[i]['filmoNames']
            }
            count += 1

# pprint(movie_list)

    with open('director.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ('peopleCd', 'peopleNm', 'repRoleNm', 'filmoNames')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for value in movie_list.values():
            # print(value)
            # 값들을 열 단위로 구분하여 작성
            writer.writerow(value)