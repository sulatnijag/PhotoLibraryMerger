# !/usr/bin/python
import subprocess, os
from datetime import datetime
import multiprocessing
import timeit
import logging



class PLMerger:
    img_src_dir = None
    img_tgt_dir = None
    cpu_count = None
    supported_files = None

    def __init__(self, img_tgt_dir, img_src_dir):
        self.img_src_dir = img_src_dir
        self.img_tgt_dir = img_tgt_dir
        self.cpu_count = multiprocessing.cpu_count()
        self.supported_files = set()


    def getEXIF(self, filename):
        md = dict()
        output = subprocess.check_output('exiftool "' + filename + '"', shell=True)
        for ln in output.splitlines():
            k, v = ln.split(b':', 1)
            k = str(k.strip(), 'utf-8')
            v = str(v.strip(), 'utf-8')
            md[k] = v
        return (md['File Type'], md['File Name'], md['Directory'], md['File Size'], md['File Modification Date/Time'], md['File Type Extension'])



    def worker(self, f_path):
        try:
            f_type, f_name, f_dir, f_size, f_mod, f_ext = self.getEXIF(f_path)

            self.supported_files.add(f_type)


        except Exception:
            print("Unknown image format :" + f_path)
            pass




    def run(self):

        multiprocessing.log_to_stderr()
        logger = multiprocessing.get_logger()
        logger.setLevel(logging.WARNING)


        for src in self.img_src_dir:
            for root, dirs, files in os.walk(src):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files[:] = [f for f in files if not f.startswith('.')]

                for f in files:
                    p = os.path.join(root, f)
                    self.worker(p)

        print(self.supported_files)




def main():
    print("PhotoLibraryMerger started")
    start = timeit.default_timer()

    img_src_dir = ['/Volumes/Data/Pictures/Photos Library 2.photoslibrary/Masters/',
                   '/Volumes/Data/Pictures/Photos Library.photoslibrary/Masters/',
                   '/Volumes/Data/Pictures/GoPro/']
    img_src_dir = ['/Volumes/My Passport for Mac/Jag_2016/Chrise in Swiss/',
                   '/Volumes/My Passport for Mac/FAT_BUFFALO/Pictures/',
                   '/Volumes/My Passport for Mac/FAT_BUFFALO/Nepal_Pics/',
                   '/Volumes/My Passport for Mac/FAT_BUFFALO/macBook Backup/Italy/',
                   '/Volumes/My Passport for Mac/FAT_BUFFALO/macBook Backup/Iphone4/',
                  ]

    img_tgt_dir = '/Volumes/MAC ESS/Photos'

    # Test
    img_src_dir = ['/Volumes/MAC ESS/']
    #img_tgt_dir = '/Users/jag/git_repo/PhotoLibraryMerger/target'
    plm = PLMerger(img_tgt_dir, img_src_dir)
    plm.run()



    stop = timeit.default_timer()

    print('Time: ', stop - start)
    print("Program completed")



if __name__ == "__main__":
    main()

