from datetime import datetime
import json
import os
import time
import requests

# Tomar credenciales de las variables de entorno de GitHub Actions (Secrets)
PAGE_ID = os.environ.get("PAGE_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")


def programar_publicacion(imagen_path, mensaje, timestamp):
    # Verificar si la imagen realmente existe en el proyecto
    tiene_imagen = imagen_path and os.path.exists(imagen_path)

    try:
        if tiene_imagen:
            # Publicar/Programar con foto
            url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
            with open(imagen_path, "rb") as image_file:
                files = {"source": image_file}
                data = {
                    "caption": mensaje,
                    "published": "false",  # Vital para que quede programada
                    "scheduled_publish_time": timestamp,
                    "access_token": ACCESS_TOKEN,
                }
                response = requests.post(url, data=data, files=files)
        else:
            # Si no hay imagen, programar solo el texto en el feed
            print(f"Aviso: La imagen '{imagen_path}' no existe. Programando solo texto...")
            url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
            data = {
                "message": mensaje,
                "published": "false",
                "scheduled_publish_time": timestamp,
                "access_token": ACCESS_TOKEN,
            }
            response = requests.post(url, data=data)

        resultado = response.json()

        if "id" in resultado:
            print(f"Éxito: Publicación programada correctamente (ID: {resultado['id']}).")
        else:
            print(f"Error al programar:", resultado)

    except Exception as e:
        print(f"Excepción al procesar la publicación: {e}")


# Cargar el archivo de configuración
if __name__ == "__main__":
    if not os.path.exists("publicaciones.json"):
        print("El archivo publicaciones.json no existe.")
        exit(1)

    with open("publicaciones.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    for post in posts:
        # Extraer datos soportando si 'imagen' o 'timestamp' faltan en algún objeto
        imagen = post.get("imagen", "")
        mensaje = post.get("mensaje", "")
        timestamp = post.get("timestamp")

        programar_publicacion(imagen, mensaje, timestamp)
        time.sleep(3)  # Pausa de 3 segundos para evitar bloqueos por saturación