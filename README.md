# pjt_01 README

## 00. 영화진흥위원회 오픈 API 활용 데이터 추출 (.csv파일 작성)

* 목표
  * 기초 Python에 대한 이해
  * Python을 통한 데이터 수집 및 파일 저장
  * Python 조건/반복문 및 다양한 자료구조 조작
  * API 활용을 통해 데이터를 수집하고 내가 원하는 형태로 가공한다.
  * 영화평점사이트(예- watcha)에 필요한 데이터를 프로그래밍을 통해 수집한다.



## 01. 주간/주말 박스오피스(최근 50주간 박스오피스 TOP10 데이터 수집)

- Check-Point
  - 키 값을 .env파일에서 불러와서 사용
  - targetDt = datetime() - timedelta(weeks=i) # from datetime import timedelta, datetime
  - 빈 딕셔너리 작성 후 조건을 만족하는 value를 추가하는 방법 사용
  - targetDt 50회 반복
  - 딕셔너리에 딕셔너리 값 추가하기
  - .csv 파일 작성('w')

```python
# 프로그래밍 과정
# 1. 영진위 사이트에서 발급받은 키 값을 .env파일에 작성한 후 불러와서 사용한다.
# 2. 처음 기준 날짜에서 1주씩 줄여가면서 50주 전까지 반복
# 3. 최근 50주간 데이터를 받아와 비교해야되기 때문에 targetDt 50번 반복 필요
# --> for문 없이 작성하고 적은 횟수로 for문 돌려본 뒤 최종적으로 50번 반복(실패 시 키 요청 횟수 오버 방지)
# 4. .csv 파일 작성(write)
# 코드를 작성하면서 잘 진행되고 있는지 중간중간 print해서 확인
# --> 딕셔너리 안에 key와 value값이 많을 경우 pprint로 출력하면 보기 편하다.

import requests
import csv
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint


# 최종 결과값을 입력할 빈 딕셔너리 생성.
result = {}
# 50주 전까지의 데이터를 수집해야 하기 때문에 range(50) 사용
for i in range(50):
    # .env에 작성한 'MOVIE_KEY'를 불러옴 (key를 config해오기 위해서는 대문자로 작성해야한다.)
    key = config('MOVIE_KEY')
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')      # 이렇게 변환해줘야 날짜를 인식할 수 있다.

    # url에 기본 base_url 뒤에 오는 규칙을 파악하여 key값과 targetDt값을 받아올 주소를 작성
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?&key={key}&targetDt={targetDt}&weekGb=0'
    # 읽어올 수 있는 자료 형태로 수정(.json())
    api_data = requests.get(url).json()
    # pprint(api_data)

    # 주간/주말 박스오피스 데이터 리스트로 가져오기.
    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
    # pprint(movies)

    # 필요한 key값 : movieCd, movieNm, audiAcc(누적 관객수)

    # 영화 정보가 담긴 딕셔너리에서 영화 대표 코드를 추출
    for movie in movies:
        code = movie.get('movieCd')
        # 값을 csv에 넣기 위해서는 딕셔너리 형식으로 만들어야 한다.// 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에
        # 기존에 이미 영화 코드가 들어가 있다면, 그게 가장 마지막 주 자료다. 즉 기존 영화 코드가 있다면 딕셔너리에 넣지 않는다.

        ###-----이 부분에서 막혀서 시간 오래 걸림-----###
        # 딕셔너리에 딕셔너리 값을 추가 ===> 중괄호를 양쪽에 열어두고 반복되는 인자.get('key') 입력
        if code not in result:          
            result[code] = {
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'),
                'audiAcc': movie.get('audiAcc')
            }
    # pprint(result)

    # .csv 파일 새로 작성
    # with open('.csv 파일명', '읽기/쓰기', 'encoding='utf-8', newline=''--> window에서 설정해줘야 하는 값) as f: // 그 외에 DictReader, DictWrter도 있다.
    with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
        # 목록 중 불러올 value에 해당하는 key값 나열
        fieldnames = ('movieCd', 'movieNm', 'audiAcc')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for value in result.values():
            # print(value)
            # 불러온 값을 열 단위로 작성
            writer.writerow(value)
    # 여기까지 1주를 성공한 다음에 50주의 for문을 돌려야 한다.


### 내가 풀었던 과정 ###


# 필요한 key값 : movieCd, movieNm, audiAcc(누적 관객수)
    # winner = []
    # for i in range(1,7):
    #     winner.append(lotto[f'drwtNo{i}'])
# final = []
# movies_list = []
# movies_dict = {}

# movies = movie.get('boxOfficeResult').get('weeklyBoxOfficeList')

# for i in range(len(movies)):
#     movies_dict['movieCd'] = movies[i].get('movieCd')
#     movies_dict['movieNm'] = movies[i].get('movieNm')
#     movies_dict['audiAcc'] = movies[i].get('audiAcc')


# for j in range(len(movies)):
#     movies_list.append(movies_dict)


    # movies_list.append(movies[i].get('movieCd'))
    # movies_list.append(movies[i].get('movieNm'))
    # movies_list.append(movies[i].get('audiAcc'))

    # for key, val in movie_dict.items():
    # for key, val in movies[]
# pprint(movies_dict)
    # for key in movies[0]:
    #     if key == 'movieCd':  # or key == 'movieNm' or key == 'audiAcc':
    #         print(key)            #  movies_dict.update({key: val})
    # movies_list.append(movies_dict)
        
# pprint(final)


# empty = []
# for i in range(10):
#     for key, val in movie_list[i]:
#         if key == 'movieCd' or key == 'movieNm' or key == 'audiAcc':
#             empty.append(val)

# print(empty)

#     empty.append(movie_list[i]['movieNm'])
#     empty.append(movie_list[i]['audiAcc'])

# with open('movies.csv', 'w', newline='', encoding='utf-8') as f:
#     fieldnames = ('movieCd', 'movieNm', 'audiAcc')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     writer.writeheader()

#     for movie in movie_list:
#         writer.writerow(empty)


# with open('avengers.csv', 'w', newline='', encoding='utf-8') as f:      # newline='', encoding='utf-8': 윈도우에 필요한 명령어
#     # 저장할 데이터들의 필드 이름을 미리 정한다.
#     fieldnames = ('name', 'gender', 'appearances', 'years since joining')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     # 필드 이름을 csv 파일 최상단에 작성한다.
#     writer.writeheader()

#     # 딕셔너리를 순회하며 key를 통해 한 줄씩(value를) 작성한다.
#     for avenger in avengers:        # 리스트 안의 딕셔너리들을 불러온다.
#         writer.writerow(avenger)     # writerow() : 열 작성 명령어
```





## 02. 영화 상세정보(수집한 영화 대표코드를 활용)

- Check-Point
  - 이전에 작성했던 .csv 파일을 활용('movieCd'가 같은지)
  - 딕셔너리 안에 리스트, 그 리스트 안에 딕셔너리에 있는 value값 가져오기
  - 빈 딕셔너리를 만났을 때 발생하는 Error 해결

```python
# 프로그래밍 과정
# 1. 이전에 작성했던 boxoffice.csv 파일에서 'movieCD'열 값을 읽어온다.('r' : read, 생략가능)
# 2. 영화 대표코드(movieCd)를 참조할 것이기 때문에 movieCd 값들을 리스트로 묶어둔다. --> 리스트 안에 존재하는지 판단하는 조건문 작성
# 3. 조건을 만족하는 값을 넣는 빈 딕셔너리 생성
# 4. 마지막으로 .csv 파일 작성


import requests
from decouple import config
from pprint import pprint
import csv


# 필요 정보 : movieCd, movieNm, movieNmEn, movieNmOg, watchGradeNm, openDt, showTm, genreNm, directors


with open('boxoffice.csv', newline='', encoding='utf-8') as f:  # 
    reader = csv.DictReader(f)      # 필드 네임을 작성하는 것이 아니기 때문에 f까지만 작성
    Cd_list = []                    # (읽어오기 전에 값을 추가할 빈 리스트를 먼저 만든다.)
    # 한 줄씩 읽는다.
    for row in reader:
        Cd_list.append(row['movieCd'])

# 아래에 조건을 만들고 그 조건을 만족하는 값을 넣어주기 위해 빈 딕셔너리를 작성
result = {}
for Cd in Cd_list:
    movieCd = Cd
    key = config('MOVIE_KEY')
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={movieCd}'

    api_data = requests.get(url).json()
    movie_data = api_data.get('movieInfoResult').get('movieInfo')

    # pprint(movie_data)
    for data in movie_data:
        code = movie_data.get('movieCd')
        result[code] = {
            'movieCd': movie_data.get('movieCd'),
            'movieNm': movie_data.get('movieNm'),
            'movieNmEn': movie_data.get('movieNmEn'),
            'movieNmOg': movie_data.get('movieNmOg'),
            # 여기서 딕셔너리 안에 리스트 // 그 리스트 안에 딕셔너리의 key값을 불러오는 것이 어려웠다.
            # 리스트를 살펴보고 규칙을 파악하여 인덱스 0번의 값을 불러와서 사용
            # for문을 돌려봤을 때 List out of range Error가 발생
            # audits 항목 중 빈 딕셔너리가 있어 오류가 발생한 것을 발견하여
            # if, else문을 사용하여 빈 딕셔너리를 만났을 때 'None'값을 반환하는 방법을 사용
            'watchGradeNm': movie_data.get('audits')[0].get('watchGradeNm') if movie_data.get('audits') else None,
            'openDt': movie_data.get('openDt'),
            'showTm': movie_data.get('showTm'),
            'genreNm': movie_data.get('genres')[0].get('genreNm'),
            'directors': movie_data.get('directors')[0].get('peopleNmEn') if movie_data.get('directors') else None
            }

    # pprint(result)

# .csv 파일을 새로 작성('w')
# 가져와야하는 value값에 해당하는 key 목록을 나열
with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'directors')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        # print(value)
        # 값들을 열 단위로 구분하여 작성
        writer.writerow(value)

# 이전에 코딩했던 01.py 파일을 참고하면 쉽게 풀어나갈 수 있을 것이라 생각했지만
# 예상치 못한 문제들(딕셔너리 안에 리스트, 그 안에 딕셔너리 & 빈 딕셔너리를 만났을 때 for문이 멈춰버리는 현상)
# 이러한 문제들로 인해 코드 작성에 어려움이 있었다.
```



## 03. 영화인 상세정보(감독정보를 활용하여)

- Check-Point
  - movie.csv 파일 내의 감독이름 활용
  - 빈 리스트에 감독명 추가
  - 빈 딕셔너리에 만족하는 데이터 저장
    - 딕셔너리 키값('repRoleNm')에 대응하는 value값('감독')
  - director.csv 파일에 작성('w')

```python
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
```

