# techrocks42

Notre projet consiste en la récupération des informations sur les technologies utilisées par les entreprises pour leur site web.

Etape 1: récupérer les url des sites web de chacune des entreprises
* Ne prendre que le siège des entreprises (colonne siege = 1)
* Ne prendre que les entreprises de plus de 5 employés
* Recherche de la ville plus nom de l'entreprise

Utilisation de duckduckgo => renderer html
Utilisation de google comme moteur de recherche pas satisfaisant : rate limited

Parsing via beautifulsoup4 (python)
Récupération de toutes les réponses contenant des url, puis filtre sur les url sans sous chemin (domaine seul = exlcusion directe de tous les sites répertoriant les entreprises)
=> Bonne rapidité de récupération (pas besoin de scaling :-) sinon on utiliserait AWS Cli pour lancer différentes AMI amazon en parallèle)

Pas d'utilisation de Google Places (car pas le droit d'utiliser le résultat)

=> Résultat dans 10000_Scrapped.md

Phase 2:
=> Récupération de la "technologie web" utilisée dans le site web de l'entreprise
=> Utilisation de wappanalyze (très lent)
=> Split de 100 processus en parallèle (modulo100 du sirene) pour récupérer toutes les informations

Base de donnée: fichier csv avec en clef le siren, url, technologie en résultat (enfin j'espère).

Merci Fred !
