import json
import os
import requests

PAGE_ID = os.environ.get("PAGE_ID_3")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN_7")

JSON_FILE = "publicaciones.json"


def publicar_siguiente():
  if not os.path.exists(JSON_FILE):
    print(f"El archivo {JSON_FILE} no existe.")
    return

  with open(JSON_FILE, "r", encoding="utf-8") as f:
    publicaciones = json.load(f)

  if not publicaciones:
    print("No hay publicaciones pendientes en la cola.")
    return

  # Extraer el primer post de la cola
  post = publicaciones.pop(0)

  # Construir el texto final concatenando los campos
  titulo = post.get("titulo", "")
  mensaje = post.get("mensaje", "")
  desc_en = post.get("descripcion_ingles", "")
  desc_es = post.get("descripcion_espanol", "")
  hashtags = post.get("hashtags", "")
  ruta_imagen = post.get("images", "")

  texto_completo = (
      f"📌 {titulo}\n\n"
      f"💬 {mensaje}\n\n"
      f"🇬🇧 {desc_en}\n\n"
      f"🇪🇸 {desc_es}\n\n"
      f"{hashtags}"
  )

  tiene_imagen = bool(ruta_imagen and os.path.exists(ruta_imagen))

  if tiene_imagen:
    print(f"Publicando en Facebook con imagen: {ruta_imagen}")
    url = "https://graph.facebook.com/v19.0/me/photos"
    payload = {"caption": texto_completo, "access_token": ACCESS_TOKEN}

    with open(ruta_imagen, "rb") as img_file:
      files = {"source": img_file}
      response = requests.post(url, data=payload, files=files)
  else:
    print("Publicando en Facebook solo texto...")
    url = "https://graph.facebook.com/v19.0/me/feed"
    payload = {"message": texto_completo, "access_token": ACCESS_TOKEN}
    response = requests.post(url, data=payload)

  if response.status_code == 200:
    print("¡Publicado en el muro con éxito!")
    # Guardar el JSON actualizado sin la publicación procesada
    with open(JSON_FILE, "w", encoding="utf-8") as f:
      json.dump(publicaciones, f, ensure_ascii=False, indent=2)
  else:
    print(f"Error al publicar en Facebook: {response.text}")
    exit(1)


if __name__ == "__main__":
  publicar_siguiente()