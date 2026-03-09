from playwright.sync_api import sync_playwright, TimeoutError
import os
import time

USUARIO = os.environ.get("USUARIO")
PASSWORD = os.environ.get("PASSWORD")

if not USUARIO or not PASSWORD:
    raise Exception("Faltan las variables de entorno USUARIO o PASSWORD")

URL = "https://www.compraensanjuan.com/login.php"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        ignore_https_errors=True
    )

    page = context.new_page()

    # Intentar cargar la página hasta 3 veces
    for intento in range(3):
        try:
            print(f"Intento {intento+1} de cargar la página")
            page.goto(URL, wait_until="domcontentloaded", timeout=20000)
            break
        except TimeoutError:
            print("Timeout al cargar la página, reintentando...")
            time.sleep(5)
    else:
        raise Exception("No se pudo cargar la página")

    # Login
    page.fill('input[name="email"]', USUARIO)
    page.fill('input[name="clave"]', PASSWORD)

    page.click('button[onclick*="valida_envia"]')

    page.wait_for_url("**/micuenta.php", timeout=60000)

    # Actualizar publicaciones
    page.click('button[onclick*="actualizaractivos"]')

    time.sleep(3)

    browser.close()
    #except:
    #    print("No se encontró el botón de cerrar sesión, continuando igual...")

    browser.close()
