import pandas as pd
import xlsxwriter as xl

path = "salvamentos/"


def FactoryArquizacao(Lista, Tipo):

    df = pd.DataFrame(Lista)

    match Tipo:
        case "excell":
            criarExcell(df)
        case "csv":
            criarSCV(df)
        case "json":
            criarJson(df)
        case "html":
            criarHTML(df)


def criarExcell(df):
    write = pd.ExcelWriter(f"{path}tudo_ai.xlsx", engine="xlsxwriter")

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


def criarSCV(df):
    df.to_csv(f"{path}tudo_ai.csv", index=True)


def criarJson(df):
    df.to_json(f"{path}tudo_ai.json", index=False)


def criarHTML(df):
    df.to_html(f"{path}tudo_ai.html", index=False)
