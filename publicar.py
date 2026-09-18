import json
import os
import time
import requests

PAGE_ID = os.environ.get("PAGE_ID_3")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN_7")

JSON_FILE = "publicaciones.json"

# Minutos a futuro para la publicación (Facebook requiere entre 10 minutos y 75 días)
MINUTOS_A_FUTURO = 20


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

    # Extraer variables del JSON
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

    # Calcular Unix Timestamp para 20 minutos en el futuro
    tiempo_programado = int(time.time()) + (MINUTOS_A_FUTURO * 60)

    tiene_imagen = bool(ruta_imagen and os.path.exists(ruta_imagen))

    if tiene_imagen:
        print(f"Programando publicación con imagen para dentro de {MINUTOS_A_FUTURO} minutos...")
        url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
        payload = {
            "caption": texto_completo,
            "access_token": ACCESS_TOKEN,
            "published": "false",
            "scheduled_publish_time": tiempo_programado,
        }

        with open(ruta_imagen, "rb") as img_file:
            files = {"source": img_file}
            response = requests.post(url, data=payload, files=files)
    else:
        print(f"Programando publicación de solo texto para dentro de {MINUTOS_A_FUTURO} minutos...")
        url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
        payload = {
            "message": texto_completo,
            "access_token": ACCESS_TOKEN,
            "published": "false",
            "scheduled_publish_time": tiempo_programado,
        }
        response = requests.post(url, data=payload)

    if response.status_code == 200:
        print(f"¡Publicación programada con éxito en Facebook para dentro de {MINUTOS_A_FUTURO} minutos!")
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(publicaciones, f, ensure_ascii=False, indent=2)
    else:
        print(f"Error al programar en Facebook: {response.text}")
        exit(1)


if __name__ == "__main__":
    publicar_siguiente()