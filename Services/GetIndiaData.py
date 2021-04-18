from bs4 import BeautifulSoup
from selenium import webdriver
from Model.india_covid_datamodel import IndiaCovidData
from Model.india_district_covid_datamodel import IndianDistrictData
import requests
import logging
import json

class GetIndiaData():
    def __init__(self):
        logging.basicConfig(filename="./logs/GetIndiaData.log",filemode='w',format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)
        try:
            url='https://api.covid19india.org/v4/data.json'
            page=requests.get(url)
            self.all_india_data=page.json()
            logging.info("++++++++ ALL INDIA DATA +++++++++++++%s",self.all_india_data)
        except Exception as err:
            logging.exception(err)
            raise Exception(err)

    # def get_soup(self,page):    
    #     return BeautifulSoup(page.content,'html.parser')

    def getAllStatesData(self):

        try:
            data=self.all_india_data
            data_list=[]
            for key in data:
                if(key=='TT'):
                    continue
                
                total_data=data[key]['total']
                tested=total_data['tested'] if total_data['tested'] else 'NA'
                confirmed=total_data['confirmed'] if total_data['confirmed'] else 'NA'
                recovered=total_data['recovered'] if total_data['recovered'] else 'NA'
                deaths=total_data['deceased'] if total_data['deceased'] else 'NA'
                state=self.getState(key)
                data_dict={
                    "state":state,
                    "confirmed":confirmed,
                    "recovered":recovered,
                    "deaths":deaths,
                    "tested":tested
                }
                data_list.append(data_dict)

            logging.info("%s+++++++++ STATES DATA LIST ++++++++++++++++++%s",self.getAllStatesData.__name__,data_list)

            
            data=IndiaCovidData(
                covid_data=data_list
            )
            data.save()
            return "All States Data Saved Successfully"
        except Exception as err:
            logging.exception(err)
            raise Exception(err)
    
    def get_district_data(self):
        try:
            data=self.all_india_data
            data_list=[]
            for key in data:
                if(key=='TT'):
                    continue
                state_name=self.getState(key).strip().lower()
                districts_data=data[key]['districts']
                data_list.append({"state":state_name,"districts":json.dumps(districts_data)})
            logging.info("%s+++++++++ Districts DATA LIST ++++++++++++++++++%s",self.get_district_data.__name__,data_list)
            data=IndianDistrictData(
                covid_data=data_list
            )
            data.save()
            return "Districts Data Saved Successfully"
        except Exception as identifier:
            logging.exception(identifier)
            raise Exception(identifier)
        
    def getState(self,state_code):
        #returns state name using state code
        if(state_code=='AN'):
            return 'Andaman And Nicobar Islands'

        if(state_code=='AP'):
            return 'Andhra Pradesh'
        
        if(state_code=='AR'):
            return 'Arunachal Pradesh'
        
        if(state_code=='AS'):
            return 'Assam'
        
        if(state_code=='BR'):
            return 'Bihar'

        if(state_code=='CH'):
            return 'Chandigarh'
        
        if(state_code=='CT'):
            return 'Chattisgarh'

        if(state_code=='DL'):
            return 'Delhi'

        if(state_code=='DN'):
            return 'Dadra And Nagar Haveli'

        if(state_code=='GA'):
            return 'Goa'

        if(state_code=='GJ'):
            return 'Gujarat'

        if(state_code=='HR'):
            return 'Haryana'

        if(state_code=='HP'):
            return 'Himachal Pradesh'

        if(state_code=='JH'):
            return 'Jharkhand'

        if(state_code=='JK'):
            return 'Jammu And Kashmir'

        if(state_code=='KA'):
            return 'Karnataka'

        if(state_code=='KL'):
            return 'Kerala'

        if(state_code=='LA'):
            return 'Ladakh'

        if(state_code=='MH'):
            return 'Maharashtra'

        if(state_code=='ML'):
            return 'Meghalaya'

        if(state_code=='MN'):
            return 'Manipur'

        if(state_code=='MP'):
            return 'Madhya Pradesh'

        if(state_code=='MZ'):
            return 'Mizoram'

        if(state_code=='NL'):
            return 'Nagaland'

        if(state_code=='OR'):
            return 'Odisha'

        if(state_code=='PB'):
            return 'Punjab'

        if(state_code=='PY'):
            return 'Pondicherry'

        if(state_code=='RJ'):
            return 'Rajasthan'

        if(state_code=='SK'):
            return 'Sikkim'

        if(state_code=='TG'):
            return 'Telangana'

        if(state_code=='TR'):
            return 'Tripura'

        if(state_code=='TN'):
            return 'Tamil Nadu'

        if(state_code=='UP'):
            return 'Uttar Pradesh'

        if(state_code=='UT'):
            return 'Uttarakhand'

        if(state_code=='WB'):
            return 'West Bengal'

             
            