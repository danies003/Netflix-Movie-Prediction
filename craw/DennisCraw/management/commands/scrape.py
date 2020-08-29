#!/usr/bin/env python
# coding: utf-8

# # DOE

# In[2]:
from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from DennisCraw.models import Job
import urllib.request as req
import pandas as pd
import bs4
class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    def handle(self, *args, **options):


    
    
       



        # # NSF

        # In[3]:




        url="https://www.nsf.gov/news/"
        request=req.Request(url, headers={"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")


        root=bs4.BeautifulSoup(data, "html.parser")
        links=root.find('div',class_="col-md-12 l-add__border")
        list1={'title':[],'href':[],'time':[]}
        for a in links.find_all("div", {"class":"media l-media"}):
            for b in a.find_all("div", {"class":"media-body"}):

                for c in b.find_all("span", {"class":"l-media__date" }):
                        list1['time'].append(c.get_text())

                for d in b.find_all("a"):
                        list1['title'].append(d.get_text())


                        if "https://" in d['href']:

                            list1['href'].append(d['href'])

                        else:
                            list1['href'].append("https://www.nsf.gov"+d['href'])




        NSF = pd.DataFrame(list1, columns=['time', 'title', 'href'])






        # # FAA 

        # In[4]:



        url="https://www.faa.gov/news/"
        request=req.Request(url, headers={"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")


        root=bs4.BeautifulSoup(data, "html.parser")
        links=root.find('article',class_="content")
        list1={'title':[],'href':[],'time':[]}
        for a in  links.find_all("div", {"class":"newsItem"}):   
            for p in a.find_all("p", {"class":"join"}):
                for small in p.find_all("small"):
                    for btag in small.find_all("b"):

                        list1['time'].append(btag.get_text())


            for h3 in a.find_all("h3"):
                   for atag in h3:

                        list1['title'].append(atag.get_text())


                        if "https://" in atag['href']:

                            list1['href'].append(atag['href'])

                        else:    

                            list1['href'].append("https://www.faa.gov"+atag['href'])




        FAA = pd.DataFrame(list1, columns=['time', 'title', 'href'])





        # # NIST

        # In[5]:



        url="https://www.nist.gov/news-events/news"
        request=req.Request(url, headers={"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")


        root=bs4.BeautifulSoup(data, "html.parser")
        links=root.find('div',class_="nist-block nist-block--news")
        list1={'title':[],'href':[],'time':[]}
        for a in  links.find_all("article", {"class":"nist-teaser"}):    
                for b in  a.find_all("div", {"class":"nist-teaser__content-wrapper"}): 
                    for time in b.find_all("time"):

                        list1['time'].append(time.get_text())

                    for title in b.find_all("span"):

                        list1['title'].append(title.get_text())

                    for p in b.find_all("a"):
                            if "https://" in p['href']:

                                list1['href'].append(p['href'])

                                print("")
                            else:    

                                list1['href'].append("https://www.nist.gov"+p['href'])
                                print("")


        NIST = pd.DataFrame(list1, columns=['time', 'title', 'href'])








        # # 建立各自panda dataframe  加上website 標籤

        # In[6]:



        NIST['website'] = 'NIST'


        FAA['website'] = 'FAA'


        NSF['website'] = 'NSF'




        # # 合成一個大的table 用時間排序

        # In[7]:


        merged_df = pd.concat([NIST, FAA, NSF])
        merged_df = merged_df[['time', 'website', 'title', 'href']]
        merged_df['time'] = pd.to_datetime(merged_df['time'])
        merged_df.set_index('time', drop=True, append=False, inplace=True, verify_integrity=False)
        merged_df=merged_df.sort_values(by=['time'], ascending=False)
        print(merged_df)


        # # 搜尋指定的website

        # In[8]:




        # In[34]:

        try:
                    # save in db
                    Job.objects.create(
                        title=merged_df['title'],
                        href=merged_df['href'],

                        time=merged_df['time']
                    )
                    print('%s added' % (title,))
        except:
                    print('%s already exists' % (title,))
        self.stdout.write( 'job complete' )



    # In[ ]:




