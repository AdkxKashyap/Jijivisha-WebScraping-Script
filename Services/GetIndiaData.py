from bs4 import BeautifulSoup
from selenium import webdriver
from Model.india_covid_datamodel import IndiaCovidData

class GetIndiaData():
    def __init__(self):
        try:
            self.driver=webdriver.Chrome('Assets/chromedriver')
            self.driver.get("https://covid19ind.zaoapp.net/")
            self.soup=BeautifulSoup(self.driver.page_source,'html.parser')
        except Exception as err:
            raise Exception(err)
    def getAllData(self):

        try:
            html_soup=self.soup
            main_table=html_soup.find_all("table")[0]
            main_table_body=main_table.find('tbody')
            table_rows=main_table_body.find_all('tr')
            if not(main_table or main_table_body or table_rows):
                raise Exception("Table Element Not Found.")
            data_list=[]
            for row in table_rows:
                
                table_data=row.find_all('td')
                if not table_data:
                    continue
                data_dist={
                    "state":table_data[0].text.title().strip(),
                    "confirmed":table_data[1].text.strip(),
                    "recovered":table_data[2].text.strip(),
                    "deaths":table_data[3].text.strip()       
                    }
               
                data_list.append(data_dist)
            
            data=IndiaCovidData(
                covid_data=data_list
            )
            data.save()
            return "Data Saved Successfully"
        except Exception as err:
            raise Exception(err)
        finally:
            self.driver.close()
            
    