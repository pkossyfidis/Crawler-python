#Κωνσταντινος Παπαγεωργιαδης 2881
#Παναγιωτης Κοσσυφιδης 2928


import urllib.request 
import re
from bs4 import BeautifulSoup
import requests
from urllib.request import Request
from queue import Queue
import threading
import time
import string
import math




def Crawler():
        global index

        index=index+1
        #print(threading.current_thread().name,worker)
        r=requests.get(urlLinks[index-1])
        if r.status_code==200  :
            req=Request(urlLinks[index-1])
            html = urllib.request.urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(html,'html.parser')
            text = soup.find('body')
            for link in text.find_all('a',href=True):
                if len(link['href'])>0  and len(urlLinks)<=numberOfUrls and link['href'] not in urlLinks:
                    if link['href'][0]=='#':
                        pass
                    elif link['href'][0]=='h' :
                        urlLinks.append(link['href'])
            article=''
            urlName=soup.title.string
            
            article = article + ' ' +str(urlName)
            for i in text.findAll('p'):
                article = article + ' ' +  i.text  #append the content of each paragraph in the article variable
            article=re.sub('[!@#$%^&-+=*<>?/:;}{.,|_]','',article)
            article=article.lower()
            article=article.split()
            #print(urlLinks[index-1])
            if index <=numberOfUrls:
                indexer(urlName,article)
    



def indexer(urlName , article):
    global timesCalled
    my_dict=dict()
    for word in article:
        if word in my_dict.keys():
            c=my_dict.get(word)
            c=c+1
            my_dict.update({word:c})
        else:
            my_dict.update({word:1})
    
    for word in my_dict.keys():
        if word in details:
            number=my_dict.get(word)
            urlAndTimes=details.get(word)
            number2=urlAndTimes[-1]
            total=number+number2
            urlAndTimes.pop(-1)
            urlAndTimes.append(urlName)
            urlAndTimes.append(number)
            urlAndTimes.append(total)
            details.update({word:urlAndTimes})
            inHowManyUrls=Ni.get(word)+1
            Ni.update({word:inHowManyUrls})
            total=0
        else:
            number=my_dict.get(word)
            urlAndTimes=[urlName,number]
            urlAndTimes.append(number)
            details.update({word:urlAndTimes})
            Ni.update({word:1})
    maxOrosDoc(urlName,details)
    findTF(details,urlName)
    findIDf(details)
    weightOfDoc(urlName) 
    ldScore(urlName)
    if index==numberOfUrls and timesCalled==0:
        timesCalled=timesCalled+1
        queryfunc(urlName)


def maxOrosDoc(urlName,details):
   
    maxOros=-1  
    for word in details: #poses fores emfanizete o pio suxnos oros
        if urlName in details.get(word):
            k1=details.get(word)
            p1=k1.index(urlName)
            p1=p1+1
            if(k1[p1]>maxOros):
                maxOros=k1[p1]
                wordOros=urlName
    maxW.update({wordOros:maxOros})




def findTF(details,urlName):
    for word in details:
        divisionT=[]
        if urlName in details.get(word):
            k=details.get(word)
            p=k.index(urlName)
            p=p+1
            divisionT.append(urlName)
            wmax=maxW.get(urlName)
            divisionT.append(k[p]/float(wmax)) #vriskoume to tf ths leksis word sto doc 
            tfD.update({word:divisionT})

def findIDf(details):
    for word in details:
        if word in Ni:
            i=Ni.get(word)
            fraction=numberOfUrls/float(i)
            logarithm=math.log(1+fraction)
            idfD.update({word:logarithm})



def weightOfDoc(urlName):
    global urlNames
    for word in tfD:
        wlist=[]
        if urlName in tfD.get(word):
            name=tfD.get(word)
            ind=name.index(urlName)+1
            tfi=name[ind]
            wd=tfi*idfD.get(word)
            wlist.append(urlName)
            wlist.append(wd)
            weightDoc.update({word:wlist})
            urlNames.append(urlName)



def queryfunc(urlName):
    #ni=ni
    q=input("Give Query: ")
    #q="stack"
    count=1
    maxC=-1
    for w in q.split():
        word=w.lower()
        wText=[]
        if word in query:
            count=query.get(word)+1
            query.update({word:count})
        else:
            query.update({word:count})
        if(count>maxC):
            maxC=count
        count=1
    tfiQ(maxC)
    iDFQ(numberOfUrls)
    weighOfQuery()
    


def tfiQ(maxC):
    for word in query:
        freq=query.get(word)
        tf=freq/float(maxC)
        tfQ.update({word:tf})


def iDFQ(numberOfUrls):
    for word in query:
        if word in Ni:
            total=Ni.get(word)
            idf=math.log(1+(numberOfUrls/float(total)))
            idfQ.update({word:idf})
        else:
            idfQ.update({word:0})



def weighOfQuery():
    wq=float()
    for word in query:
        idfq=idfQ.get(word)
        tfq=tfQ.get(word)
        wq=idfq*tfq
        wQword.update({word:wq})



def ldScore(urlName):
    ldcount=0
    for word in weightDoc:
        if urlName in weightDoc.get(word):
            dw=weightDoc.get(word)
            dw2=dw.index(urlName)+1
            ldcount=ldcount+pow(dw[dw2],2)
    ld.update({urlName:ldcount})



def similarity():
    for urlName in urlNames:
        simi=0
        lq=1
        Lqd=0
        for word in query:
            if urlName in weightDoc.get(word):
                dw=weightDoc.get(word)
                dw2=dw.index(urlName)+1
                simi=simi+wQword.get(word)*dw[dw2]
                ld2=ld.get(urlName)
                Lqd=(1/(lq*ld2))
        final=simi*Lqd
        similar.update({urlName:final})





def threader():
    while True:
        worker=q.get()
        Crawler()
        q.task_done()




Ni=dict()
details=dict()
maxW=dict()
tfD=dict()
idfD=dict()
weightDoc=dict()
query=dict()
tfQ=dict()
idfQ=dict()
wQword=dict()
ld=dict()
similar=dict()
urlAndTimes=[]
inHowManyUrls=0  
timesCalled=0  
urlNames=[]

print("Type:   1.Website  2.Number of Websites to crawl  3.Number of threads to use   (With spaces in between)")
timesCalled=0
url,numberOfUrls,threads= input().split()
numberOfUrls=int(numberOfUrls)
threads=int(threads)
index =0 
urlLinks=[]
urlLinks.append(url)
Crawler()
#print(index)

q=Queue()

for x in range (threads):
    t=threading.Thread(target=threader)
    t.daemon=True
    t.start()

start=time.time()

for worker in range(numberOfUrls):
    q.put(worker)

q.join()  

similarity()
for x in similar:
   print(x,":",similar.get(x))



