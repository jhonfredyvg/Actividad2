from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

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


            # Limpieza de datos
        df['Precio'] = df['Precio'].str.replace('$  ', '').str.replace('.', '').str.replace(',', '').astype(float)
        df['Valor sin Descuento'] = df['Valor sin Descuento'].str.replace('$  ', '').str.replace('.', '').str.replace(',', '')
        df['Valor sin Descuento'] = df['Valor sin Descuento'].replace('N/A', float('nan')).astype(float)
        df['Descuento'] = df['Descuento'].replace('N/A', '0').str.replace('%', '').str.replace('-', '').str.replace('.', '').str.replace(',', '').astype(float)

        # Configuración del estilo
        sns.set_theme(style="darkgrid")

        # 1. Análisis Básico
        print("\n=== Análisis Básico ===")
        print("\nEstadísticas de Precios:")
        print(df['Precio'].describe())

        print("\nNúmero de productos por marca:")
        print(df['Marca'].value_counts())

        print("\nPromedio de precio por marca:")
        print(df.groupby('Marca')['Precio'].mean().sort_values(ascending=False))

        # 2. Top 5 productos más caros y más baratos
        print("\n=== Top 5 Productos ===")
        print("\nProductos más caros:")
        print(df.nlargest(5, 'Precio')[['Nombre', 'Marca', 'Precio']])
        print("\nProductos más baratos:")
        print(df.nsmallest(5, 'Precio')[['Nombre', 'Marca', 'Precio']])

        # 3. Visualizaciones principales

        # 3.1 Distribución de Precios
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='Precio', bins=20)
        plt.title('Distribución de Precios de Laptops')
        plt.xlabel('Precio (COP)')
        plt.ylabel('Frecuencia')
        plt.show()

        # 3.2 Precios por Marca
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='Marca', y='Precio')
        plt.xticks(rotation=45)
        plt.title('Precios por Marca')
        plt.xlabel('Marca')
        plt.ylabel('Precio (COP)')
        plt.show()

        # 3.3 Proporción de Envío Gratis
        envio_counts = df['Envío Gratis'].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(envio_counts.values, labels=envio_counts.index, autopct='%1.1f%%')
        plt.title('Proporción de Productos con Envío Gratis')
        plt.show()

        # 4. Resumen por Marca
        resumen_marca = df.groupby('Marca').agg({
            'Precio': ['count', 'mean', 'min', 'max'],
            'Envío Gratis': lambda x: (x == 'Sí').mean() * 100
        }).round(2)

        resumen_marca.columns = ['Cantidad', 'Precio Promedio', 'Precio Mínimo', 'Precio Máximo', 'Porcentaje Envío Gratis']

        print("\n=== Resumen por Marca ===")
        print(resumen_marca)

        # Guardar datos
        df.to_csv('laptops_data.csv', index=False)
        print("\nLos datos han sido guardados en 'laptops_data.csv'")

    return pd.DataFrame(data)


if __name__ == "__main__":
    url_base = 'https://www.falabella.com.co/falabella-co/category/cat1361001/Computadores-Portatiles'
    df = scrape_falabella(url_base)
    print(df)
    df.to_csv("laptops.csv", index=False)