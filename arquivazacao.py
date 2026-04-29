import pandas as pd
import xlsxwriter as xl

path = "salvamentos/"


def FactoryArquizacao(Lista, Tipo):

    match Tipo:
        case "excell":
            criarExcell(Lista)
        case "csv":
            criarSCV(Lista)
        case "json":
            criarJson(Lista)
        case "html":
            criarHTML(Lista)


def criarExcell(Lista):
    df = pd.DataFrame(Lista)
    write = pd.ExcelWriter(f"{path}tudo_ai.xls", engine="xlsxwriter")

    df.to_excel(write, sheet_name="jogos", index=False)

    workbook = write.book
    worksheet = write.sheets["jogos"]

    formato_alerta = workbook.add_format(
        {"bg_color": "#FFC7CE", "font_color": "#9C0006"}
    )

    formato_cabecalho = workbook.add_format(
        {"bold": True, "border": 1, "bg_color": "#D7E4BC"}
    )

    num_linhas = len(df)

    worksheet.conditional_format(
        1,
        5,
        num_linhas,
        5,
        {"type": "cell", "criteria": ">", "value": 15, "format": formato_alerta},
    )

    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:G", 15)

    worksheet.autofilter(0, 0, num_linhas, len(df.columns) - 1)

    write.close()
    print(f"Planilha salva com sucesso: tudo_ai.xls")


def criarSCV(lista):
    df = pd.DataFrame(lista)
    df.to_csv(f"{path}tudo_ai.csv", index=True)


def criarJson(Lista):
    df = pd.DataFrame(Lista)
    df.to_json(f"{path}tudo_ai.json", index=False)


def criarHTML(Lista):
    df = pd.DataFrame(Lista)
    df.to_html(f"{path}tudo_ai.html", index=False)
