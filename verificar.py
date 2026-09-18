import os
import requests

PAGE_ID = os.environ.get("PAGE_ID_3")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN_7")

# Consultar publicaciones programadas en la API
url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/scheduled_posts"
params = {
    "fields": "id,message,created_time,scheduled_publish_time,is_published",
    "access_token": ACCESS_TOKEN
}

response = requests.get(url, params=params)
datos = response.json()

print("--- PUBLICACIONES PROGRAMADAS EN FACEBOOK ---")
print(datos)