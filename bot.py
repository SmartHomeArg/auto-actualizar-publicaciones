from playwright.sync_api import sync_playwright
import os
import time

USUARIO = os.environ.get("USUARIO")
PASSWORD = os.environ.get("PASSWORD")

if not USUARIO or not PASSWORD:
    raise Exception("Faltan las variables de entorno USUARIO o PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )
    page = context.new_page()

    # 1️⃣ Abrir login
    page.goto("https://www.compraensanjuan.com/login.php", timeout=60000)

    # 2️⃣ Completar campos
    page.wait_for_selector('input[name="email"]', timeout=60000)
    page.wait_for_selector('input[name="clave"]', timeout=60000)
    page.fill('input[name="email"]', USUARIO)
    page.fill('input[name="clave"]', PASSWORD)

    # 3️⃣ Click en "Siguiente"
    page.click('button[onclick*="valida_envia"]')

    # Esperar redirección automática a micuenta.php
    page.wait_for_url("**/micuenta.php", timeout=60000)
    page.wait_for_load_state("networkidle")

    # 4️⃣ Click en botón "Actualizar publicaciones"
    page.wait_for_selector('button[onclick*="actualizaractivos"]', timeout=60000)
    page.click('button[onclick*="actualizaractivos"]')

    # Esperar que termine la acción
    time.sleep(4)

    # 5️⃣ Cerrar sesión
    page.wait_for_selector('a[href="cierre_sesion.php"]', timeout=60000)
    page.click('a[href="cierre_sesion.php"]')

    browser.close()
