from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import logging
import datetime as date
import os

# -------------------------------------------------------------------------

os.makedirs("logs", exist_ok=True)
log_filename = f"logs/execucao_{date.time().strftime('%Y-%m-%d_%H-%M-%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# -------------------------------------------------------------------------


def scraping(jogos):

    seletores = {
        "nota_publica": (
            By.XPATH,
            '//*[@id="__nuxt"]/div[2]/main/div/div/section[1]/div/div[3]/div[4]/div/div[2]/div[1]/div[2]/div/div/span',
        ),
        "nota_critica": (By.CSS_SELECTOR, '[data-testid="global-score-value"]'),
        "reviews_publica": (
            By.XPATH,
            '//*[@id="__nuxt"]/div[2]/main/div/div/section[1]/div/div[3]/div[4]/div/div[2]/div[1]/div[1]/div[2]/div[2]/a',
        ),
        "reviews_critca": (
            By.CSS_SELECTOR,
            '[data-testid="global-score-review-count-link"]',
        ),
        "genero": (By.CSS_SELECTOR, ".global-link-button__label"),
        "empresa": (By.CSS_SELECTOR, 'a[href*="/company/"]'),
    }

    user_agent = UserAgent().random

    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    with webdriver.Chrome(service=service, options=options) as driver:

        wait = WebDriverWait(driver, 10)
        notas = []

        for cada_jogo in jogos:

            try:

                dados_jogo = {"jogo": cada_jogo}

                driver.get(f"https://www.metacritic.com/game/{cada_jogo}/")

                for chave, (tipo_busca, caminho) in seletores.items():

                    elemento = wait.until(
                        EC.presence_of_element_located((tipo_busca, caminho))
                    ).text

                    if chave == "nota_publica":
                        elemento = elemento.replace(".", "")

                    dados_jogo[chave] = elemento

                dados_jogo["gap"] = abs(
                    int(dados_jogo["nota_publica"]) - int(dados_jogo["nota_critica"])
                )

                notas.append(dados_jogo)
                print(f"{cada_jogo} coletado com sucesso")
                logging.info(f"Sucesso: {cada_jogo}")

            except Exception as e:
                print(f"ERRO EM : {cada_jogo}... pulando para o proximo")
                logging.warning(f"Aviso em {cada_jogo}: {e}")

    driver.quit()
    logging.info("Navegador fechado corretamente.")

    return notas


def limpeza(jogos):

    return [
        j.replace("'", "").replace(":", "").replace(" ", "-").replace("’", "").lower()
        for j in jogos
    ]


def quebraLista(jogos, n):

    tamanho = len(jogos) // n
    saida = []

    for i in range(0, len(jogos), tamanho):
        saida.append(jogos[i : i + tamanho])

    return saida


def scraping_MultiTreads(jogos, n):
    jogos = limpeza(jogos)
    Lista_Blocos = quebraLista(jogos, n)

    notas_totais = []

    with ThreadPoolExecutor(max_workers=n) as executor:
        resultados = executor.map(scraping, Lista_Blocos)

    for i in resultados:
        notas_totais.extend(i)

    return notas_totais
