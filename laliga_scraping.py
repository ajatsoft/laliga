from bs4 import BeautifulSoup
import requests, re, pandas as pd

def devuelveProbabilidades():
    ## urls
    url = "https://www.predictz.com/predictions/spain/primera-liga/"

    ## parametros de la cabecera
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }

    ## obtenemos la web
    response = requests.get(url, headers=headers)

    ## obtenemos el contenido formateado
    soup = BeautifulSoup(response.content.decode("utf-8"), features="html5lib")

    ## configuramos los filtros
    re_local = re.compile(".*?(?= v )")
    re_visitante = re.compile("(?<= v ).*")

    ## creamos el dataframe
    df = pd.DataFrame()

    ## obtenemos todos los partidos
    for partidos in soup.find_all("tr","pzcnth"):

        ## obtenemos los equipos
        for equipos in partidos.find_all("td","fixt"):
            equipo = equipos.a.string
            local = re_local.search(equipo).group(0)
            visitante = re_visitante.search(equipo).group(0)

        ## obtenemos las apuestas
        apuesta = []
        for apuestas in partidos.find_all("td","odds"):
            apuesta.append(apuestas.a.string)

        ## creamos un dataframe con cada linea
        data = pd.DataFrame([[local, visitante, apuesta[0], apuesta[1], apuesta[2]]]
            ,columns=["local","visitante","ganalocal","empate","ganavisitante"]
        )

        ## anexamos la nueva linea al dataframe
        df = df.append(data, ignore_index=True)

    ## obtenemos las probabilidades individuales de cada equipo
    local = df[["local","ganalocal","empate","ganavisitante"]]
    visitante = df[["visitante","ganavisitante","empate","ganalocal"]]

    ## cambiamos el nombre de las columnas para que coincidan
    local.columns = ["equipo","gana","empata","pierde"]
    visitante.columns = ["equipo","gana","empata","pierde"]

    ## creamos el dataframe final
    resultado = pd.DataFrame()

    ## anexamos los dos dataframes
    resultado = resultado.append(local, ignore_index=True)
    resultado = resultado.append(visitante, ignore_index=True)

    ## devolvemos el dataframe
    return resultado

## eof
