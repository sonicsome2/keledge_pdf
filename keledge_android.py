import os
import json
import uuid
import argparse
import requests
import progressbar
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

parser= argparse.ArgumentParser()
parser.add_argument('-k','--key',dest='key',help="input the key")
parser.add_argument('-n','--name',dest='name',help="input books's name")
args = parser.parse_args()

if args.key == None or args.name == None:
    parser.print_help()
    os._exit(0)
    
# key先ascii然后再hex
hex_ascii_key = ''
for i in args.key:
    hex_ascii_key += f'{ord(i):x}'

# 加载json请求
try:
    with open('res.json', 'r') as f:
        data = json.load(f)
except Exception as e:
    print(e)

bookurls = data['Data']['SplitFileUrls']
uuid_str = uuid.uuid4()
tmp_dir = 'download_%s' % uuid_str
os.system(f'mkdir {tmp_dir}')

p = progressbar.ProgressBar()
for url in p(bookurls):
    page = bookurls.index(url)+1
    filename = f"x-{page}"
    r = requests.get(url = url,stream=True)
    with open(tmp_dir + '/' + filename+'.aes','wb') as f:
        f.write(r.content)
    os.system(f'openssl enc -d -aes-128-ecb -K {hex_ascii_key } -in {tmp_dir}/{filename}.aes -out {tmp_dir}/{filename}.pdf')
    os.system(f'rm {tmp_dir}/*.aes')

print("正在合成PDF文件.........")
for root, dirs, files in os.walk(tmp_dir):
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    files.sort(key=lambda x: int(x[x.rfind('-') + 1:][:-4]))
    file_list = [tmp_dir + '/' + file for file in files]
    merger = PdfFileMerger(strict=False)
    for pdf in file_list:
        merger.append(pdf)
    path = args.name + '.pdf'
    merger.write(path)
print("Success !!!!")
os.system(f'rm -rf {tmp_dir}')