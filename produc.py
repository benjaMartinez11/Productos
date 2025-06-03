# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
from selenium import webdriver

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
#######################################################################
def fetch_dia():
    navagador = webdriver.Firefox()
    print("[DIA] Iniciando extracción...")
    category_url = "https://diaonline.supermercadosdia.com.ar/bebidas/gaseosas/cola"
    results = []

    navagador.get(category_url)

    soup = BeautifulSoup(navagador.page_source, "html.parser")
    container = soup.find(id="gallery-layout-container")
    if not container:
        print("[DIA] No se encontró el contenedor de productos.")
        return []

    productos = container.find_all("article")
    for product in productos:
        try:
            name_elem = product.find("h3")
            name = name_elem.text.strip() if name_elem else "Sin nombre"

            price_elem = product.find("span", class_="diaio-store-5-x-sellingPrice diaio-store-5-x-sellingPrice--hasListPrice")
            if not price_elem:
                for span in product.find_all("span"):
                    if "sellingPrice" in span.get("class", [""])[0]:
                        price_elem = span
                        break
            price = price_elem.text.strip() if price_elem else "Sin precio"

            link_elem = product.find("a", href=True)
            relative_url = link_elem["href"] if link_elem else "#"
            full_url = urljoin(category_url, relative_url)

            results.append(["DIA", name, price, full_url])
        except Exception as e:
            print("Error extrayendo producto DIA:", e)
    navagador.close()
    return results
#######################################################################
def fetch_carrefour():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    print("[CARREFOUR] Iniciando extracción...")
    category_url = "https://www.carrefour.com.ar/Bebidas/Gaseosas/Gaseosas-cola"
    results = []

    navagador = webdriver.Firefox()
    navagador.get(category_url)

    try:
        WebDriverWait(navagador, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pr0"))
        )

        soup = BeautifulSoup(navagador.page_source, "html.parser")

        container = soup.find("div", class_="valtech-carrefourar-search-result-3-x-loadingOverlay")

        if not container:
            print("[CARREFOUR] No se encontró el contenedor de productos.")
            navagador.quit()
            return []

        # Buscar productos dentro del contenedor
        productos = container.find_all("section", class_="vtex-product-summary-2-x-container")

        print(f"[CARREFOUR] Productos encontrados: {len(productos)}")

        for product in productos:
            try:
                # Extraer la marca (nombre pedido)
                name_elem = product.find("span", class_="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body")
                name = name_elem.text.strip() if name_elem else "Sin nombre"

                # Precio
                price_elem = product.find("span", class_="vtex-product-price-1-x-sellingPrice")
                if not price_elem:
                    for span in product.find_all("span"):
                        if "sellingPrice" in " ".join(span.get("class", [])):
                            price_elem = span
                            break
                price = price_elem.text.strip() if price_elem else "Sin precio"

                # Link
                link_elem = product.find("a", href=True)
                relative_url = link_elem["href"] if link_elem else "#"
                full_url = urljoin(category_url, relative_url)

                results.append(["CARREFOUR", name, price, full_url])
            except Exception as e:
                print("Error extrayendo producto Carrefour:", e)

    except Exception as e:
        print("[CARREFOUR] Error al cargar productos:", e)

    navagador.quit()
    return results



#######################################################################

def fetch_coto():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    print("[coto] Iniciando extracción...")
    category_url = "https://www.cotodigital.com.ar/sitios/cdigi/categoria/catalogo-bebidas-bebidas-sin-alcohol-gaseosas/_/N-n4l4r5"
    results = []

    navagador = webdriver.Firefox()
    navagador.get(category_url)

    try:
        WebDriverWait(navagador, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "productos"))
        )

        soup = BeautifulSoup(navagador.page_source, "html.parser")

        container = soup.find("div", class_="productos")

        if not container:
            print("[coto] No se encontró el contenedor de productos.")
            navagador.quit()
            return []

        # Buscar productos dentro del contenedor
        productos = container.find_all("div", class_="card-container")

        print(f"[coto] Productos encontrados: {len(productos)}")

        for product in productos:
            try:
                # Extraer la marca (nombre pedido)
                name_elem = product.find("h3", class_="nombre-producto cursor-pointer")
                name = name_elem.text.strip() if name_elem else "Sin nombre"

                # Precio
                price_elem = product.find("h4", class_="card-title text-center mt-1 m-0 p-0 ng-star-inserted")
                if not price_elem:
                    for span in product.find_all("span"):
                        if "sellingPrice" in " ".join(span.get("class", [])):
                            price_elem = span
                            break
                price = price_elem.text.strip() if price_elem else "Sin precio"

                # Link
                link_elem = product.find("a", href=True)
                relative_url = link_elem["href"] if link_elem else "#"
                full_url = urljoin(category_url, relative_url)

                results.append(["coto", name, price, full_url])
            except Exception as e:
                print("Error extrayendo producto coto:", e)

    except Exception as e:
        print("[coto] Error al cargar productos:", e)

    navagador.quit()
    return results

#######################################################################

def save_to_csv(data, filename="precios_supermercados.csv"):
    if not data:
        print("[SAVE] No hay datos para guardar.")
        return
    df = pd.DataFrame(data, columns=["Supermercado", "Producto", "Precio", "URL"])
    df.to_csv(filename, index=False)
    print(f"[SAVE] Archivo guardado en {filename}")

def main():
    print("[MAIN] Iniciando extracción de precios...")
    all_data = []

    all_data.extend(fetch_dia())
    all_data.extend(fetch_carrefour())
    all_data.extend(fetch_coto())

    print(f"[MAIN] Total de registros: {len(all_data)}")
    save_to_csv(all_data)
    print("[MAIN] Proceso finalizado.")

if __name__ == "__main__":
    main()
