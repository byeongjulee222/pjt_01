import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint
import csv


# 필요 정보 : movieCd, movieNm, movieNmEn, movieNmOg, watchGradeNm, openDt, showTm, genreNm, directors

with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)      # 필드 네임을 작성하는 것이 아니기 때문에 f까지만 작성
    Cd_list = []
    # 한 줄씩 읽는다.
    for row in reader:
        Cd_list.append(row['movieCd'])

result = {}
for i in Cd_list:
    movieCd = i
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
            'watchGradeNm': movie_data.get('audits')[0].get('watchGradeNm') if movie_data.get('audits') else None,
            'openDt': movie_data.get('openDt'),
            'showTm': movie_data.get('showTm'),
            'genreNm': movie_data.get('genres')[0].get('genreNm'),
            'directors': movie_data.get('directors')[0].get('peopleNmEn') if movie_data.get('directors') else None
            }

    # pprint(result)

with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNmEn')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        # print(value)
        writer.writerow(value)
