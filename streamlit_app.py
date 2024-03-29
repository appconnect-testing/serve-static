import streamlit as st

if __name__ == "__main__":
    st.set_page_config(
        page_title="fish ai project",
        page_icon="chart_with_upwards_trend",
        layout="wide",
    )

    import warnings
    warnings.filterwarnings("ignore")
    import numpy as np  # np mean, np random
    import pandas as pd  # read csv, df_moon manipulation
    import plotly.express as px  # interactive charts
    import streamlit as st  # 🎈 data web app development
    import html_functions
    from PIL import Image
    import os
    import re
    import other_func
    import main2
    import random
    import json
    import io
    import requests


    import os

    from dotenv import load_dotenv

    load_dotenv()

    






    def find_fisker():
        fisker = {}
        for i in list(dict(main_data["Art FAO"].value_counts()))[:15]:
            try:

                fisker[i] = [f for f in os.listdir("fish") if re.search(i, f, flags=re.IGNORECASE)][0]
            except:

                pass
        return fisker


    def average_for_place_and_time_sss(limiting_place, lower_month, higher_month):
        mid_df = sss_data.loc[(sss_data["variable"] == limiting_place) & (sss_data["month"] >= lower_month) & (sss_data["month"] <= higher_month)]
        return round(mid_df["value"].mean(), 2)
    def average_for_time_sss(lower_month, higher_month):
        mid_df = sss_data.loc[(sss_data["month"] >= lower_month) & (sss_data["month"] <= higher_month)]
        return round(mid_df["value"].mean(), 2)


    def average_for_place_and_time_sst(limiting_place, lower_day, higher_day):
        mid_df = sst_data.loc[(sss_data["variable"] == limiting_place) & (sst_data["day"] >= lower_day) & (sst_data["day"] <= higher_day)]
        return round(mid_df["value"].mean(), 2)

    def average_for_time_sst( lower_day, higher_day):
        mid_df = sst_data.loc[(sst_data["day"] >= lower_day) & (sst_data["day"] <= higher_day)]
        return round(mid_df["value"].mean(), 2)




    def file_by_url(url):
        s=requests.get(url).content
        return io.StringIO(s.decode('utf-8'))


    @st.cache_resource()
    def open_dataframes():


        #df_moon = pd.read_csv("/Users/audunbutenschon/Documents/intito materiale/moon_data.csv")
        #main_data = pd.read_csv("/Users/audunbutenschon/Documents/intito materiale/fangstdata_full.csv")
        #sss_data = pd.read_csv("/Users/audunbutenschon/Documents/intito materiale/sss_prototype_data.csv")
        #sst_data = pd.read_csv("/Users/audunbutenschon/Documents/intito materiale/sst_prototype_data.csv")

        df_moon = pd.read_csv(file_by_url("https://data-for-stuff.s3.us-east.cloud-object-storage.appdomain.cloud/moon_data.csv"))
        main_data = pd.read_csv(file_by_url("https://data-for-stuff.s3.us-east.cloud-object-storage.appdomain.cloud/fangstdata_full%20(2).csv"))
        sss_data = pd.read_csv(file_by_url("https://data-for-stuff.s3.us-east.cloud-object-storage.appdomain.cloud/sss_prototype_data.csv"))
        sst_data = pd.read_csv(file_by_url("https://data-for-stuff.s3.us-east.cloud-object-storage.appdomain.cloud/sst_prototype_data.csv"))

        places_cord = main_data[["Lon (hovedområde)", "Lat (hovedområde)", "Hovedområde", "Siste fangstdato"]].drop_duplicates(subset=["Hovedområde", "Siste fangstdato"])[:-2].dropna(subset=["Lon (hovedområde)", "Lat (hovedområde)"])
        places_cord["kordinater"] = "(" + places_cord["Lat (hovedområde)"].str.replace(",", ".").astype(float).round(0).astype(str) + ", " + places_cord["Lon (hovedområde)"].str.replace(",", ".").astype(float).round(0).astype(str) + ")"
        sss_data = sss_data.merge(places_cord, left_on="variable", right_on="kordinater", how="left")
        sst_data = sst_data.merge(places_cord, left_on="variable", right_on="kordinater", how="left")
        places_cord["Lon (hovedområde)"] = places_cord["Lon (hovedområde)"].str.replace(",", ".").astype(float); places_cord["Lat (hovedområde)"] = places_cord["Lat (hovedområde)"].str.replace(",", ".").astype(float)
        places_cord.rename(columns={"Lon (hovedområde)": "lon","Lat (hovedområde)": "lat" }, inplace=True)
        places_cord["Siste fangstdato"] = pd.to_datetime(places_cord["Siste fangstdato"])
        main_data["Siste fangstdato"] = pd.to_datetime(main_data["Siste fangstdato"])

        sss_data = sss_data[~sss_data["value"].isin(["--"])]
        sss_data["value"]  = sss_data["value"].astype(float).round(3)


        import ibm_boto3
        from ibm_botocore.client import Config
        api_key = os.getenv("api_key")
        service_instance_id = os.getenv("service_instance_id")
        auth_endpoint = os.getenv("auth_endpoint")
        service_endpoint = os.getenv("service_endpoint")
        s3 = ibm_boto3.resource('s3',
                ibm_api_key_id=api_key,
                ibm_service_instance_id=service_instance_id,
                ibm_auth_endpoint=auth_endpoint,
                config=Config(signature_version='oauth'),
                endpoint_url=service_endpoint)

        return df_moon, main_data, sss_data, places_cord, sst_data, s3



    df_moon, main_data, sss_data, places_cord, sst_data, s3 = open_dataframes()





    df_moon["date"] = pd.to_datetime(df_moon["date"])

    sub_main_data = main_data[["loc", "Hovedområde"]].drop_duplicates(subset="Hovedområde")
    places = dict(zip(list(sub_main_data["Hovedområde"]), sub_main_data["loc"]))


    col1, col2, col3 = st.columns(3)
    from datetime import datetime

    start_time = st.slider(
        "up to what date do you wish to view data from",
        value=(datetime(2021, 1, 1)),
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2021, 12, 30),
        format="MM/DD/YY")


    date1 = df_moon.loc[df_moon["date"] ==start_time]["moon_phase_complicated"]

    date2 = date1

    with open('style.css') as f:
        html = f'<style>{f.read()}</style>'
        picture_location =  "https://intitoimages.s3.eu-de.cloud-object-storage.appdomain.cloud/moon%20slider%20"+str(int(date1/0.12)+1)+".png"

        html = html.replace("replace_this_with_moon_slider", picture_location)
        st.markdown(html, unsafe_allow_html=True)






    #with st.container():
    #    col1, col2= st.columns(2)
    #    with col1:
    #        place = st.selectbox("choose location",  ["all"] + list(places))











    #if start_time != datetime(2021, 1, 1):
        #places_cord = places_cord.loc[places_cord["Siste fangstdato"] >= start_time[0]]
        #places_cord = places_cord.loc[places_cord["Siste fangstdato"] <= start_time[1]]
    places_cord = places_cord.loc[places_cord["Siste fangstdato"] <= start_time]
    main_data = main_data.loc[main_data["Siste fangstdato"] <= start_time]



    with st.container():
        col1, col2= st.columns(2)
        with col1:
            place = st.selectbox("choose location",  ["all"] + list(places))
            if place != "all":
                places_cord = places_cord.loc[places_cord["Hovedområde"] == place]
                main_data = main_data.loc[main_data["Hovedområde"] == place]

            st.map(places_cord[["lon", "lat"]], use_container_width=True, zoom=2)
        with col2:
            print_this = "nothing"
            if place != "all":
                #print_this = average_for_place_and_time_sss(places_cord["kordinater"][places_cord.first_valid_index()],start_time[0].month , start_time[1].month)
                print_this = average_for_place_and_time_sss(places_cord["kordinater"][places_cord.first_valid_index()],0 , start_time.month)
            if place == "all":
                #print_this = average_for_time_sss(start_time[0].month , start_time[1].month)
                print_this = average_for_time_sss(0, start_time.month)

            if place != "all":
                first_jan = datetime(day=1, month=1, year= 2021)
                print_this_sst = average_for_place_and_time_sst(places_cord["kordinater"][places_cord.first_valid_index()],0 , (start_time-first_jan).days)
            if place == "all":
                first_jan = datetime(day=1, month=1, year= 2021)
                #print_this_sst = average_for_time_sst((start_time[0]-first_jan).days , (start_time[1]-first_jan).days)
                print_this_sst = average_for_time_sst((start_time-first_jan).days , (start_time-first_jan).days)

            main2.construct_valves(print_this, print_this_sst, main_data=main_data)

            #st.metric("salt", f"{print_this}‰ (Per-mile)")
            #st.metric("se", f"{print_this_sst}°C")

    opptelling_av_tall =dict(main_data["Art FAO"].value_counts())


    fesk_data = find_fisker()

    other_func.generate_image(main_data)
    st.image("test.png")

    translated_parameters = {"Fartøynasjonalitet gruppe":"Nationality of fishermen", "Kvalitet": "Quality",  "Art FAO": "Fish species", "Fartøynavn": "Name of vessel", "Hovedområde FAO": "General area" }

    main2.generate_form(["Fartøynasjonalitet gruppe","Kvalitet", "Art FAO","Fartøynavn","Hovedområde FAO"], translated_parameters)


    import webbrowser

    if st.button('cognos'):
        webbrowser.open_new_tab("https://eu-de.dataplatform.cloud.ibm.com/dashboards/36f9fe33-261c-479a-9d49-3ff1eaab3aa2/view/5306da372ca328e277febde407cf2c547462270ebabb8b0782867b495c667897a8601bc7c8264e08d2445060faea1559c1")


    data = {"date":start_time.strftime("%Y%m%d%H%M%S"), "location": str(place)}
    with open("parameters.json", "w") as jsonFile:
        json.dump(data, jsonFile)



    data = open("parameters.json", 'rb')

    s3.Bucket('imagesforintitodash').put_object(Key="parameters.json", Body=data)
