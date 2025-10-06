import os
import random
import time
from playwright.sync_api import sync_playwright

SESSION_FILE = "session.json"

# ------------------- Funções auxiliares -------------------

def human_delay(min_ms=300, max_ms=1200):
    """Espera um tempo aleatório simulando reação humana."""
    time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))

def human_move_mouse(page, element):
    """Move o mouse de forma 'humana' até o centro do elemento."""
    box = element.bounding_box()
    if not box:
        return

    # Começa em uma posição aleatória da tela
    start_x, start_y = random.randint(0, 400), random.randint(0, 300)
    page.mouse.move(start_x, start_y)
    human_delay(200, 500)

    # Faz movimentos intermediários antes de chegar
    for _ in range(random.randint(2, 4)):
        mid_x = random.uniform(box["x"], box["x"] + box["width"])
        mid_y = random.uniform(box["y"], box["y"] + box["height"])
        page.mouse.move(mid_x, mid_y, steps=random.randint(15, 30))
        human_delay(50, 200)

    # Move até o centro do botão/input
    target_x = box["x"] + box["width"] / 2
    target_y = box["y"] + box["height"] / 2
    page.mouse.move(target_x, target_y, steps=random.randint(20, 40))
    human_delay(200, 500)

def human_click(page, element):
    """Simula um clique humano no elemento."""
    human_move_mouse(page, element)
    page.mouse.down()
    human_delay(50, 150)
    page.mouse.up()
    human_delay(200, 600)

def fechar_modal(page):
    try:
        # pega todos os elementos que correspondem ao seletor
        elements = page.query_selector_all("i.eds-modal__close")
        for el in elements:
            if el.is_visible():
                human_click(page, el)
                print("Modal visível fechado com sucesso.")
                return
        print("Nenhum botão de fechar visível, seguindo o fluxo.")
    except Exception as e:
        print(f"Erro ao tentar fechar modal: {e}")



def human_type(element, text):
    """Digita como humano, letra por letra, com variação de tempo."""
    for char in text:
        element.type(char, delay=random.randint(50, 200))  # entre 50 e 200ms por caractere
    human_delay(300, 700)


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
    # Pega só o link exato de "Produtos"
    btn = page.get_by_role("link", name="Produtos", exact=True)
    btn.wait_for(state="visible", timeout=10000)
    human_click(page, btn)
    human_delay(1000, 2000)


def pesquisar_produto(page, nome_produto):
    """Pesquisa por um produto e pressiona Enter."""
    # localiza todos os inputs e pega o primeiro visível
    inputs = page.locator("div.eds-input__inner input[placeholder*='Pesquisar Nome do Produto']")
    input_pesquisa = None
    for i in range(inputs.count()):
        candidate = inputs.nth(i)
        if candidate.is_visible():
            input_pesquisa = candidate
            break

    if input_pesquisa is None:
        raise Exception("Não encontrou input de pesquisa visível!")

    # espera o input estar visível e anexado
    input_pesquisa.wait_for(state="visible", timeout=10000)

    input_pesquisa.scroll_into_view_if_needed()
    human_click(page, input_pesquisa)

    # limpa o campo como humano
    input_pesquisa.press("Control+A")
    human_delay(100, 300)
    input_pesquisa.press("Backspace")
    human_delay(200, 500)

    # garante que o input ainda está habilitado antes de digitar
    if not input_pesquisa.is_enabled():
        raise Exception("Input de pesquisa não está habilitado!")

    # digita o produto
    human_type(input_pesquisa, nome_produto)

    input_pesquisa.press("Enter")
    human_delay(800, 1500)





def clicar_mais(page):
    """Clica no primeiro botão 'Mais' visível na tela."""
    # espera pelo botão 'Mais' aparecer visível
    try:
        page.wait_for_selector("button:has-text('Mais')", state="visible", timeout=10000)
    except:
        print("Não encontrou nenhum botão 'Mais' visível após esperar 10s.")
        return False

    mais_buttons = page.locator("button:has-text('Mais')")
    for i in range(mais_buttons.count()):
        btn = mais_buttons.nth(i)
        if btn.is_visible():
            btn.scroll_into_view_if_needed()
            human_click(page, btn)
            human_delay(1000, 2000)
            print("Botão 'Mais' clicado.")
            return True

    print("Não encontrou nenhum botão 'Mais' visível mesmo após esperar.")
    return False



def clicar_impulsionar_agora(page):
    """Clica no botão 'Impulsionar Agora' se visível."""
    spans = page.locator("span")
    for i in range(spans.count()):
        span = spans.nth(i)
        if span.is_visible() and span.inner_text().strip() == "Impulsionar Agora":
            span.scroll_into_view_if_needed()
            human_click(page, span)
            print("Impulsionado!")
            return True
    print("⚠️ Não foi possível clicar em 'Impulsionar Agora'")
    return False


def salvar_sessao(context):
    """Salva a sessão atual."""
    context.storage_state(path=SESSION_FILE)


# ------------------- Fluxo principal -------------------
if not os.path.exists(SESSION_FILE):
    login_manual()

p, browser, context, page = start_browser_with_session()

try:
    page.goto("https://accounts.shopee.com.br/seller/login")
    human_delay(4000, 6000)

    #fechar_modal(page)
    #input("Pressione Enter para começar a automação...")

    abrir_aba_produtos(page)

    human_delay(4000, 6000)
    produtos = ["18497628810", "23597447451", "18897750589", "22893207112", "22493221678"]

    for produto in produtos:
        pesquisar_produto(page, produto)
        print("Produto pesquisado.")
        clicar_mais(page)
        print("Botão 'Mais' selecionado.")
        human_delay(3000, 6000)
        clicar_impulsionar_agora(page)
        human_delay(3000, 6000)

    input("Pressione Enter para fechar o browser...")
finally:
    browser.close()
    p.stop()
