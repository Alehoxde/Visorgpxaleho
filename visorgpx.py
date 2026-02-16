
import os 
import folium
import exif 
import gpxpy

from exif import Image


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS_DIR = os.path.join(BASE_DIR, "Visorgpxaleho", "web", "fotos")
OUTPUT_HTML = os.path.join(BASE_DIR, "Visorgpxaleho", "web", "index.html")
GPX_FILE = os.path.join(BASE_DIR,  "Visorgpxaleho", "data", "ruta.gpx")





def convertir_a_decimal(dms, ref):
    grados = float(dms[0])
    minutos = float(dms[1])
    segundos = float(dms[2])

    decimal = grados + (minutos / 60) + (segundos / 3600)

    if ref == "S":
        decimal *= -1
    if ref == "W":
        decimal *= -1

    return decimal



#Función para leer los datos GPS de una foto utilizando la biblioteca exif
def leer_exif_gps(ruta_foto_ciclo_actual):
    with open(ruta_foto_ciclo_actual, "rb") as image:
        exif_foto_ciclo_actual = Image(image)
        print(exif_foto_ciclo_actual.has_exif)
        latitud = exif_foto_ciclo_actual.gps_latitude
        lat_ref = exif_foto_ciclo_actual.gps_latitude_ref
        longitud = exif_foto_ciclo_actual.gps_longitude
        lon_ref = exif_foto_ciclo_actual.gps_longitude_ref
        lat_decimal = convertir_a_decimal(latitud, lat_ref)
        lon_decimal = convertir_a_decimal(longitud, lon_ref)

        print(lat_decimal, lon_decimal)
        print(f"Latitud: {lat_decimal}, Longitud: {lon_decimal}")
        print(f"Foto: {ruta_foto_ciclo_actual} - Latitud: {lat_decimal}, Longitud: {lon_decimal}")
        return lat_decimal, lon_decimal
    

def leer_gpx(ruta_gpx):
    coords = []
    with open(ruta_gpx, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    for track in gpx.tracks:
        for segment in track.segments:
            for p in segment.points:
                coords.append((p.latitude, p.longitude))
    return coords

#Funcion Principal para generar el mapa con las fotos
def generar_mapa():
    mapa = folium.Map(location=[0, 0], zoom_start=10, tiles="OpenStreetMap") 
    print(FOTOS_DIR)
    if os.path.isdir(FOTOS_DIR): 

        coordenadas_archivo_gpx = leer_gpx(GPX_FILE)
        folium.PolyLine(
        coordenadas_archivo_gpx,
        color="blue",
        weight=4,
        tooltip="ruta.gpx"
        ).add_to(mapa)


        for img in os.listdir(FOTOS_DIR):
            print(img)
            if img.lower().endswith((".jpg", ".jpeg")):
                ruta_foto_ciclo_actual = os.path.join(FOTOS_DIR, img)
                gps = leer_exif_gps(ruta_foto_ciclo_actual) 
                if gps:
                    latitud, longitud = gps
                        
                    html_marcador_foto_ciclo_actual = f"""
                    <b>{img}</b><br>
                    <img src="fotos/{img}" width="250">
                    """
                    
                    print(latitud)

                    folium.Marker(
                        location=(latitud, longitud),
                        popup=folium.Popup(html_marcador_foto_ciclo_actual, max_width=300),
                        icon=folium.Icon(icon="camera", prefix="fa")
                    ).add_to(mapa) 
               


        mapa.save(OUTPUT_HTML)
        print(f"Mapa generado exitosamente en {OUTPUT_HTML}")


if __name__ == "__main__":
    generar_mapa()



                

                    


                     


                   
                   
        

               
                 
                 
