import requests
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from Model import covid_data_model as MODEL
from Model.global_aggregate_datamodel import AggregateGlobalData



class RetriveCOVIdDATA: 
    def __init__(self):
        try:
          
            logging.basicConfig(filename="./logs/GetCovidData.log",filemode='w',format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)
            page=requests.get("https://www.worldometers.info/coronavirus/#countries")
            self.soup=self.get_soup(page)
            # print(self.soup)
        except Exception as err:
            raise Exception(err)
    def get_soup(self,page):    
        return BeautifulSoup(page.content,'html.parser')

    def check_elem(self,func_name,elem,elem_name):
         #For easy debugging
        if not elem:
            errMsg="In "+func_name+","+elem_name+" Not Found."
            raise Exception(errMsg)

    def get_data_aggregate(self):
        try:
            #returns overall data-overall deaths,recovered etc.   
            html_soup=self.soup
            #getting data of maincounter
            main_res=html_soup.find_all(class_="maincounter-number")
            #getting active cases,closed cases etc
            cases_list=[]
            cases_panels=html_soup.find_all(class_="panel panel-default")
            for panel in cases_panels:
                data_1=panel.find('div',{'class':'number-table-main'}).text.strip()
                span_data=panel.find_all('span',{'class':'number-table'})
                data_2=span_data[0].text.strip()
                data_3=span_data[1].text.strip()
                cases_list.append(data_1)
                cases_list.append(data_2)
                cases_list.append(data_3)
            data_list=[]
            #getting data from each counter
            for data in main_res:
                counter_number_wrapper=data.find('span')
                counter_number_content=counter_number_wrapper.text.strip()
                data_list.append(counter_number_content)

            data_list=data_list+cases_list
            all_data_dict={
                "covid19_cases":data_list[0],
                "total_deaths":data_list[1],
                "total_recovered":data_list[2],
                "total_infected":data_list[3],
                "in_mild_condition":data_list[4],
                "serious_critical":data_list[5],
                "cases_with_outcome":data_list[6],
                "recovered_discharged":data_list[7]
            }
            # print(all_data_dict)
            logging.info("%s+++++++++++++++%s",self.get_data_aggregate.__name__,all_data_dict)
            data=AggregateGlobalData(
                agg_covid_data=all_data_dict
            )
            data.save()
            return "Aggregate Data Saved Successfully!"
        except Exception as err:
            return err
        
    #gets data of all the countries and also continents
    def get_data_allcountries(self):
        try:
            func_name=self.get_data_allcountries.__name__
            html_soup=self.soup
            self.check_elem(func_name,html_soup,"html_soup")
            html_table=html_soup.find('table',{"id":"main_table_countries_today"})
            self.check_elem(func_name,html_table,"html_table")
            html_tbody=html_table.find_all('tbody')[0]
           
            self.check_elem(func_name,html_tbody,"html_tbody")
            html_tr=html_tbody.find_all('tr')
            # print(html_tr)
            self.check_elem(func_name,html_tr,"html_tr")

           

            data_list=[]
            for tr in html_tr:
                
                html_td=tr.find_all('td')
                self.check_elem(func_name,html_td,"html_td")
                country=html_td[1].text.lower().strip()
                #removing continents from datalist
                type_="country"
                continents=['world','europe','africa','asia','north america','south america','oceania']
                if country in continents:
                    type_="continents"

                if country=='usa':
                    country='United States'
                if country=='uk':
                    country='United Kingdom'
                if country=='s. korea':
                    country='South Korea'
                if country=='drc':
                    country='Democratic Republic of the Congo'
                if country=='congo':
                    country='Republic of the Congo'
                if country=='car':
                    country='Central African Republic'
                data_dist={
                    "type":type_,
                    "country":country.title().strip(),
                    "total_cases":html_td[2].text.strip(),
                    "new_cases":html_td[3].text.strip(),
                    "total_deaths":html_td[4].text.strip(),
                    "new_deaths":html_td[5].text.strip(),
                    "total_recovered":html_td[6].text.strip(),
                    "active_cases":html_td[8].text.strip(),
                    "serious_or_critical":html_td[9].text.strip(),
                    "tot_cases_oneM_pop":html_td[10].text.strip(),
                    "deaths_oneM_pop":html_td[11].text.strip(),
                    "total_tests":html_td[12].text.strip(),
                    "tests_oneM_pop":html_td[13].text.strip(),
                    "continent":html_td[15].text.lower().strip()
                }
                # print( html_td[8].text.strip(),country)
                data_list.append(data_dist)
            logging.info("%s+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%s",self.get_data_allcountries.__name__,data_list)
            data=MODEL.GlobalData(
                covid_data=data_list
            )
            data.save()
            return "All Countries Data Saved Successfully!"
        except Exception as err:
            raise Exception(err)
       

            
        