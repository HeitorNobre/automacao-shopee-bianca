import os
from playwright.sync_api import sync_playwright
import time

SESSION_FILE = "session.json"

# ------------------- Funções reutilizáveis -------------------

def login_manual():
    """Abre a página de login para login manual e salva sessão."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://accounts.shopee.com.br/seller/login")

        print("Faça login manualmente e depois aperte Enter aqui...")
        input()  # pausa para login manual

        # Salva a sessão
        page.context.storage_state(path=SESSION_FILE)
        browser.close()


def start_browser_with_session():
    """Abre o browser com a sessão salva e retorna o contexto e a página."""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(
        storage_state=SESSION_FILE,
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    return p, browser, context, page


def abrir_aba_produtos(page):
    """Abre a aba 'Produtos' no Seller Center."""
    page.wait_for_selector("a:has-text('Produtos')", state="visible")
    page.click("a:has-text('Produtos')")
    page.wait_for_timeout(2000)


def pesquisar_produto(page, nome_produto):
    """Pesquisa por um produto e pressiona Enter."""
    # Localiza todos inputs com placeholder semelhante e escolhe o visível
    inputs = page.locator("div.eds-input__inner input[placeholder*='Pesquisar Nome do Produto']")
    input_pesquisa = None
    for i in range(inputs.count()):
        candidate = inputs.nth(i)
        if candidate.is_visible():
            input_pesquisa = candidate
            break

    if input_pesquisa is None:
        raise Exception("Não encontrou input de pesquisa visível!")

    input_pesquisa.scroll_into_view_if_needed()
    input_pesquisa.click()
    input_pesquisa.fill(nome_produto)
    input_pesquisa.press("Enter")
    page.wait_for_timeout(2000)

def clicar_mais(page):
    """Clica no primeiro botão 'Mais' visível na tela."""
    mais_buttons = page.locator("button:has-text('Mais')")
    for i in range(mais_buttons.count()):
        btn = mais_buttons.nth(i)
        if btn.is_visible():
            btn.scroll_into_view_if_needed()
            btn.click()
            page.wait_for_timeout(2000)  # espera o menu abrir
            print("Botão 'Mais' clicado.")
            return True
    print("Não encontrou nenhum botão 'Mais' visível.")
    return False

def clicar_impulsionar_agora(page):
    """
    Clica no primeiro botão 'Impulsionar Agora' visível usando JavaScript.
    Retorna True se conseguiu clicar, False caso contrário.
    """
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
        print("⚠️ Não foi possível clicar em 'Impulsionar Agora'")
    return success


def salvar_sessao(context):
    """Salva a sessão atual."""
    context.storage_state(path=SESSION_FILE)


# ------------------- Fluxo principal -------------------
if not os.path.exists(SESSION_FILE):
    login_manual()

p, browser, context, page = start_browser_with_session()

try:
    page.goto("https://accounts.shopee.com.br/seller/login")
    time.sleep(5)

    abrir_aba_produtos(page)
    input("Pressione Enter para fechar o browser...")

    produto_desejado = "18497628810"
    pesquisar_produto(page, produto_desejado)

    print("Produto pesquisado e Enter pressionado.")

    clicar_mais(page)

    print("Produto selecionado o mais")

    time.sleep(5)
    clicar_impulsionar_agora(page)
    time.sleep(5)

    #-------------------------------------------------------------
    #PRODUTO 2
    #-------------------------------------------------------------

    produto_desejado = "23597447451"
    pesquisar_produto(page, produto_desejado)

    print("Produto pesquisado e Enter pressionado.")

    clicar_mais(page)

    print("Produto selecionado o mais")

    time.sleep(5)

    clicar_impulsionar_agora(page)

    time.sleep(5)

    #---------------------------------------------------------------
    #PRODUTO 3
    #---------------------------------------------------------------

    produto_desejado = "18897750589"
    pesquisar_produto(page, produto_desejado)

    print("Produto pesquisado e Enter pressionado.")

    clicar_mais(page)

    print("Produto selecionado o mais")

    time.sleep(5)

    clicar_impulsionar_agora(page)

    time.sleep(5)
    #---------------------------------------------------------------
    #PRODUTO 4
    #---------------------------------------------------------------

    produto_desejado = "23597447525"
    pesquisar_produto(page, produto_desejado)

    print("Produto pesquisado e Enter pressionado.")

    clicar_mais(page)

    print("Produto selecionado o mais")

    time.sleep(5)

    clicar_impulsionar_agora(page)

    time.sleep(5)
    #---------------------------------------------------------------
    #PRODUTO 5
    #---------------------------------------------------------------

    produto_desejado = "22493221678"
    pesquisar_produto(page, produto_desejado)

    print("Produto pesquisado e Enter pressionado.")

    clicar_mais(page)

    print("Produto selecionado o mais")

    time.sleep(5)

    clicar_impulsionar_agora(page)

    time.sleep(5)

    # salvar_sessao(context)


    produtos = ["18497628810","23597447451","18897750589","23597447525","22493221678"]

    for produto in produtos:
        pesquisar_produto(page, produto)
        print("Produto pesquisado e Enter pressionado.")
        clicar_mais(page)
        print("Produto selecionado o mais")
        time.sleep(5)
        clicar_impulsionar_agora(page)
        time.sleep(5)
    
    
    input("Pressione Enter para fechar o browser...")
finally:
    browser.close()
    p.stop()
