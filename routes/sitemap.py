
import requests

url = 'https://eyvaztis.ru/'
while True:
    response = requests.get(url)
    response_time = response.elapsed.total_seconds()

    print(f"Время ответа: {response_time} секунд")
