# projet_3

## Objectif
L’objectif de ce projet est de choisir, mettre en place, et peupler une base de données à partir d’un jeu de données de l’open data, et d’implémenter une API vous permettant de requêter cette base de données.

## Pré-requis
**pip3 install -r requirements.txt**

## Data
J'ai choisi de prendre le jeu de données suivant:
- **https://www.kaggle.com/vardan95ghazaryan/top-250-football-transfers-from-2000-to-2018**

## Choix de la base de données
J'ai choisi d'utiliser **ElasticSearch** pour stocker le jeu de données.

## Lancement d'ElasticSearch
Tapez dans un terminal la commande suivante:

**docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.10.1**

## Lancement de Kibana (Optionnel)
Tapez dans un terminal la commande suivante:

**docker run -d --name kibana --link elasticsearch:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:7.10.2**
        
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
      "target_fields":["Name","Position","Age","Team_from","League_from","Team_to","League_to",
      "Season","Market_value","Transfer_fee"]
      }
    }
  ]
 }'**
 
Puis on crée l'index "projet_3" avec la ligne de commande suivante:

**curl -X PUT localhost:9200/projet_3 -H "Content-Type: application/json" --data-binary "@projet_3_analyzer.json"**

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

Pour vérifier que l'API est en ligne, vous pouvez aller à l'adresse suivante:

**http://0.0.0.0:5000/status**

et vous devez visualiser la réponse ci-dessous:

**{'On Air': 1}**

L'API possède plusieurs routes différentes que je vais détailler ci-dessous:

- **http://0.0.0.0:5000/all_transfers** pour avoir une visualisation d'une dizaine de résultats.

Pour les routes suivantes, il est important de connaitre le nom des différentes colonnes du jeu de données.
Nous avons les noms suivants:

- **Name**: Nom du joueur
- **Position**: Position sur le terrain (ex: Centre Forward, Attacking Midfield, Second Striker....)
- **Age**: Age du joueur
- **Team_from**: Nom de l'équipe avant le transfert
- **League_from**: Nom du championnat avant le transfert
- **Team_to**: Nom de l'équipe après le transfert
- **League_to**: Nom du championnat après le transfert
- **Season**: Date de la saison (ex: 2001 2002)
- **Market_value**: Prix estimatif du transfert
- **Transfer_fee**: Prix réel du transfert

- **http://0.0.0.0:5000/Name/query** pour faire une recherche spécifique pour le champs "Name" (ex: http://0.0.0.0:5000/Name/Zidane).

- **http://0.0.0.0:5000/Position/query** pour faire une recherche spécifique pour le champs "Position" (ex: "http://0.0.0.0:5000/Position/Centre").

- **http://0.0.0.0:5000/Age/query** pour faire une recherche spécifique pour le champs "Age" (ex: http://0.0.0.0:5000/Age/25).

- **http://0.0.0.0:5000/Team_from/query** pour faire une recherche spécifique pour le champs "Team_from" (ex: http://0.0.0.0:5000/Team_from/barcelona).

- **http://0.0.0.0:5000/League_from/query** pour faire une recherche spécifique pour le champs "League_from" (ex: http://0.0.0.0:5000/League_from/Premier).

- **http://0.0.0.0:5000/Team_to/query** pour faire une recherche spécifique pour le champs "Team_to" (ex: http://0.0.0.0:5000/Team_to/Ternana).

- **http://0.0.0.0:5000/League_to/query** pour faire une recherche spécifique pour le champs "League_to" (ex: http://0.0.0.0:5000/League_to/LaLiga).

- **http://0.0.0.0:5000/Season/query** pour faire une recherche spécifique pour le champs "Season" (ex: http://0.0.0.0:5000/Season/2000-2001).

- **http://0.0.0.0:5000/Transfer_fee/query** pour faire une recherche spécifique pour le champs "Transfer_fee" (ex: http://0.0.0.0:5000/Transfer_fee/26000000).

- **http://0.0.0.0:5000/Age/less/query** pour obtenir tous les résultats qui seront inférieurs à la valeur demandée pour le champs "Age" (ex: http://0.0.0.0:5000/Age/less/25).

- **http://0.0.0.0:5000/Transfer_fee/less/query** pour obtenir tous les résultats qui seront inférieurs à la valeur demandée pour le champs "Transfer_fee" (ex: http://0.0.0.0:5000/Transfer_fee/less/10000000).

- **http://0.0.0.0:5000/Age/more/query** pour obtenir tous les résultats qui seront supérieurs à la valeur demandée pour le champs "Age" (ex: http://0.0.0.0:5000/Age/more/30).

- **http://0.0.0.0:5000/Transfer_fee/more/query** pour obtenir tous les résultats qui seront supérieurs à la valeur demandée pour le champs "Transfer_fee" (ex: http://0.0.0.0:5000/Transfer_fee/more/25000000).

- **http://0.0.0.0:5000/Age/query1/query2** pour obtenir tous les résultats qui seront comppris entre les valeurs demandées pour le champs "Age" (ex: http://0.0.0.0:5000/Age/20/23).

- **http://0.0.0.0:5000/Transfer_fee/query1/query2** pour obtenir tous les résultats qui seront compris entre les valeurs demandées pour le champs "Transfer_fee" (ex: http://0.0.0.0:5000/Transfer_fee/23000000/25000000).

- **http://0.0.0.0:5000/Age/avg** pour obtenir la moyenne du champs "Age" (ex: http://0.0.0.0:5000/Age/avg).

- **http://0.0.0.0:5000/Transfer_fee/avg** pour obtenir la moyenne du champs "Transfer_fee" (ex: http://0.0.0.0:5000/Transfer_fee/avg).

- **http://0.0.0.0:5000/Age/min** pour obtenir le minimum du champs "Age" (ex: http://0.0.0.0:5000/Age/min).

- **http://0.0.0.0:5000/Transfer_fee/min** pour obtenir le minimum du champs "Transfer_fee" (ex: http://0.0.0.0:5000/Transfer_fee/min).

- **http://0.0.0.0:5000/Age/max** pour obtenir le maximum du champs "Age" (ex: http://0.0.0.0:5000/Age/max).

- **http://0.0.0.0:5000/Transfer_fee/max** pour obtenir le maximum du champs "Transfer_fee" (ex: http://0.0.0.0:5000/Transfer_fee/max).

- **http://0.0.0.0:5000/Transfers/stats** pour obtenir les statistiques des champs "Age" et "Transfer_fee" (ex: http://0.0.0.0:5000/Transfers/stats).

- **http://0.0.0.0:5000/Players** pour obtenir les noms des joueurs contenus dans la base de données (ex: http://0.0.0.0:5000/Players).

- **http://0.0.0.0:5000/Teams** pour obtenir les noms des différentes équipes (ex: http://0.0.0.0:5000/Teams).

- **http://0.0.0.0:5000/Leagues** pour obtenir les noms des différentes ligues (ex: http://0.0.0.0:5000/Leagues).
