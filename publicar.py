from datetime import datetime
import json
import os
import time
import requests

# Tomar credenciales de las variables de entorno de GitHub Actions
PAGE_ID = os.environ.get("61588186526840")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")


def programar_publicacion(imagen_path, mensaje, timestamp):
  url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"

  try:
    with open(imagen_path, "rb") as image_file:
      files = {"source": image_file}
      data = {
          "message": mensaje,
          "published": "false",  # Vital para que quede programada
          "scheduled_publish_time": timestamp,
          "access_token": ACCESS_TOKEN,
      }

      response = requests.post(url, data=data, files=files)
      resultado = response.json()

      if "id" in resultado:
        print(f"Éxito: Imagen {imagen_path} programada correctamente.")
      else:
        print(f"Error con {imagen_path}:", resultado)

  except Exception as e:
    print(f"Excepción al procesar {imagen_path}: {e}")


# Cargar el archivo de configuración
if __name__ == "__main__":
  with open("publicaciones.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

  for post in posts:
    programar_publicacion(post["imagen"], post["mensaje"], post["timestamp"])
    time.sleep(3)  # Pausa de 3 segundos para evitar bloqueos por saturación