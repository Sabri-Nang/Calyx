from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook


def get_values(url: str) -> list:
    '''
    Obtengo los datos de la url.
    Devuelve una lista.
    Cada fila de la tabla será un elemento de la lista.
    '''
    driver = webdriver.Chrome()
    try:
        driver.get(url)
    except Exception:
        print('No se puede acceder a la web solicitada')
        return
    elemento = driver.find_element(By.ID, "billetes")
    trs = elemento.find_elements(By.TAG_NAME, "tr")
    driver.quit()
    rows = []
    for tr in trs:
        rows.append(tr.text)
    return rows


def create_excel(url, file):
    rows = get_values(url)
    wb = Workbook()
    ws = wb.active
    ws.append(['Dia', rows[0].split(' ')[0]])
    ws.append(['Moneda', rows[0].split(' ')[1],
               rows[0].split(' ')[2], 'Promedio'])
    for row in rows[1:]:
        row = row.split(' ')
        row_normalize = []
        for value in row:
            if ',' in value:
                value = value.replace(',', '.')
            try:
                value = round(float(value), 2)
                row_normalize.append(value)
            except Exception:
                if value.lower() in ['dolar', 'euro', 'real']:
                    row_normalize.append(value)
        promedio = (row_normalize[-1]+row_normalize[-2])/2
        row_normalize.append(promedio)
        ws.append(row_normalize)
    wb.save(filename=file)


def main():
    url = 'https://www.bna.com.ar/Personas'
    file = 'cotizacion.xlsx'
    create_excel(url, file)


main()
