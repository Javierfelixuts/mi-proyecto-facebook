from datetime import datetime, timedelta, timezone
import json
import os
import requests

PAGE_ID = os.environ.get("PAGE_ID_3")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN_7")

JSON_FILE = "publicaciones.json"


def calis_programado():
  if not os.path.exists(JSON_FILE):
    print(f"El archivo {JSON_FILE} no existe.")
    return

  with open(JSON_FILE, "r", encoding="utf-8") as f:
    publicaciones = json.load(f)

  if not publicaciones:
    print("No hay publicaciones pendientes.")
    return

  # Tomamos el primer post
  post = publicaciones[0]

  texto_completo = (
      f"📌 {post.get('titulo', '')}\n\n"
      f"💬 {post.get('mensaje', '')}\n\n"
      f"🇬🇧 {post.get('descripcion_ingles', '')}\n\n"
      f"🇪🇸 {post.get('descripcion_espanol', '')}\n\n"
      f"{post.get('hashtags', '')}"
  )

  ruta_imagen = post.get("images", "")

  # Calculamos el tiempo actual UTC + 20 minutos
  tiempo_programado = datetime.now(timezone.utc) + timedelta(minutes=20)
  timestamp_unix = int(tiempo_programado.timestamp())

  # Parámetros necesarios para programar
  payload = {
      "access_token": ACCESS_TOKEN,
      "published": "false",  # Indica que NO se publique ya
      "scheduled_publish_time": timestamp_unix,  # Fecha y hora en formato UNIX
  }

  tiene_imagen = bool(ruta_imagen and os.path.exists(ruta_imagen))

  if tiene_imagen:
    print(f"Programando prueba con imagen: {ruta_imagen}")
    url = "https://graph.facebook.com/v19.0/me/photos"
    payload["caption"] = texto_completo

    with open(ruta_imagen, "rb") as img_file:
      files = {"source": img_file}
      response = requests.post(url, data=payload, files=files)
  else:
    print("Programando prueba solo texto...")
    url = "https://graph.facebook.com/v19.0/me/feed"
    payload["message"] = texto_completo
    response = requests.post(url, data=payload)

  if response.status_code == 200:
    print(
        "¡Cális programado con éxito! Tienes 20 minutos para revisarlo en"
        " Meta Business Suite."
    )
    print(f"Respuesta de FB: {response.json()}")
  else:
    print(f"Error al programar: {response.text}")


if __name__ == "__main__":
  calis_programado()