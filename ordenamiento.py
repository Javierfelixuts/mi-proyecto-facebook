import os

def continuar_secuencia(carpeta_origen, carpeta_destino, inicio=81, prefijo="leccion"):
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.webp')
    
    # Obtener y ordenar las imágenes de la nueva carpeta
    archivos = [f for f in os.listdir(carpeta_origen) if f.lower().endswith(extensiones_validas)]
    archivos.sort()
    
    if not archivos:
        print(f"No se encontraron imágenes en '{carpeta_origen}'.")
        return

    # Crear la carpeta de destino si no existe
    os.makedirs(carpeta_destino, exist_ok=True)

    contador = inicio
    print(f"Moviendo y renombrando {len(archivos)} imágenes a '{carpeta_destino}' desde el #{inicio}...")

    for archivo in archivos:
        extension = os.path.splitext(archivo)[1].lower()
        nuevo_nombre = f"{prefijo}{contador}{extension}"
        
        ruta_antigua = os.path.join(carpeta_origen, archivo)
        ruta_nueva = os.path.join(carpeta_destino, nuevo_nombre)
        
        # Mueve la imagen ya renombrada a la carpeta principal
        os.rename(ruta_antigua, ruta_nueva)
        print(f" Renombrado: {archivo} ➡️ {nuevo_nombre}")
        
        contador += 1

    print(f"\n¡Listo! Las imágenes ahora van hasta la #{contador - 1} en '{carpeta_destino}'.")

if __name__ == "__main__":
    # Carpeta donde están las fotos nuevas (las que también se llaman 1 a 80)
    CARPETA_NUEVAS = "images/carpeta ordenada/ingles"
    
    # Carpeta principal donde quieres juntar todo
    CARPETA_FINAL = "images/carpeta ordenada/"
    
    # Número en el que debe continuar la secuencia
    NUMERO_INICIAL = 81
    
    PREFIJO = ""

    continuar_secuencia(CARPETA_NUEVAS, CARPETA_FINAL, inicio=NUMERO_INICIAL, prefijo=PREFIJO)