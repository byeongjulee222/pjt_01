# sample.py

avengers = [
    {
        "name": "tony stark",
        "gender": "male",
        "appearances": 3068,
        "years since joining": 52
    },
    {
        "name": "robert bruce banner",
        "gender": "male",
        "appearances": 2089,
        "years since joining": 52
    },
    {
        "name": "thor odinson",
        "gender": "male",
        "appearances": 2402,
        "years since joining": 52
    },
    {
        "name": "steven rogers",
        "gender": "male",
        "appearances": 3458,
        "years since joining": 51
    }
]

# 1. csv.DictWriter() 메서드 사용
import csv
# with open('avengers.csv', 'w', newline='', encoding='utf-8') as f:      # newline='', encoding='utf-8': 윈도우에 필요한 명령어
#     # 저장할 데이터들의 필드 이름을 미리 정한다.
#     fieldnames = ('name', 'gender', 'appearances', 'years since joining')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     # 필드 이름을 csv 파일 최상단에 작성한다.
#     writer.writeheader()

#     # 딕셔너리를 순회하며 key를 통해 한 줄씩(value를) 작성한다.
#     for avenger in avengers:        # 리스트 안의 딕셔너리들을 불러온다.
#         writer.writerow(avenger)     # writerow() : 열 작성 명령어

# 2. csv.DictReader() 메서드 사용
with open('avengers.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)      # 필드 네임을 작성하는 것이 아니기 때문에 f까지만 작성

    # 한 줄씩 읽는다.
    for row in reader:
        # print(row)
    # 좀 더 정확하게 읽고 싶으면
        print(row['name'])
        print(row['gender'])
        print(row['appearances'])
        print(row['years since joining'])