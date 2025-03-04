import requests

url = "http://127.0.0.1:8000/agencies"
headers = {"api-key": "1ba15bf3eb78b3f344ee9894dbf27b98f08e83bc36d83db889d2176611609a16"}

response = requests.get(url, headers=headers)

print("🔹 Response Status:", response.status_code)  
print("🔹 Response Data:", response.json())
