import requests
import json

API_KEY = '1148b7211ad9ac4b35f86ab6667c8d34'

# popular 높은순으로 id추출 (한 페이지당 20개)
popular_ids = []
for page in range(1, 6):
    url = 'https://api.themoviedb.org/3/movie/popular?api_key={}&page={}&language=ko-kr'.format(API_KEY, page)
    res = requests.get(url)
    data = json.loads(res.text)

    for i in range(20):
        popular_ids.append(data['results'][i]['id'])


# data 추출
movie_list = []
for num in popular_ids:
    movie_data = dict()

    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=ko-kr'.format(num, API_KEY)
    url += '&append_to_response=videos'
    res = requests.get(url)

    # 존재하지 않는 URL 스킵
    if res.status_code != 200:
        continue

    data = json.loads(res.text)

    # 빈값이 있는 경우 스킵
    if len(data['overview']) > 10 and len(data['poster_path']) > 10\
         and data['runtime'] and data['videos']['results']:
        # print(num)

        movie_data['id'] = data['id']
        movie_data['title'] = data['title']
        movie_data['original_title'] = data['original_title']
        movie_data['original_language'] = data['original_language']
        movie_data['overview'] = data['overview']
        movie_data['release_date'] = data['release_date']
        movie_data['runtime'] = data['runtime']
        movie_data['poster_path'] = data['poster_path']
        movie_data['popularity'] = data['popularity']
        movie_data['genres'] = data['genres']
        movie_data['rank'] = 0

        if data['videos']['results'][0]['site'] == 'YouTube':
            video_url = 'https://www.youtube.com/watch?v='
        else:
            video_url = 'https://vimeo.com/'
        video_key = data['videos']['results'][0]['key']
        movie_data['video_url'] = video_url + video_key

        movie_list.append(movie_data)

# print(movie_list[0])
print('추출 데이터 수:', len(movie_list))
with open('movie_data.json','w',encoding="utf-8") as make_file:
    json.dump(movie_list, make_file, ensure_ascii=False, indent='\t')


## 디버깅용 코드
# num = 885110
# url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=ko-kr'.format(num, API_KEY)
# url += '&append_to_response=videos'
# res = requests.get(url)
# data= json.loads(res.text)
# print(data['videos'])