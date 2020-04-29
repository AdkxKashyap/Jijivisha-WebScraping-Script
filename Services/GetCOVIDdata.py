import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from Model import covid_data_model as MODEL
from Model.global_aggregate_datamodel import AggregateGlobalData



class RetriveCOVIdDATA: 
    def __init__(self):
        try:
            # Using selenium for web scraping
           
            self.driver=webdriver.Chrome('C:/Users/Akash Deep Kashyap/chromedriver')
            
            self.driver.get('https://www.worldometers.info/coronavirus/#countries')
            self.soup=BeautifulSoup(self.driver.page_source,'html.parser')
        except:
            raise Exception("Could not Fetch Data")
        
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
            
            data=AggregateGlobalData(
                agg_covid_data=all_data_dict
            )
            data.save()
            return "Data Saved Successfully!"
        except Exception as err:
            return err
        finally:
            self.driver.close()
    #gets data of all the countries and also continents
    def get_data_allcountries(self):
        try:
            html_soup=self.soup
            html_table=html_soup.find('table',{"id":"main_table_countries_today"})
            html_tbody=html_table.find_all('tbody')[0]
            html_tr=html_tbody.find_all('tr',{"role":"row"})

            if not(html_table or html_tbody or html_tr):
                raise Exception("Table Element Not Found.")

            data_list=[]
            for tr in html_tr:
                
                html_td=tr.find_all('td')
                country=html_td[0].text.lower().strip()
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
                    "total_cases":html_td[1].text.strip(),
                    "new_cases":html_td[2].text.strip(),
                    "total_deaths":html_td[3].text.strip(),
                    "new_deaths":html_td[4].text.strip(),
                    "total_recovered":html_td[5].text.strip(),
                    "active_cases":html_td[6].text.strip(),
                    "serious_or_critical":html_td[7].text.strip(),
                    "tot_cases_oneM_pop":html_td[8].text.strip(),
                    "deaths_oneM_pop":html_td[9].text.strip(),
                    "total_tests":html_td[10].text.strip(),
                    "tests_oneM_pop":html_td[11].text.strip(),
                    "continent":html_td[12].text.lower().strip()
                }
                data_list.append(data_dist)
            data=MODEL.GlobalData(
                covid_data=data_list
            )
            data.save()
            return "Data Saved Successfully!"
        except Exception as err:
            raise Exception(err)
        finally:
            self.driver.close()
         

            
        