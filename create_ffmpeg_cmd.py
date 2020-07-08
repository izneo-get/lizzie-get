# -*- coding: utf-8 -*-
__version__ = "0.03"
"""
Source : https://github.com/izneo-get/lizzie-get

Permet de créer les lignes de commande à exécuter pour fusionner les fichiers Lizzie récupérés avec l'application Android.
Nécessite FFmpeg.
"""
import os
import sys
import glob
import eyed3
import re 

if __name__ == "__main__":

    folder = sys.argv[1] if len(sys.argv) > 1 else '.'

    output_template = sys.argv[2] if len(sys.argv) > 2 else "{album}_{id}_{titre}"
    
    list_dir = glob.glob(folder + '/*.v3.exo')
    tuple_dir = []
    for f in list_dir:
        pattern = re.compile(r'(.*?)(\d+)\.(\d+)\.(\d+)\.v3\.exo')
        parts = pattern.fullmatch(f)
        key_order = ('00000000000000' + parts[2])[-14:] + ('00000000000000' + parts[3])[-14:] + ('00000000000000' + parts[4])[-14:]
        tuple_dir.append( (f, key_order) )

    list_dir = sorted(tuple_dir, key=lambda tuple_dir: tuple_dir[1])
    list_chapters = {}
    for (f, tmp) in list_dir:
        base_name = os.path.basename(f)
        chapter = base_name.split('.')[0]
        if chapter not in list_chapters:
            list_chapters[chapter] = []
        list_chapters[chapter].append(f)

    eyed3.log.setLevel("ERROR")
    for c in list_chapters:
        audiofile = eyed3.load(list_chapters[c][0])
        album_name = audiofile.tag.album if audiofile.tag and audiofile.tag.album else ""
        file_id = ('000' + c)[-3:]
        # chapter_name = audiofile.tag.title if audiofile.tag.title else (audiofile.tag.album + '_' + c if audiofile.tag.album else c)
        chapter_name = audiofile.tag.title if audiofile.tag and audiofile.tag.title else ''
        file_name = output_template
        file_name = file_name.replace('{album}', album_name)
        file_name = file_name.replace('{a}', album_name)
        file_name = file_name.replace('{id}', file_id)
        file_name = file_name.replace('{i}', file_id)
        file_name = file_name.replace('{titre}', chapter_name)
        file_name = file_name.replace('{t}', chapter_name)
        # file_name = album_name + '_' + file_id + '_' + chapter_name
        all_parts = '|'.join(list_chapters[c])
        print(f"ffmpeg -i \"concat:{all_parts}\" -c copy \"{file_name}.mp3\" && ^")
    print("echo Done!")
