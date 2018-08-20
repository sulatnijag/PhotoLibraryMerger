# !/usr/bin/python
import subprocess, sys, os
import sqlite3
import pdb
from datetime import datetime
import shutil

def compare(a, b, encoding="utf8"):
    if isinstance(a, bytes):
        a = a.decode(encoding)
    if isinstance(b, bytes):
        b = b.decode(encoding)
    return a == b


def getEXIF(filename):
    md = dict()
    output = subprocess.check_output('exiftool "' + filename + '"', shell=True)
    for ln in output.splitlines():
        k, v = ln.split(b':', 1)
        k = str(k.strip(), 'utf-8')
        v = str(v.strip(), 'utf-8')
        md[k] = v
    return (md['File Type'], md['File Name'], md['Directory'], md['File Size'], md['File Modification Date/Time'], md['File Type Extension'])


def resolveConflict(source, target):
    isConflict = False
    nf_name = ''
    sf_type, sf_name, sf_dir, sf_size, sf_mod, sf_ext = getEXIF(source)
    tf_type, tf_name, tf_dir, tf_size, tf_mod, tf_ext = getEXIF(target)

    if(sf_type==tf_type and sf_size==tf_size and sf_mod==tf_mod):
        isConflict = False
        nf_name = sf_name
    else:
        isConflict = True
        s_name = sf_name.split('.', 1)
        sf_mod = sf_mod[11:19]
        nf_name = s_name[0] + '_' + sf_mod.replace(':','') + '.' + sf_ext

    return (isConflict, nf_name)


def insertSourceImg(conn, file_type, file_name, directory, file_size, file_mod_time, action):
    file_mod_time = datetime.strptime(file_mod_time[:19], '%Y:%m:%d %H:%M:%S')
    t = (file_type, file_name, directory, file_size, file_mod_time, action)
    conn.execute("INSERT INTO src_images(file_type, file_name, directory, file_size, file_mod_time, action) VALUES (?, ?, ?, ?, ?, ?)", t)
    conn.commit()



def initSource():
    try:
        conn.execute('DROP TABLE src_images')
    except:
        print("images table does not exist")

    conn.execute('''CREATE TABLE src_images (
                     image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     file_type text NOT NULL,
                     file_name text NOT NULL,
                     directory text NOT NULL,
                     file_size text NOT NULL,
                     file_mod_time DATETIME NOT NULL,
                     action int NOT NULL
                    )'''
                 )


#img_src_dir = ['/Volumes/Data/Pictures/Photos Library 2.photoslibrary/Masters/',
#               '/Volumes/Data/Pictures/Photos Library.photoslibrary/Masters/',
#               '/Volumes/Data/Pictures/GoPro/']


#img_tgt_dir = '/Volumes/MAC ESS/Photos'

img_src_dir = ['/Users/jag/git_repo/PhotoLibraryMerger/source_meta_updated/']
img_tgt_dir = '/Users/jag/git_repo/PhotoLibraryMerger/target'

conn = sqlite3.connect('/Users/jag/git_repo/PhotoLibraryMerger/PLM.db')

initSource()
#initTarget()


#for tgt in img_tgt_dir:
#    for root, dirs, files in os.walk(tgt, topdown=False):
#        for name in files:
#            f_type, f_name, f_dir, f_size, f_mod = getEXIF(os.path.join(root, name))


            #insertImg(conn, f_type, f_name, f_dir, f_size, f_mod, False)
#        for name in dirs:
#            print(os.path.join(root, name))


for src in img_src_dir:
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        for name in files:
            f_type, f_name, f_dir,  f_size, f_mod, f_ext = getEXIF(os.path.join(root, name))
            f_mod_time = datetime.strptime(f_mod[:19], '%Y:%m:%d %H:%M:%S')
            year = f_mod_time.strftime('%Y')
            month = f_mod_time.strftime('%m')
            day = f_mod_time.strftime('%d')

            tgt_path = os.path.join(img_tgt_dir, year, month)


            src_path = os.path.join(root, name)


            os.makedirs(tgt_path, exist_ok=True)

            tgt_file_path = os.path.join(tgt_path, name)

            if os.path.exists(tgt_file_path):
                isConflict, nf_name = resolveConflict(src_path, tgt_file_path)
                if isConflict:
                    print('Source ' + src_path + '  renamed to: ' + nf_name)
                    shutil.copy2(src_path, os.path.join(tgt_path, nf_name))
                    insertSourceImg(conn, f_type, f_name, f_dir, f_size, f_mod, 1)

                else:
                    print('Source ' + src_path + ' is already in : ' + tgt_path)
                    insertSourceImg(conn, f_type, f_name, f_dir, f_size, f_mod, 0)

            else:
                shutil.copy2(src_path, tgt_path)
                insertSourceImg(conn, f_type, f_name, f_dir, f_size, f_mod, 2)
                print('Source ' + src_path + ' copied to : ' + tgt_path)



conn.close()

print("Program completed")

