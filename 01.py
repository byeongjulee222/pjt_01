import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint
import csv

result = {}

for i in range(50):
    key = config('MOVIE_KEY')
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')      # 이렇게 변환해줘야 날짜를 인식할 수 있다.


    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?&key={key}&targetDt={targetDt}&weekGb=0'
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
        if code not in result:          
            result[code] = {
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'),
                'audiAcc': movie.get('audiAcc')
            }
    # pprint(result)

    with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ('movieCd', 'movieNm', 'audiAcc')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for value in result.values():
            # print(value)
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