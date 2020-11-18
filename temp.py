import urllib3
import json
import time
import API

http = urllib3.PoolManager()
servertime = http.request('GET', 'https://api.kraken.com/0/public/Time') #Récupère le temps serveur

print(servertime.data)

assets = http.request('GET', 'https://api.kraken.com/0/public/AssetPairs') #Récupère TOUS les assets de la plateforme

#print(assets.data['result'])

res = assets.data
my_json = res.decode('utf8').replace("'", '"')
res = json.loads(my_json)
res2 = res["result"]

f = open("listOfTickers.txt", "w")
print("La liste des tickers sont les suivants : ")

for key in res2:
    f.write("%s\n" % key)
f.close()

f = open("listOfTickers.txt", "r")
print(f.read().replace('\n', ', '))
print("\nVous pouvez retrouver la liste dans le fichier listOfTickers.txt !")
print("\n")


def repeatedTickerRequest():
    starttime = time.time() #Démarre un chrono à l'heure actuelle
    average = 0.0
    api = API.API(key='a0BWIk6U52YdgMikKlbCFiMaP8O87kjdGWmSaWCi03PtTRHImYThdKau', secret='aOtvRUVC5R/yJbNC05WGQWXINHZVPVUmbF6CBrLhg+1AaAXltFGvoreBIUVJFTBOH8b1yE0iAgTfHIVLJDVVRA==')
    
    while True: #Boucle infinie
        print("tic")
        tickers = http.request('GET', 'https://api.kraken.com/0/public/Ticker?pair=BTCEUR') #Récupère spécifiquement la pair BTC/EUR
        res = tickers.data # On s'intéresse à la partie data de la requête, juste tickers renvoie une HTTPresponse
        my_json = res.decode('utf8').replace("'", '"') #On retouche le fichier en remplacer les ' par des " (plus lisible) et on le decode
        res = json.loads(my_json) #On le convertit en jsonn
        
        res2 = res["result"]["XXBTZEUR"]["c"][0] # On récupère le dernier trade fait sur cette paire
        
        
        f = open("Tickers_Of_BTCEUR.txt","a+")
        f.write(res2+"\n") #On écrit le dernier trade en fin de fichier
        f.close()
        
        f = open("Tickers_Of_BTCEUR.txt","r")
        listTicks = []
        for line in f:
            listTicks.append(line[:-1]) #On fait la moyenne de tous les ticks
            average += float(line)
            
        average /= len (listTicks)             
        print(listTicks)
        print("LA MOYENNE EST DE " + str(average))
        f.close()
        
        f = open("Averages.txt","a")
        f.write(str(average)+"\n") #La moyenne est enregistrée dans le fichier Averages.txt
        f.close()
        
        print(api.query_private('Balance')['result'])
        print(api.query_private('OpenOrders')['result'])
        if(api.query_private('OpenOrders')['result']['open'] == {}):
            print('ok')
        time.sleep(60.0 - ((time.time() - starttime) % 60.0)) #On attend 60 secondes avant de pouvoir recommencer
 
        

repeatedTickerRequest()
