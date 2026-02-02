from playwright.sync_api import sync_playwright
import os

USUARIO = os.environ.get("USUARIO")
PASSWORD = os.environ.get("PASSWORD")

if not USUARIO or not PASSWORD:
    raise Exception("Faltan las variables de entorno USUARIO o PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )
    page = context.new_page()

    # 1. Login
page.goto("https://www.compraensanjuan.com/login.php", timeout=60000)
page.wait_for_selector("input[name='email']", timeout=60000)
page.wait_for_selector("input[name='clave']", timeout=60000)

page.fill("input[name='email']", USUARIO)
page.fill("input[name='clave']", PASSWORD)

page.wait_for_selector("form button[type='submit']:visible", timeout=60000)
page.click("form button[type='submit']:visible")

page.wait_for_load_state("networkidle")


    # 2. Ir a Mi cuenta (donde está el botón real)
    page.goto("https://www.compraensanjuan.com/micuenta.php", timeout=60000)
    page.wait_for_load_state("networkidle")

    # 3. Click en el botón que llama a validar actualizar
    page.wait_for_selector("button[onclick*='actualizaractivos']", timeout=60000)
    page.click("button[onclick*='actualizaractivos']")

    page.wait_for_timeout(4000)
    browser.close()


    # 4. Enviar formulario (si el botón es submit)
    page.click("button[type='submit']")

    # 5. Esperar que termine el login
    page.wait_for_load_state("networkidle")

    # 6. Ir a publicaciones
    page.goto("https://www.compraensanjuan.com/mispublicaciones.php", timeout=60000)
    page.wait_for_timeout(3000)

    # 7. Click en actualizar
    page.locator("text=Actualizar").first.click()

    page.wait_for_timeout(3000)
    browser.close()
