# lizzie-get
Ce script permet de récupérer un livre audio présent sur https://www.lizzie.audio dans la limite des capacités de notre compte existant.

Le but est de pouvoir écouter un livre audio sur un support non compatible avec les applications fournies par Lizzie. 
Il est évident que les livres audios ne doivent en aucun cas être conservés une fois l'écoute terminée ou lorsque votre abonnement ne vous permet plus de les écouter.


## Utilisation
### lizzie_get
Script pour sauvegarder un livre audio depuis son compte Lizzie.
**Utilisation**  
```
optional arguments:
  -h, --help            show this help message and exit
  --session-id SESSION_ID, -s SESSION_ID
                        L'identifiant de session (à récupérer dans les
                        cookies)
  --output-folder OUTPUT_FOLDER, -o OUTPUT_FOLDER
                        Répertoire racine de téléchargement

```

Exemple :  
Pour récupérer le livre dans un répertoire temporaire :  
```
python lizzie_get.py -s azertyuiop1234567890 -o "c:/temp/"
```

L'identifiant de session est créé lorsque vous vous connectez à votre compte Lizzie. 
Pour l'obtenir, identifiez vous sur https://abonnement.lizzie.audio et recherchez votre cookie "SESS" avec votre navigateur web.

#### Chrome  
Menu --> Plus d'outils --> Outils de développements  
Application / Storage / Cookies  
et recherchez le cookie "SESS" du comaine "abonnement.lizzie.audio".  


#### Firefox  
Menu --> Developpement web --> Inspecteur de stockage --> Cookies  
et recherchez le cookie "SESS" du comaine "abonnement.lizzie.audio".  
