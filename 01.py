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
    # 주간 데이터를 모두 수집해와야 하기 때문에 weekGb = 0
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


###------------내가 풀었던 과정---------------###


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