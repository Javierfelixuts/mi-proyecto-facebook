import os
import json
import requests

PAGE_ID = os.environ.get("PAGE_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN_4")

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

    post = publicaciones.pop(0)
    mensaje = post.get("mensaje", "")
    ruta_imagen = post.get("imagen", "")

    tiene_imagen = ruta_imagen and os.path.exists(ruta_imagen)

    if tiene_imagen:
        print(f"Publicando en Facebook con imagen: {ruta_imagen}")
        url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
        payload = {"caption": mensaje, "access_token": ACCESS_TOKEN}
        files = {"source": open(ruta_imagen, "rb")}
        response = requests.post(url, data=payload, files=files)
    else:
        print("Publicando en Facebook solo texto...")
        url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
        payload = {"message": mensaje, "access_token": ACCESS_TOKEN}
        response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("¡Publicado en el muro con éxito!")
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(publicaciones, f, ensure_ascii=False, indent=2)
    else:
        print(f"Error al publicar en Facebook: {response.text}")
        exit(1)

if __name__ == "__main__":
    publicar_siguiente()