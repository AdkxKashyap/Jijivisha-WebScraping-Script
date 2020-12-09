from bs4 import BeautifulSoup
from selenium import webdriver
from Model.global_news_datamodel import GlobalNews
import requests
import re

class GetGlobalNews():
    def __init__(self):
        self.final_news_list=[]
    
    def get_soup(self,page):
       
        return BeautifulSoup(page.content,'html.parser')
    
    def check_elem(self,func_name,elem,elem_name):
         #For easy debugging
        if not elem:
            errMsg="In "+func_name+","+elem_name+" Not Found."
            raise Exception(errMsg)
        
    
    def data_from_worldometers(self):
        try:
            page=requests.get("https://www.worldometers.info/coronavirus/#countries")
            html_soup=self.get_soup(page)
            self.check_elem(self.data_from_worldometers.__name__,html_soup,"html_soup")
            news_div=html_soup.find("div",{"id":"news_block"})
            self.check_elem(self.data_from_worldometers.__name__,news_div,"news_div")
            news_content_list=news_div.find_all('div')[1].find_all(class_="news_post")
            self.check_elem(self.data_from_worldometers.__name__,news_content_list,"news_content_list")
            
            country_list=['india','usa','spain','italy','germany','france','china','uk','russia','brazil','canada','netherlands','belgium','switzerland',
                                'portugal','pakistan','nepal','bangladesh','israel','japan','saudi arabia','mexico','s.korea','uae','south africa','thailand'
                                ,'new zealand','afghanistan','taiwan','syria','australia,',"sri lanka"]
            for item in news_content_list:
                country=item.find("a").text.lower()
                if country in country_list:
                    news_content=item.find(class_="news_body").text
                    finale_data=re.sub("\[source\]","",news_content).strip()
                    news_dict={
                "source":"worldometer",
                "href":item.find(class_="news_source_a")["href"],
                "heading":"Covid Cases in:"+country.strip().title(),
                "content":finale_data
            }
                    self.final_news_list.append(news_dict)
            
           
        except Exception as errMsg:
            print(errMsg)    
    
    def data_from_bbc(self):
        
        try:
            page=requests.get("https://www.bbc.com/news/coronavirus")
            html_soup=self.get_soup(page)
            prefix="https://bbc.com"
            
            self.check_elem(self.data_from_bbc.__name__,html_soup,"html_soup")
            contents_main_div=html_soup.find("div",{"aria-labelledby":"featured-contents"})
            self.check_elem(self.data_from_bbc.__name__,contents_main_div,"contents_main_div")
            contents_one_div=contents_main_div.find(class_="gel-layout").find_all(class_="gel-layout__item")[0].find(class_="gs-c-promo-body")
            self.check_elem(self.data_from_bbc.__name__,contents_one_div,"contents_one_div")
            news_dict={
                "source":"bbc",
                "href":prefix+contents_one_div.find(class_="gs-c-promo-heading")['href'],
                "heading":contents_one_div.find(class_="gs-c-promo-heading").text.strip(),
                "body":contents_one_div.find(class_="gs-c-promo-summary").text.strip()
            }
            self.final_news_list.append(news_dict)
            
            contents_two_div=contents_main_div.find(class_="gel-layout").find_all(class_="gel-layout__item")[6].find(class_="gel-layout")
            self.check_elem(self.data_from_bbc.__name__,contents_two_div,"contents_two_div")
            contents_two_divs_list=contents_two_div.find_all(class_="gel-layout__item")
            
            count=0
            while(count<5):
                content=contents_two_divs_list[count].find(class_="gs-c-promo-body")
                news_dict={
                    "source":"bbc",
                    "href":prefix+content.find(class_="gs-c-promo-heading")["href"],
                    "heading":content.find(class_="gs-c-promo-heading").text.strip(),
                    "body":content.find(class_="gs-c-promo-summary").text.strip()
                }
                count=count+1
                self.final_news_list.append(news_dict)
            return self.final_news_list
        except Exception as errMsg:
            return errMsg
    
    def data_from_firstpost(self): 
        try:
            page=requests.get("https://www.firstpost.com/tag/coronavirus")
            html_soup=self.get_soup(page)
            self.check_elem(self.data_from_firstpost.__name__,html_soup,"html_soup")
            articles_list_div=html_soup.find(class_="articles-list")
            self.check_elem(self.data_from_firstpost.__name__,articles_list_div,"articles_list")
            articles_list_items=articles_list_div.find_all("li")
            self.check_elem(self.data_from_firstpost.__name__,articles_list_items,"articles_list")
             
            for  item in articles_list_items:
                news_dict={
                        "source":"firstpost",
                        "href":item.find(class_="list-item-link")['href'],
                        "heading":item.find(class_="list-title").text.strip(),
                        "content":item.find(class_="list-desc").text.strip()
                    } 
                self.final_news_list.append(news_dict)
        except Exception as errMsg:
            return errMsg
    
    def get_all_news(self):
         try:
            self.data_from_worldometers()
            self.data_from_firstpost()
            self.data_from_bbc()
         
            
            data=GlobalNews(
                news_data=self.final_news_list
            )
            data.save()
            return "World News Data Saved Successfully"
         except Exception as errMsg:
             return errMsg
        
        