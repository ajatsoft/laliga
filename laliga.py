import laliga_api, laliga_twitter, laliga_scraping, pandas as pd

## definimos el proceso principal
def main():
    ## obtenemos la clasificacion a traves de una api
    clasificacion = laliga_api.devuelveClasificacion()

    ## anyadimos el hashtag de cada equipo eliminando los espacios de su nombre
    clasificacion["hashtag"] = clasificacion.apply(lambda s: s["equipo"].replace(" ",""), axis=1)

    ## obtenemos los proximos partidos a traves de scraping
    probabilidades = laliga_scraping.devuelveProbabilidades()

    ## obtenemos el total de tweets sobre cada equipo en la semana actual a traves de twitter
    tweets = laliga_twitter.devuelveRelevancia(clasificacion["hashtag"].values)

    ## juntamos todo en un mismo DataFrame
    resultado = pd.merge(clasificacion, probabilidades, how='left', on="equipo")
    resultado = pd.merge(resultado, tweets, how='left', on="hashtag")

    ## exportamos el resultado a un fichero csv
    resultado.to_csv(path_or_buf="laliga.csv", index=False)

## lanzamos el proceso
main()

## eof
