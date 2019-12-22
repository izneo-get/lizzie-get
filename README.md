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


## Installation
### Prérequis
- Python 3.7+ (non testé avec les versions précédentes)
- pip
- Librairies SSL

#### Sous Windows
##### Python
Allez sur ce site :  
https://www.python.org/downloads/windows/  
et suivez les instructions d'installation de Python 3.

##### Pip
- Téléchargez [get-pip.py](https://bootstrap.pypa.io/get-pip.py) dans un répertoire.
- Ouvrez une ligne de commande et mettez vous dans ce répertoire.
- Entrez la commande suivante :  
```
python get-pip.py
```
- Voilà ! Pip est installé !
- Vous pouvez vérifier en tapant la commande :  
```
pip -v
```

##### Librairies SSL
- Vous pouvez essayer de les installer avec la commande :  
```
pip install pyopenssl
```
- Vous pouvez télécharger [OpenSSL pour Windows](http://gnuwin32.sourceforge.net/packages/openssl.htm). 


#### Sous Linux
Si vous êtes sous Linux, vous n'avez pas besoin de moi pour installer Python, Pip ou SSL...  

### Téléchargement
- Vous pouvez cloner le repo git :  
```
git clone https://github.com/izneo-get/lizzie-get.git
```
ou  
- Vous pouvez télécharger uniquement le binaire Windows (expérimental).  


### Configuration
(pour la version "script" uniquement)
```
pip install -r requirements.txt
```
