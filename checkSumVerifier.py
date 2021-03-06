#!/usr/bin/python3
# Purpose of this project is to write a script that will run in the background
# on boot. Any items downloaded to Downloads (or another specified folder) will
# have various hashes made of them
# Dependencies watchdog
# Usage python checkSumVerifier


import time
import sys # for command line arguments
import hashlib # for preforming file hashes
from env import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileDownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        file_name, extension = os.path.splitext(event.src_path)
        print(event)
        if extension in extension_list and file_name != output_file_name:
            hash_md5 = hashlib.md5()
            hash_sha1 = hashlib.sha1()
            file_name += extension
            with open(output_file_name, "a+") as w:
                w.writelines(file_name + "\n")

                with open(file_name, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)

                    w.writelines("md5: " + hash_md5.hexdigest() + "\n")
                    del hash_md5

                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha1.update(chunk)

                    w.writelines("sha1: " + hash_sha1.hexdigest() + "\n")
                    del hash_sha1


if __name__ == "__main__":
    if len(sys.argv) > 0 and sys.argv[1] == '0':
        download_handler = FileDownloadHandler()
        observer = Observer()
        observer.schedule(download_handler, path=directory_to_scan, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        print("You need arguments this. will show help eventually once I make it")
