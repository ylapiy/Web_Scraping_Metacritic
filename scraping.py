from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor


def scraping(jogos):

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 10)

    notas = []

    for cada_jogo in jogos:

        try:

            driver.get(f"https://www.metacritic.com/game/{cada_jogo}/")

            genero = driver.find_element(
                By.CSS_SELECTOR, ".global-link-button__label"
            ).text

            empresa = driver.find_element(By.CSS_SELECTOR, 'a[href*="/company/"]').text

            nota_publica = driver.find_element(
                By.XPATH,
                '//*[@id="__nuxt"]/div[2]/main/div/div/section[1]/div/div[3]/div[4]/div/div[2]/div[1]/div[2]/div/div/span',
            ).text
            nota_publica = nota_publica.replace(".", "")

            reviews_publicas = driver.find_element(
                By.XPATH,
                '//*[@id="__nuxt"]/div[2]/main/div/div/section[1]/div/div[3]/div[4]/div/div[2]/div[1]/div[1]/div[2]/div[2]/a',
            ).text

            nota_critica = driver.find_element(
                By.CSS_SELECTOR, '[data-testid="global-score-value"]'
            ).text

            reviews_critica = driver.find_element(
                By.CSS_SELECTOR, '[data-testid="global-score-review-count-link"]'
            ).text

            nota_critica_num = int(nota_critica)
            nota_publica_num = int(nota_publica)

            gap = nota_publica_num - nota_critica_num

            gap = gap * -1 if gap < 0 else gap

            (
                print(
                    f"{cada_jogo} : {nota_publica} | {reviews_publicas} | {nota_critica} | {reviews_critica} |, gap de : {gap} | {genero} | {empresa}"
                )
            )

            notas.append(
                {
                    "jogo": cada_jogo,
                    "publico": nota_publica,
                    "reviewns players": reviews_publicas,
                    "critica": nota_critica,
                    "reviews critica": reviews_critica,
                    "gap": gap,
                    "genero": genero,
                    "empresa": empresa,
                }
            )

        except Exception as e:
            print(f"ERRO EM : {cada_jogo}... pulando para o proximo")

    driver.quit()

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
