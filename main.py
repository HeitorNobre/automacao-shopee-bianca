import os
from playwright.sync_api import sync_playwright
import time

# Caminho do arquivo de sessão
SESSION_FILE = "session.json"

def login_shopee():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://accounts.shopee.com.br/seller/login")

        print("Faça login manualmente e depois aperte Enter aqui...")
        input()  # pausa para login manual

        # Salva a sessão
        page.context.storage_state(path=SESSION_FILE)
        browser.close()

# Se a sessão não existe, faz login manual
if not os.path.exists(SESSION_FILE):
    login_shopee()

# Agora abre o browser com a sessão salva
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state=SESSION_FILE)  # carrega sessão
    page = context.new_page()
    page.goto("https://accounts.shopee.com.br/seller/login")
    time.sleep(10)

    # Clicar na aba de produtos
    page.wait_for_selector("a:has-text('Produtos')", state="visible")
    page.click("a:has-text('Produtos')")
    
    time.sleep(5)

    # pega o primeiro ícone "sort-dsc"
    page.wait_for_selector("div.action-icon.order-icon")
    is_desc = page.locator("i.sort-dsc").nth(1).is_visible()

    # garante que a coluna fique sempre em ordem descendente
    if not is_desc:
        page.locator("div.action-icon.order-icon").nth(1).click()

    print("Terminou...")
    input()  # pausa para login manual

    # Salva a sessão
    page.context.storage_state(path=SESSION_FILE)
    browser.close()

    # Dentro da página de produtos, clicar nos produtos para dar boost

   # 1. Clica no botão "Mais"

#    # number one ---------------------------------------------------------------------------------
#     # Clica no "Mais"
#     page.locator("button:has-text('Mais')").first.click()

#     # Aguarda um tempo fixo para o menu carregar
#     page.wait_for_timeout(3000)

#     # Usa uma função JavaScript para clicar no primeiro "Impulsionar Agora" visível
#     success = page.evaluate("""
#         () => {
#             const spans = document.querySelectorAll('span[data-v-5b614814]');
#             for (const span of spans) {
#                 if (span.textContent.trim() === 'Impulsionar Agora') {
#                     const rect = span.getBoundingClientRect();
#                     if (rect.width > 0 && rect.height > 0) {
#                         span.click();
#                         return true;
#                     }
#                 }
#             }
#             return false;
#         }
#     """)

#     if not success:
#         print("Não foi possível clicar em 'Impulsionar Agora'")


    # number two ---------------------------------------------------------------------------------

    # Clica no "Mais"
    page.locator("button:has-text('Mais')").nth(1).click()

    # Aguarda um tempo fixo para o menu carregar
    page.wait_for_timeout(3000)

    # Usa uma função JavaScript para clicar no primeiro "Impulsionar Agora" visível
    success = page.evaluate("""
        () => {
            const spans = document.querySelectorAll('span[data-v-5b614814]');
            for (const span of spans) {
                if (span.textContent.trim() === 'Impulsionar Agora') {
                    const rect = span.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        span.click();
                        return true;
                    }
                }
            }
            return false;
        }
    """)

    if not success:
        print("Não foi possível clicar em 'Impulsionar Agora'")

    # number three ---------------------------------------------------------------------------------

    # Clica no "Mais"
    page.locator("button:has-text('Mais')").nth(6).click()

    # Aguarda um tempo fixo para o menu carregar
    page.wait_for_timeout(3000)

    # Usa uma função JavaScript para clicar no primeiro "Impulsionar Agora" visível
    success = page.evaluate("""
        () => {
            const spans = document.querySelectorAll('span[data-v-5b614814]');
            for (const span of spans) {
                if (span.textContent.trim() === 'Impulsionar Agora') {
                    const rect = span.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        span.click();
                        return true;
                    }
                }
            }
            return false;
        }
    """)

    if not success:
        print("Não foi possível clicar em 'Impulsionar Agora'")


    # # Aguarda diretamente pelo botão "Impulsionar Agora" aparecer
    # page.wait_for_selector("text=Impulsionar Agora", state="visible", timeout=10000)

    # # Clica no "Impulsionar Agora"
    # page.locator("text=Impulsionar Agora").first.click()




    
    #time.sleep(5)
    
    # Continua a automação
