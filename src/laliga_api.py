import requests, csv, unidecode, pandas as pd

def devuelveClasificacion():
    ## urls
    url_equipos = "http://api.football-data.org/v2/competitions/PD/teams"
    url_clasificacion = "https://api.football-data.org/v2/competitions/PD/standings"

    ## parametros de la cabecera
    headers = {
    "X-Auth-Token": "12f38ea0c0324913b9c2915ca026813d",
    "Accept": "application/json"
    }

    ## obtenemos la web
    response = requests.get(url_equipos, headers=headers)

    ## guardamos la respueta de la api en un json
    equipos = response.json()

    ## obtenemos el total de quipos
    total = int(equipos["count"])

    ## iniciamos el listado de equipos
    nombres = {}

    ## recorremos los diferentes equipos del json
    for i in range(total):
        ## quitamos tildes
        nombre = unidecode.unidecode(equipos["teams"][i]["shortName"])

        ## cambiamos a mano tres nombres que no coinciden con la realidad
        if nombre == "Girona FC":
            nombre = "Girona"
        if nombre == "Club Atletico":
            nombre = "Atletico Madrid"
        if nombre == "Athletic Club":
            nombre = "Athletic Bilbao"

        ## asignamos el nombre en su sitio
        nombres[equipos["teams"][i]["id"]] = nombre

    ## hacemos la peticion de clasificaciones a la api
    response = requests.get(url_clasificacion, headers=headers)

    ## guardamos la respueta de la api en un json
    clasificaciones = response.json()

    ## creamos el dataframe
    df = pd.DataFrame()

    ## recorremos los diferentes equipos del json
    for i in range(total):
        ## creamos un dataframe con cada linea
        data = pd.DataFrame([[
            clasificaciones["standings"][0]["table"][i]["position"]
            #,clasificaciones["standings"][0]["table"][i]["team"]["id"]
            ,nombres[clasificaciones["standings"][0]["table"][i]["team"]["id"]]
            ,clasificaciones["standings"][0]["table"][i]["playedGames"]
            ,clasificaciones["standings"][0]["table"][i]["won"]
            ,clasificaciones["standings"][0]["table"][i]["draw"]
            ,clasificaciones["standings"][0]["table"][i]["lost"]
            ,clasificaciones["standings"][0]["table"][i]["points"]
            ,clasificaciones["standings"][0]["table"][i]["goalsFor"]
            ,clasificaciones["standings"][0]["table"][i]["goalsAgainst"]
            ,clasificaciones["standings"][0]["table"][i]["goalDifference"]
            ]]
            ,columns=["posicion","equipo","partidos","victorias","empates","derrotas","puntos","golesafavor","golesencontra","diferencia"]
        )

        ## anexamos la nueva linea al dataframe
        df = df.append(data, ignore_index=True)

    ## devolvemos el dataframe
    return df

## eof
