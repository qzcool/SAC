from modules.utils import *

# Download File Common Function
## 加入自主命名(根据列表)的功能
def download_file(url, path, local_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    shutil.move(local_filename,path+'/'+local_filename)