from Services import GetCOVIDdata
from Services.GetCOVIDdata import RetriveCOVIdDATA
from Services.GetIndiaData import GetIndiaData
from Services.GetIndiaNews import GetIndiaNews
from Services.GetWorldNews import GetGlobalNews
from Services.GetMythBusters import GetMythBusters
from db import mongo

def main():
    try:
        get_covid_data=GetCOVIDdata.RetriveCOVIdDATA().get_data_allcountries()
        print(get_covid_data)
        get_agg_data=RetriveCOVIdDATA().get_data_aggregate()
        print(get_agg_data)
        get_india_data=GetIndiaData().getAllStatesData()
        print(get_india_data)

        print(GetIndiaNews().get_all_news())
        print(GetGlobalNews().get_all_news())
        print(GetIndiaData().get_district_data())
        # print(GetMythBusters().save_data())
    except Exception as identifier:
        print(identifier)
   
if __name__=='__main__':
    main()