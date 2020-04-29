from bs4 import BeautifulSoup
from Model.myth_busters_datamodel import MythBusters
import requests


class GetMythBusters():
    def __init__(self):
        self.final_myths_list=[]
    
    def get_soup(self,page):
        return BeautifulSoup(page.content,'html.parser')
    
    def check_elem(self,func_name,elem,elem_name):
         #For easy debugging
        if not elem:
            errMsg="In "+func_name+","+elem_name+" Not Found."
            raise Exception(errMsg)
        
    
    def data_from_who(self):
        try:
            page=requests.get("https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters")
            html_soup=self.get_soup(page)
            self.check_elem(self.data_from_who.__name__,html_soup,"html_soup")
            page_content_div=html_soup.find("div", {"id":"PageContent_C003_Col01"})
            self.check_elem(self.data_from_who.__name__,page_content_div,"page_content_div")
            page_contents=page_content_div.find_all(class_="sf-image thumb")
            
            for content in page_contents:
                src="https://www.who.int/"+content.find("img")["data-src"]
                self.final_myths_list.append(src)
           
        except Exception as err:
            return err
       
    def save_data(self):
        try:
          self.data_from_who()
          data=MythBusters(
              myth_busters_data=self.final_myths_list
          )
          data.save()
          return "Data Saved Successfully!"
        except Exception as err:
            return err