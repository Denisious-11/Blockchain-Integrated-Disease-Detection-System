import ipfsApi
import urllib.request
from retry import retry
@retry(urllib.error.URLError, tries=1)

def download1(index, url,ex):
    filename = "%s.%s" %(index,ex)
    urllib.request.urlretrieve(url, filename)


def upload(fname):
    api = ipfsApi.Client('127.0.0.1', 5001)
    new_file = api.add(fname)
    print(new_file)
    hash1=new_file[0]['Hash']
    return hash1

def download(hash,filename):
    # api = ipfsApi.Client('127.0.0.1', 5001)
    # response=api.cat(hash)
    #api.get(hash)
    url="https://ipfs.io/ipfs/"+hash
    response=urllib.request.urlretrieve(url, filename)
    return response

if __name__=="__main__":
        
    # url="https://ipfs.io/ipfs/"+hash

    # download(1,url,'py')
    download1('QmcAF6U128Q9KLezRPZYA3y1mWS8wTGUHv51WSH7YxbJhj','g2.jpg')