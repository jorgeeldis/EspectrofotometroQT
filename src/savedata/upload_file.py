import os
import requests
from bs4 import BeautifulSoup

# Función para subir un archivo a la página web
def upload(file_path):
    
    # file_name = os.path.basename(file_path)
    file_name = os.path.basename(file_path).split('/')[-1]

    url = "https://app.espectrocg.com/upload"  # Reemplaza con la URL de la página con el formulario
    # Realizar una solicitud GET para obtener la página con el formulario
    response = requests.get(url)

    # Extraer el token CSRF del HTML
    soup = BeautifulSoup(response.text, "html.parser")
    token_csrf = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")
    print(token_csrf)

    token_csrf_cookie = response.cookies.get("csrftoken")
    print(token_csrf_cookie)

    # Cargar el archivo
    with open(file_path, "rb") as archivo_para_subir:
        # Crear los datos del formulario
        datos_formulario = {
            "file": archivo_para_subir,
        }

        # Realizar la solicitud HTTP POST con el token CSRF
        respuesta = requests.post(
            url,
            data={"filename": file_name, "csrfmiddlewaretoken": token_csrf},
            files=datos_formulario,
            cookies={"csrftoken": token_csrf_cookie},
            headers={"Referer": url},
        )

    # Verificar el estado de la respuesta
    if respuesta.status_code == 200:
        return True
    else:
        return False
