import os
user = os.environ["USER"]
directory_to_scan = "/home/%s/Downloads" % user
output_file_name = "hashes"
use_md5 = True
use_sha1 = True
extension_list = [".iso", ".tar", ".gz", ".tar.gz"]
