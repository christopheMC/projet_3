# projet_3

## Objectif
L’objectif de ce projet est de choisir, mettre en place, et peupler une base de données à partir d’un jeu de données de l’open data, et d’implémenter une API vous permettant de requêter cette base de données.

## Data
J'ai choisi de prendre le jeu de données suivant:
- **https://www.kaggle.com/vardan95ghazaryan/top-250-football-transfers-from-2000-to-2018**

## Choix de la base de données
J'ai choisi d'utiliser **ElasticSearch** pour stocker le jeu de données.

## Lancement d'ElasticSearch
Tapez dans un terminal la commande suivante:

**docker run -d \
--name elasticsearch \
-p 9200:9200 \
-p 9300:9300 \
-e "discovery.type=single-node" \
elasticsearch:7.10.1**

## Lancement de Kibana (Optionnel)
Tapez dans un terminal la commande suivante:

**docker run -d \
        --name kibana \
        --link elasticsearch:elasticsearch \
        -p 5601:5601 docker.elastic.co/kibana/kibana:7.10.2**
        
Dans une fenêtre internet, vous aurez accès à l'interface Kibana à l'adresse URL suivante:

**http://localhost:5601**

## Création de l'index dans ES et peuplement de façon manuelle
### Création du pipeline
On crée le pipeline avec le nom des colonnes issues du jeu de données.

**curl -X PUT localhost:9200/_ingest/pipeline/projet_3_pipeline -H "Content-Type: application/json" -d '{
"processors": [
    {
      "csv" : {
      "field" :"csv_line",
      "target_fields":["name","position","age","team_from","league_from","team_to","league_to",
      "season","market_value","transfer_fee"]
      }
    }
  ]
 }'**
 
Puis on crée l'index "projet_3" avec la ligne de commande suivante:

**curl -X PUT localhost:9200/projet_3 \
-H "Content-Type: application/json" \
--data-binary "@projet_3_analyzer.json"**

### Nettoyage du jeu de données
Pour nettoyer le jeu de données, il suffit de lancer un programme python qui va créer un nouveau fichier .csv où on aura supprimé les headers et supprimé les caractères de ponctuation tels que les virgules, les guillemets....

**python3 transform.py**

### Peuplement de la base de données
J'ai crée un script pour transférer le fichier csv nettoyé vers la base de données.
Il suffit de taper la commande suivante dans le terminal:

**./insert.sh**

## Création de l'index dans ES et peuplement de façon automatique
On peut également faire les 3 opérations précédentes en lançant la commande suivante:

**python3 fill.py**

## API pour interrogation de la base de données
L'**API** a été créée sous **Flask**.
Pour la lancer, il faut taper la commande suivante:

**python3 api_projet_3.py**

L'URL, pour se connecter, est le suivant:

**http://0.0.0.0:5000/**

L'API possède plusieurs routes différentes que je vais détailler ci-dessous:
- **http://0.0.0.0:5000/projet_3/all** pour avoir une visualisation d'une dizaine de résultats.

Pour les routes suivantes, il est important de connaitre le nom des différentes colonnes du jeu de données.
Nous avons les noms suivants:

-**Name**: Nom du joueur
-**Position**: Position sur le terrain (ex: Centre Forward, Attacking Midfield, Second Striker....)
-**Age**: Age du joueur
-**Team_from**: Nom de l'équipe avant le transfert
-**League_from**: Nom du championnat avant le transfert
-**Team_to**: Nom de l'équipe après le transfert
-**League_to**: Nom du championnat après le transfert
-**Season**: Date de la saison (ex: 2001 2002)
-**Market_value**: Prix estimatif du transfert
-**Transfer_fee**: Prix réel du transfert

- **http://0.0.0.0:5000/projet_3/match/field/query** pour faire une recherche spécifique, on remplacera le champs "field" par un des noms de colonnes précédemment cité et le champs "query" par le nom ou la valeur que vous recherchez.

- **http://0.0.0.0:5000/projet_3/range/field/less/query** pour obtenir tous les résultats qui seront inférieurs à la valeur demandée, on remplacera le champs "field" par un des noms de colonnes numériques (age, season, market_value, transfer_fee) et le champs "query" par la valeur souhaitée.

- **http://0.0.0.0:5000/projet_3/range/field/more/query** pour obtenir tous les résultats qui seront supérieurs à la valeur demandée, on remplacera le champs "field" par un des noms de colonnes numériques (age, season, market_value, transfer_fee) et le champs "query" par la valeur souhaitée.

- **http://0.0.0.0:5000/projet_3/range/field/in/query1/query2** pour obtenir tous les résultats qui seront comppris entre les valeur demandées, on remplacera le champs "field" par un des noms de colonnes numériques (age, season, market_value, transfer_fee), le champs "query1" et le champs "query" par les valeurs souhaitées.

- **http://0.0.0.0:5000/projet_3/range/field/out/query1/query2** pour obtenir tous les résultats qui seront comppris en dehors des valeur demandées, on remplacera le champs "field" par un des noms de colonnes numériques (age, season, market_value, transfer_fee), le champs "query1" et le champs "query" par les valeurs souhaitées.

- **http://0.0.0.0:5000/projet_3/avg/field** pour obtenir la moyenne du champs "field" (age, market_value, transfer_fee) demandé.

- **http://0.0.0.0:5000/projet_3/min/field** pour obtenir le minimum du champs "field" (age, market_value, transfer_fee) demandé.

- **http://0.0.0.0:5000/projet_3/min/field** pour obtenir le maximum du champs "field" (age, market_value, transfer_fee) demandé.

- **http://0.0.0.0:5000/projet_3/sum/field** pour obtenir la somme du champs "field" (age, market_value, transfer_fee) demandé.

- **http://0.0.0.0:5000/projet_3/stats/field** pour obtenir les statistiques du champs "field" (age, market_value, transfer_fee) demandé.
