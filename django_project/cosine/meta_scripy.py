from bs4 import BeautifulSoup
import datetime
import urllib2
import requests
import datetime
import json
from pyjarowinkler import distance
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#sess = requests.Session()
#adapter = requests.adapters.HTTPAdapter(max_retries=20)
#sess.mount('http://',adapter)

class eat_spots:
	info=False
	name=""
	category=""
	room_delievery=False
	start=[]
	end=[]
	url=""

def eat_spots_dict(obj):
    return obj.__dict__

def get_start(date):
	i=0
	list=[]
	while(True):
		if date[i]==" ":
			list[0]=int(date[i:])
			if date[i+1]=="A":
				list[1]="AM"
				break
			else:
				list[1]="PM"
				break
		if date[i]=="A":
			list[0]=int(date[i:])
			list[1]="AM"
			break
		if date[i]=="P":
			list[0]=int(date[i:])
			list[1]="PM"
			break
	i=i+1
	return list



def get_eat_spots():
	list=[]
	spots=['Amul parlour','Arabian Nights',"Baskin Robbins","Billoos","Bimola Sweets","Carlos","Dreamland","Eggies","Flavour","Greenland","Heritage","Sahara","Subway","Super-Duper","Tikka"]
	headers = {'Accept-Encoding': 'identity'}
	r = requests.get('http://wiki.metakgp.org/w/Category:Food_and_Beverages', headers=headers)
	soup = BeautifulSoup(r.text,"html.parser")
	for item in spots:
	 for link in soup.findAll('a'):
	  if link.string== item:
	  	temp=eat_spots()
	  	temp.start=[]
	  	temp.end=[]
		l="http://wiki.metakgp.org"+link.get('href')
		headers = {'Accept-Encoding': 'identity'}
		html = requests.get(l, headers=headers)
		
		
		soup1=BeautifulSoup(html.text,"html.parser")
		table = soup1.find( "table", {"class":"infobox vcard"} )
		for row in table.findAll("tr"):
   			lis=[]
   			lis=''.join(row.findAll(text=True)).split("\n")
   			temp.name=item
   			if lis[0]=='Category':
   				temp.category=lis[1]
   			if lis[0]=='Room Delivery':
   				if lis[1]=='Yes':
   					temp.room_delievery=True
   			if lis[0]=='Timings':
   				if lis[1]!="":
   					#print "reached here"
   					#print lis[1]
   					i=0
   					while(True):
   						if lis[1][i]==" ":
   							if lis[1][i+1]=="A" or lis[1][i+1]=="P":
   								temp.start.append(lis[1][:i].strip())
   								temp.start.append((lis[1][i+1]+"M").strip())
   								break
   						if lis[1][i]=="A":
   							temp.start.append(lis[1][:i].strip())
   							temp.start.append("AM")
   							break
   						if lis[1][i]=="P":
   							temp.start.append(lis[1][:i].strip())
   							temp.start.append("PM")
   							break
   						i=i+1
   					p=[]
   					p=lis[1].strip().split("[")
   					i=len(p[0])-1
   					while(True):
   						if p[0][i]=="P" or p[0][i]=="A":
   							if p[0][i-1]==" ":
   								j=i-2
   								a=""
   								while(True):
   									if p[0][j]==" ":
   										break
   									a=p[0][j]+a
   									j=j-1
   								temp.end.append(a.strip())
   								temp.end.append(p[0][i]+"M")
   								break
   							else:
   								j=i-1
   								a=""
   								while(True):
   									if p[0][j]==" ":
   										break
   									a=p[0][j]+a
   									j=j-1
   								temp.end.append(a.strip())
   								temp.end.append(p[0][i]+"M")
   								break
   						i=i-1
   			temp.url=l
   			temp.info=True
   		list.append(temp)
   	 #print "done for"+ item
   	rem_spots=["Ashim's Food Canteen","Cathleen night canteen","Dominos","Hot & Spick","Hot Bite","MFS Canteen","PAN Loop Fast Food Center","Sam D","SN Night Canteen"]
   	for item in rem_spots:
   		for link in soup.findAll('a',text=item):
   			l="http://wiki.metakgp.org"+link.get('href')
   	        temp=eat_spots()
   	        temp.name=item;
   	        temp.url=l
   	        list.append(temp)
   	        #print "done for" +item
   	return list 

last_updated = datetime.datetime.now()

def scrape_for_data():
	try:
		f = open("date.txt","r")
		print "here"
		for line in f.readlines():
			last_updated_string = line # the only line
		#print last_updated_string,"here2"
		last_updated = datetime.datetime.strptime(last_updated_string, '%Y-%m-%dT%H:%M:%SZ')

	except:
		print "here1"
		last_updated = None
	if last_updated == None or ((datetime.datetime.now()-last_updated).seconds/60.0 >= 30.0) or  (datetime.datetime.now()-last_updated).seconds()/60.0 <0 :
		#scrape for new data
		list = get_eat_spots
		f1 = open("date.txt","w")
		f1.write(str(datetime.datetime.now().isoformat()))
        
def getjson():   		
    list=[]
    list=get_eat_spots()
    print "Scraped data"
    print json.dumps(list,default= eat_spots_dict).replace('\"','')
    #json.dump(','.join(host_list.keys()).replace('\"',''), fp)
    return json.dumps(list,default = eat_spots_dict).replace('\"','')

class HowTo:
	name=""
	url=""

def how_to():
	list=[]
	headers = {'Accept-Encoding': 'identity'}
	r = requests.get('https://wiki.metakgp.org/w/List_of_how-tos', headers=headers)
	soup = BeautifulSoup(r.text,"html.parser")
	for link in soup.findAll('a',text=True):
		if link.contents[0][:6]=='How to':
			temp=HowTo()
			temp.name=link.contents[0]
			temp.url='https://wiki.metakgp.org'+link.get('href')
			list.append(temp)
	return list

def get_how_to(s):
	list=[]
	list=how_to()
	sim=0
	temp=HowTo()
	for item in list:
		tfidf_vectorizer=TfidfVectorizer(analyzer="char")
		documents=(s,item.name)
		tfidf_matrix=tfidf_vectorizer.fit_transform(documents)
		cs=cosine_similarity(tfidf_matrix[0:1],tfidf_matrix)
		if cs[0][1]>sim:
			sim=cs[0][1]
			temp=item
	return json.dumps(temp.__dict__)
