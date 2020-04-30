# -*- coding: utf-8 -*-
__version__ = "0.04"
"""
Source : https://github.com/izneo-get/lizzie-get

"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import re
import os
import sys 
import html
import argparse
import configparser
import shutil
import time
from bs4 import BeautifulSoup
import json
import urllib.parse


def requests_retry_session(
    retries=3,
    backoff_factor=1,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """Permet de gérer les cas simples de problèmes de connexions.
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def choose_book():
    """Permet de choisir un livre parmi ceux disponibles dans la session.
    """
    r = requests_retry_session(session=s).get(my_books_url, cookies=s.cookies, allow_redirects=True)
    html_one_line = r.text.replace("\n", "").replace("\r", "")
    soup = BeautifulSoup(html_one_line, features="html.parser")
    index = 1
    books_url = {}
    books_title = {}
    books_key = {}
    for div in soup.find_all("div", class_="ebook_infos"):
        title = div.find("p", class_="title")
        title = title.text.strip() if title else 'Titre inconnu'
        authors = div.find("p", class_="authors")
        authors = authors.text.strip() if authors else 'Auteur inconnu'
        url = div.find("a", class_="btn")
        book_id = re.findall(r"getPlaylist\('(.*)/(\d+)/(\d+)(.*)'", url.attrs["onclick"])
        if book_id:
            book_id = book_id[0]
            book_key = ''
            books_url[str(index)] = str(book_id[1]) + '/' + str(book_id[2])
        else:
            book_id = re.findall(r"(\w+)\('(.*)/(\d+)/(\d+)(.*)'", url.attrs["onclick"])[0]
            book_key = str(book_id[0]).replace('_', '-')
            books_url[str(index)] = str(book_id[2]) + '/' + str(book_id[3])
        books_title[str(index)] = f"{authors} - {title}"
        books_key[str(index)] = book_key
        print(f"[{index}] {authors} - {title}")
        index = index + 1

    if len(books_title) == 0:
        print("Aucun livre trouvé dans cette session. Vérifiez votre identifiant de session...")
        exit(0)
        
    choice = 'none'
    while choice not in books_url and choice.lower() != 'q':
        choice = input("Quel livre souhaitez-vous télécharger ('q' pour quitter) ? ")
        if choice.lower() == 'q':
            exit()
        else:
            if choice not in books_url:
                print("Pas de livre ayant ce numéro...")
    print(books_title[choice])
    return books_url[choice] + "?mode=new" + books_key[choice]


def download_file(url, name=''):
    """Permet de télécharger le fichier qui se trouve à une URL et le sauvegarde sur le disque.

    Parameters
    ----------
    url : str
        L'URL du fichier à télécharger.
    name : str (optional)
        Le nom à utiliser pour la sauvegarde. Si non renseigné, le nom du fichier original sera utilisé.
    """
    if not name:
        name = re.findall('filePath=([^"]+)', url)[0]
        name = urllib.parse.unquote(name)
        name = re.sub(r'[/\\<>:"|\?\*]', '_', name)
    store_path = output_folder + '/' + name

    if overwrite == False and os.path.exists(store_path) == True:
        print(f"\"{store_path}\" existe déjà, on passe.")
        return False

    headers = {
        'User-Agent': user_agent,
        # 'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
        # 'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Range': 'bytes=0-',
        'Connection': 'keep-alive',
        'Referer': my_books_url,
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    r = requests_retry_session(session=s).get(url, cookies=s.cookies, headers=headers, allow_redirects=True)
    open(store_path, "wb").write(r.content)

    # my_file = open(store_path, 'wb')
    # resp = requests.get(url, stream=True, headers=headers, cookies=cookies, allow_redirects=False)
    # if resp.status_code != 200:
    #     print('not 200!')
    #     print(resp)
    #     print(url)
    # for chunk in resp:
    #     my_file.write(chunk)
    #     my_file.flush()
    return True


def download_book(book_id):
    """Permet de télécharger tout un livre.
    
    Parameters
    ----------
    book_id : str
        L'identifiant du livre à télécharger.
    """
    url = listen_book_url + book_id

    headers = {
        'User-Agent': user_agent,
        # 'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
        # 'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': my_books_url,
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    r = requests_retry_session(session=s).get(url, cookies=s.cookies, headers=headers, allow_redirects=True)

    res = json.loads(r.text)
    
    book_id_clean = book_id.split('?')[0]
    files = re.findall(listen_book_url + book_id_clean + r'\?filePath=([^"]+)', res['html'])
    for f in files:
        print(f"Téléchargement de {f}")
        url = listen_book_url + book_id_clean + '?filePath=' + f
        is_downloaded = download_file(url)
        if is_downloaded:
            print(f"Pause de {pause} secondes")
            time.sleep(pause)
    
    



if __name__ == "__main__":
    cfduid = ""
    session_id = ""
    my_books_url = "https://abonnement.lizzie.audio/my-books"
    listen_book_url = "https://abonnement.lizzie.audio/listen-book/"
    root_path = "https://www.izneo.com/"

    default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'

    # Parse des arguments passés en ligne de commande.
    parser = argparse.ArgumentParser(
    description="""Script pour sauvegarder un livre audio depuis son compte Lizzie."""
    )
    parser.add_argument(
        "--session-id", "-s", type=str, default=None, help="L'identifiant de session (à récupérer dans les cookies)"
    )
    parser.add_argument(
        "--user-agent", "-u", type=str, default=None, help="Le User-Agent à utiliser pour se faire passer pour un navigateur"
    )
    parser.add_argument(
        "--output-folder", "-o", type=str, default=None, help="Répertoire racine de téléchargement"
    )
    parser.add_argument(
        "--config", type=str, default=None, help="Fichier de configuration"
    )
    parser.add_argument(
        "--pause", '-p', type=str, default=None, help="Pause (en secondes) entre chaque fichier"
    )
    parser.add_argument(
        "--overwrite", '-w', default=False, action='store_true', help="Re-télécharge et écrase les fichiers déjà existants"
    )
    args = parser.parse_args()

    # Lecture de la config.
    config = configparser.RawConfigParser()
    if args.config:
        config_name = args.config
    else:
        config_name = re.sub(r"\.exe$", ".cfg", re.sub(r"\.py$", ".cfg", os.path.basename(sys.argv[0])))
    config.read(config_name)

    def get_param_or_default(
        config, param_name, default_value, cli_value=None
    ):
        if cli_value is None:
            return (
                config.get("DEFAULT", param_name)
                if config.has_option("DEFAULT", param_name)
                else default_value
            )
        else:
            return cli_value

    output_folder = get_param_or_default(config, "output_folder", os.path.dirname(os.path.abspath(sys.argv[0])) + "/DOWNLOADS", args.output_folder)
    if not os.path.exists(output_folder): os.mkdir(output_folder)

    user_agent = get_param_or_default(config, "user_agent", default_user_agent, args.user_agent)

    session_id = get_param_or_default(config, "session_id", "", args.session_id)
    while not session_id and session_id.lower() != 'q':
        session_id = input("Identifiant de session ('q' pour quitter) : ")
    if session_id.lower() == 'q':
        exit()

    pause = int(get_param_or_default(config, "pause", "60", args.pause))

    overwrite = args.overwrite

    # Création d'une session et création du cookie.
    s = requests.Session()
    cookie_obj = requests.cookies.create_cookie(domain='abonnement.lizzie.audio', name='SESS', value=session_id)
    s.cookies.set_cookie(cookie_obj)
    

    # Choix du livre.
    book_url = choose_book()

    # Téléchargement du livre.
    download_book(book_url)
 