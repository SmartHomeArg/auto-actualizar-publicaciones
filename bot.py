from playwright.sync_api import sync_playwright
import os

USUARIO = os.environ["USUARIO"]
PASSWORD = os.environ["PASSWORD"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1. Ir a login
    page.goto("https://compraensanjuan.com/micuenta.php")

    # 2. Login
    page.fill("input[name='usuario']", USUARIO)
    page.fill("input[name='password']", PASSWORD)
    page.click("button[type='submit']")

    # 3. Esperar que cargue
    page.wait_for_load_state("networkidle")

    # 4. Ir a publicaciones activas
    page.goto("https://compraensanjuan.com/mispublicaciones.php")

    # 5. Click en actualizar
    page.click("text=Actualizar")

    # 6. Esperar confirmación
    page.wait_for_timeout(3000)

    browser.close()
