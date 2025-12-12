import requests
url="https://dummyjson.com/carts"
response=requests.get(url)
print("status code:",response.status_code)
data=response.json()
print("response data:",data)
