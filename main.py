from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
from tqdm import tqdm

# Disable DEBUG messages
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

def scrape_falabella(url_base, num_pages=10):
    data = []
    for page in tqdm(range(1, num_pages + 1), desc="Procesando páginas"):
        url = f"{url_base}?page={page}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            html_content = response.content
            soup = BeautifulSoup(html_content, 'lxml')
            elements = soup.find_all('div', class_="jsx-1068418086")
            for element in elements:
                try:  # Manejo de errores para elementos individuales
                    nombre_producto = element.find('b', class_='pod-subTitle').text.strip()
                    precio_texto = element.find('li', class_='prices-0').find('span', class_='copy10').text.strip()
                    precio = float(precio_texto.replace('$', '').replace('.', ''))
                    # ... (resto del código de extracción de datos como antes)
                    data.append({
                        'Nombre': nombre_producto,
                        'Precio': precio,
                        # ... (resto de los campos)
                    })
                except Exception as e:
                    logging.error(f"Error al procesar elemento: {e}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error al obtener la página {url}: {e}")
            break # Detener el scraping si hay un error de red

    return pd.DataFrame(data)


if __name__ == "__main__":
    url_base = 'https://www.falabella.com.co/falabella-co/category/cat1361001/Computadores-Portatiles'
    df = scrape_falabella(url_base)
    print(df)
    df.to_csv("laptops.csv", index=False)