import tweepy, pandas as pd
from datetime import date, datetime, timedelta

def devuelveRelevancia(hashtags):
    ## nuestros credenciales de la aplicacion twitter
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    ## creamos los objetos para consultar twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    ## calculamos el lunes de esta semana
    hoy = datetime.now()
    lunes = (hoy + timedelta(days=-hoy.weekday())).strftime("%Y-%m-%d")

    ## creamos el dataframe
    df = pd.DataFrame()

    ## recorremos todos los hashtags de los equipos
    for hashtag in hashtags:
        total = 0
        for tweet in tweepy.Cursor(api.search,
                                q="#LaLiga && #" + hashtag,
                                count=2, # limitamos para que no exceda el tiempo de ejecucion
                                lang="es",
                                since=lunes # desde el lunes de esta semana
                                ).items():
            ## actualizamos el contador
            total = total + 1
            if total > 1000:
                break

        ## creamos un dataframe con cada linea
        data = pd.DataFrame([[
            hashtag, total
            ]]
            ,columns=["hashtag","tweets"]
        )

        ## anexamos la nueva linea al dataframe
        df = df.append(data, ignore_index=True)

    ## devolvemos el dataframe
    return df

## eof
