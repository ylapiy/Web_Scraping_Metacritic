from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

jogos = [
    "Elden Ring",
    "Bloodborne",
    "Sekiro: Shadows Die Twice",
    "Monster Hunter: World",
    "Monster Hunter Rise",
    "Lies of P",
    "Demon’s Souls (Remake)",
    "Nioh",
    "Nioh 2",
    "Wo Long: Fallen Dynasty",
    "The Surge",
    "The Surge 2",
    "Mortal Shell",
    "Lords of the Fallen",
    "Salt and Sanctuary",
    "Blasphemous",
    "Blasphemous 2",
    "Hollow Knight",
    "Tunic",
    "Remnant: From the Ashes",
    "Remnant ii",
    "Wild Hearts",
    "Dragon’s Dogma 2",
    "Code Vein",
    "Another Crab's Treasure",
    "Enotria: The Last Song",
    "Black Myth: Wukong",
    "Sifu",
    "Thymesia",
    "Subnautica",
    "The Forgotten City",
    "Firewatch",
    "Returnal",
    "Deathloop",
    "Sable",
    "Return of the Obra Dinn",
    "Chants of Sennaar",
    "The Witness",
    "The Talos Principle",
    "The Talos Principle 2",
    "No Man's Sky",
    "Citizen Sleeper",
    "SOMA",
    "Pacific Drive",
    "DOOM Eternal",
    "Dusk",
    "Turbo Overkill",
    "Amid Evil",
    "Ghostrunner",
    "Ghostrunner 2",
    "Metal: Hellsinger",
    "BPM: Bullets Per Minute",
    "Post Void",
    "Cruelty Squad",
    "Prodeus",
    "Ion Fury",
    "Shadow Warrior 2",
    "Titanfall 2",
    "Severed Steel",
    "Roboquest",
    "Overwatch 2",
    "Paladins",
    "Valorant",
    "Apex Legends",
    "Team Fortress 2",
    "Gundam Evolution",
    "Gigantic: Rampage Edition",
    "Bleeding Edge",
    "Predecessor",
    "Smite",
    "Devil May Cry 5",
    "Bayonetta 3",
    "Metal Gear Rising: Revengeance",
    "Hades",
    "Hades II",
    "Dead Cells",
    "Nier: Automata",
    "Astral Chain",
    "God of War (Valhalla DLC)",
    "Vanquish",
    "Hi-Fi RUSH",
    "Darkest Dungeon",
    "Darkest Dungeon ii",
    "Fear & Hunger",
    "Rain World",
    "Pathologic 2",
    "STALKER 2: Heart of Chornobyl",
    "Metro Exodus",
    "Grim Dawn",
    "Armored Core VI: Fires of Rubicon",
    "Katana ZERO",
    "Hotline Miami",
    "Enter the Gungeon",
    "The Binding of Isaac: Repentance",
    "Risk of Rain 2",
    "Granblue Fantasy: Relink",
    "God Eater 3",
    "Toukiden 2",
    "Dauntless",
    "Hellblade: Senua's Sacrifice",
    "Scorn",
    "ExoPrimal",
    "Warframe",
    "Destiny 2",
    "Shadow of the Colossus",
    "Dragon's Dogma: Dark Arisen",
]


def scraping(jogos):

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    notas = []

    for cada_jogo in jogos:

        try:

            driver.get(f"https://www.metacritic.com/game/{cada_jogo}/")

            wait = WebDriverWait(driver, 10)
            nota_publica = driver.find_element(
                By.XPATH,
                '//*[@id="__nuxt"]/div[2]/main/div/div/section[1]/div/div[3]/div[4]/div/div[2]/div[1]/div[2]/div/div/span',
            ).text
            nota_publica = nota_publica.replace(".", "")

            wait = WebDriverWait(driver, 10)
            reviews_publicas = driver.find_element(
                By.XPATH,
                '//*[@id="__nuxt"]/div[2]/main/div/div/section[1]/div/div[3]/div[4]/div/div[2]/div[1]/div[1]/div[2]/div[2]/a',
            ).text

            wait = WebDriverWait(driver, 10)
            nota_critica = driver.find_element(
                By.CSS_SELECTOR, '[data-testid="global-score-value"]'
            ).text

            wait = WebDriverWait(driver, 10)
            reviews_critica = driver.find_element(
                By.CSS_SELECTOR, '[data-testid="global-score-review-count-link"]'
            ).text

            nota_critica_num = int(nota_critica)
            nota_publica_num = int(nota_publica)

            gap = nota_publica_num - nota_critica_num

            gap = gap * -1 if gap < 0 else gap

            (
                print(
                    f"{cada_jogo} : {nota_publica} | {reviews_publicas} | {nota_critica} | {reviews_critica} |, gap de : {gap}"
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
                }
            )

        except Exception as e:
            print(f"ERRO EM : {cada_jogo}... pulando para o proximo")

    driver.quit()

    return notas


def criarSCV(lista):
    df = pd.DataFrame(lista)
    df.to_csv("tudo_ai.csv", index=True)


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

    criarSCV(notas_totais)


scraping_MultiTreads(jogos, 5)
