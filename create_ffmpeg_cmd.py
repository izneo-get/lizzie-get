# -*- coding: utf-8 -*-
__version__ = "0.01"
"""
Source : https://github.com/izneo-get/lizzie-get

Permet de créer les lignes de commande à exécuter pour fusionner les fichiers Lizzie récupérés avec l'application Android.
Nécessite FFmpeg.
"""
import os
import sys
import glob
import eyed3

if __name__ == "__main__":

    folder = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    list_dir = glob.glob(folder + '/*.v3.exo')
    list_dir = sorted(list_dir)
    list_chapters = {}
    for f in list_dir:
        base_name = os.path.basename(f)
        chapter = base_name.split('.')[0]
        if chapter not in list_chapters:
            list_chapters[chapter] = []
        list_chapters[chapter].append(f)

    eyed3.log.setLevel("ERROR")
    for c in list_chapters:
        audiofile = eyed3.load(list_chapters[c][0])
        # chapter_name = audiofile.tag.title if audiofile.tag.title else (audiofile.tag.album + '_' + c if audiofile.tag.album else c)
        chapter_name = audiofile.tag.album + '_' + ('000' + c)[-3:] if audiofile.tag.album else ('000' + c)[-3:]
        all_parts = '|'.join(list_chapters[c])
        print(f"ffmpeg -i \"concat:{all_parts}\" -c copy \"{chapter_name}.mp3\" && ^")
    print("echo Done!")
