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