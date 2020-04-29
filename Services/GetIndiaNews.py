from bs4 import BeautifulSoup
from selenium import webdriver
from Model.india_latest_news_datamodel import IndiaNews
import requests
import re

class GetIndiaNews():
    def __init__(self):
        self.final_news_list=[]
    
    def get_soup(self,page):
       
        return BeautifulSoup(page.content,'html.parser')
    
    def check_elem(self,func_name,elem,elem_name):
         #For easy debugging
        if not elem:
            errMsg="In "+func_name+","+elem_name+" Not Found."
            raise Exception(errMsg)
    
    def data_from_worlometers(self):
        try:
            page=requests.get("https://www.worldometers.info/coronavirus/country/india/")
            html_soup=self.get_soup(page)
            self.check_elem(self.data_from_worlometers.__name__,html_soup,"html_soup")
            news_div=html_soup.find("div",{"id":"news_block"})
            self.check_elem(self.data_from_worlometers.__name__,news_div,"news_div")
            news_content=news_div.find_all('div')[1].find(class_="news_body").text
            self.check_elem(self.data_from_worlometers.__name__,news_content,"news_content")
            finale_data=re.sub("\[source\]","",news_content).strip()
            news_dict={
                "source":"worldometer",
                "href":"https://www.worldometers.info/coronavirus/country/india/",
                "heading":"Covid Cases in India.",
                "content":finale_data
            }
            self.final_news_list.append(news_dict)
        except Exception as errMsg:
            print(errMsg)
    
    def data_from_firstpost(self):
        try:
            page=requests.get('https://www.firstpost.com/tag/coronavirus')
           
            html_soup=self.get_soup(page)
            self.check_elem(self.data_from_firstpost.__name__,html_soup,"html_soup")
            article_lists=html_soup.find("ul",{"class":"articles-list"}).find_all('li')
            self.check_elem(self.data_from_firstpost.__name__,article_lists,"articles-list")
            
            for div in article_lists:
                category=div.find(class_="section-btn").text
                #check if category is india
                if(category=="India"):
                    news_dict={
                        "source":"firstpost",
                        "href":div.find(class_="list-item-link")['href'],
                        "heading":div.find(class_="list-title").text,
                        "content":div.find(class_="list-desc").text
                    }
                    self.final_news_list.append(news_dict)
            return self.final_news_list
        except Exception as errMsg:
            return errMsg
    
    def data_from_bbc(self):
        try:
            page=requests.get('https://www.bbc.com/news/world/asia/india')
            
            news_dict={}
            url_prefix="https://bbc.com"
            #For easy debugging
            errMsg="In "+"data from Bbc following is not found:"
            html_soup=self.get_soup(page)
            self.check_elem(self.data_from_bbc.__name__,html_soup,"html_soup")
            
            main_index_page=html_soup.find("div",{"id":"index-page"})
            self.check_elem(self.data_from_bbc.__name__,main_index_page,"main_index_page")
            
            main_res=main_index_page.find(class_="no-mpu")
            self.check_elem(self.data_from_bbc.__name__,main_res,"main_res")
            promo_body=main_res.find(class_='gs-c-promo-body--primary')
            self.check_elem(self.data_from_bbc.__name__,promo_body,"promo_body")
            
            promo_body_link=promo_body.find('a')
            self.check_elem(self.data_from_bbc.__name__,promo_body_link,"promo_body_link")
           
            news_dict={
                    'source':'bbc',
                    'href':url_prefix+promo_body_link['href'],
                    'heading':promo_body_link.find(class_='gs-c-promo-heading__title').text,
                    'content':promo_body.find(class_='gs-c-promo-summary').text
            }
            self.final_news_list.append(news_dict)
            
    
            covid_news_maindiv=main_index_page.find("div",{"aria-labelledby":"nw-c-Coronavirusoutbreak__title"})
            covid_news_contentdivs=covid_news_maindiv.find_all(class_="gel-layout")[1].find_all(class_="gel-layout__item")
            count=0
            while(count<3):
                    count=count+1
                    body=covid_news_contentdivs[count].find(class_='gs-c-promo').find(class_='gs-c-promo-body')
                    news_dict={
                        "source":"bbc",
                        "href":url_prefix+body.find('a')['href'],
                        "heading":body.find(class_="gs-c-promo-heading").find(class_="gs-c-promo-heading__title").text
                    
            }
                    self.final_news_list.append(news_dict)
            return self.final_news_list
        except Exception as errMsg:
            return errMsg
        
     
    def get_all_news(self):
         try:
            self.data_from_worlometers()
            self.data_from_bbc()
            self.data_from_firstpost()
            
            data=IndiaNews(
                news_data=self.final_news_list
            )
            data.save()
            return "Data Saved Successfully" 
         except Exception as errMsg:
             return errMsg