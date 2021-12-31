from PIL import Image
import pyautogui
from gc import disable
from flask import Flask
disable()

def Screenshot(name,Resolution=100): ##Create a screenshot *.png
    dir = "./Screencast"
    name = str(name)
    Photo = pyautogui.screenshot()
    Size = Photo.size
    Photo.save(dir+name+".png")
    if not (Resolution > 14):
        Photo = Image.open(dir+name+".png")
        Size = Photo.size
        Photo = Photo.resize((int(Size[0]/100*Resolution),int(Size[1]/100*Resolution)))
        Photo.save(dir+name+".png")
        Photo.close()
    return dir+name+".png"

def getImageInfo(Photo): #Get pixmap and Size
    Photo = Image.open(Photo)
    Map = Photo.load()
    Size = Photo.size
    Photo.close()
    return Map,Size

def DF(x, y): #Get distance between two numbers
    if x == y:
        return 0
    if x >= y:
        return x - y
    else:
        return y - x

def CS(c1,c2): #Can ignore that pixel
    rd=DF(c1[0],c2[0])
    gd=DF(c1[1],c2[1])
    bd=DF(c1[2],c2[2])
    if rd>7:
        return False
    elif gd>7:
        return False
    elif bd>7:
        return False
    if rd+gd+bd > 10:
        return False
    return True

def CTS(pixel,hex=False):
    s="."
    if hex == True:
        if pixel:
            return TH(pixel[0])+s+TH(pixel[1])+s+TH(pixel[2])
        else:
            return None
    else:
        if pixel:
            return str(pixel[0])+s+str(pixel[1])+s+str(pixel[2])
        else:
            return None

def TH(dn):
    dn = str(hex(dn))
    r = dn[2:len(dn)]
    return str(r)

def imageToString(img):
    disable()
    map,res = getImageInfo(img)
    CTP,d,lp,C = {},"",None,0
    print(str(res[0])+"x"+str(res[1]))
    for xl in range(res[0]):
        for yl in range(res[1]):
            p = map[xl,yl]
            if not(lp==None) and CS(lp,p):
                C+=1
            else:
                if not(C==0):
                    d+="*"+TH(C)
                    C=0
                ps = CTS(p,hex=False)
                lp = p
                if ps in CTP.keys():
                    d+="/"+CTP[ps]
                else:
                    CTP[ps] = TH(xl)+":"+TH(yl)
                    d+="/"+CTS(p,hex=True)
    if not(C==0):
        d+="*"+TH(C)
    d = d[1:len(d)]
    l = len(CTP)
    CTP,lp,map,res = None,None,None,None
    return d,l

def runserver():
    app = Flask(__name__)
    @app.route('/Screen', methods=['GET'])
    def result():
        try:
            s = Screenshot("screenshot",Resolution=14)
            data,dl = imageToString(s)
            print(f"{str(dl/1024)[0:5]} kb has been sent over the internet")
            return data
        except Exception as er:
            print(er)
            return ""
    app.run(host='127.0.0.1',port=8080,debug=False)

runserver()
