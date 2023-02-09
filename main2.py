import streamlit as st
import json
import numpy as np
import plotly.graph_objects as go
import pandas as pd
def generate_form(relevant_parameters, translations):
    eng_relevant_parameters = [translations[i] for i in relevant_parameters]
    eng_to_nor_translations = dict([(value, key) for key, value in translations.items()])


    col1, col2, col3, col4, col5 = st.columns(5)

    with col2:
        if st.button("add field"):
            with open("a_number.txt", "r") as r:
                n_fields = int(r.read())
            with open("a_number.txt", "w") as w:
                w.write(str(n_fields + 1))

    with col4:
        if st.button("remove field"):
            with open("a_number.txt", "r") as r:
                n_fields = int(r.read())
            with open("a_number.txt", "w") as w:
                w.write(str(n_fields - 1))
    with st.form("inference_form"):


        with open("a_number.txt", "r") as r:
            n_fields = int(r.read())
        parameters = ["parameter " + str(i) for i in range(n_fields)]
        values = ["value " + str(i) for i in range(n_fields)]
        columns = st.columns(n_fields)
        current = -1 
        for i in columns:
            current += 1
            with i:
                parameters[current] = st.selectbox("parameter " + str(current), eng_relevant_parameters)
                values[current] = st.text_input(label="value " + str(current), value="")
        submitted = st.form_submit_button("Submit")
        if submitted:

            nor_parameters = [eng_to_nor_translations[i] for i in parameters]
            answers = dict(zip(nor_parameters, values))
            from IBM_sdk_functions import query_ai_model
            from stats_func import generate_certainity_plot, generate_text
            response = query_ai_model(answers)
            #response =  {'predictions': [{'fields': ['prediction', 'probability'], 'values': [['Trål', [4.607365917763673e-05, 0.003946150187402964, 1.9864196474372875e-06, 0.9960058331489563]]]}]}
            all_cols = st.columns(7)
            with all_cols[2]:
                #st.text(response["predictions"][0]["values"][0][0])
                st.pyplot(generate_text(response["predictions"][0]["values"][0][0]))
            with all_cols[3]:
                fig = generate_certainity_plot(np.array(response["predictions"][0]["values"][0][1]).sum())
                st.pyplot(fig)
                #st.text(response["predictions"][0]["values"][0][1][-1])
            with all_cols[4]:
                img_addresses = {"Not": "redskap/not redskap.gif", "Trål": "redskap/trawling.png", "Konvensjonelle": "redskap/konvensjonell.png"}
                st.image(img_addresses[response["predictions"][0]["values"][0][0]])
            with open('answers.json', 'w') as fp:
                json.dump(answers, fp)
            

'''
def construct_valves(salt, temperatur):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    def salt_innhold(salt):
        return go.Indicator(
            mode = "gauge+number+delta",
            value = salt,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "salinity ‰ (Per-mile)", 'font': {'size': 24}},
            delta = {'reference': 34.2, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [None, 40], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                })
    def sea_surface(temperatur):
        return  go.Indicator(
            mode = "gauge+number+delta",
            value = temperatur,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Sea surface temperature °C", 'font': {'size': 24}},
            delta = {'reference': 6.95, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [None, 20], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                })
    fig = make_subplots(rows=2, cols=1, specs=[[{'type' : 'indicator'}], [{'type' : 'indicator'}]])

    fig.add_trace(
        salt_innhold(salt), row=1, col=1
    )
    fig.add_trace(
        sea_surface(temperatur), row=2, col=1
    )
    fig.update_layout(height=600, width=600)

    return st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")


'''


def construct_valves(salt, temperatur, main_data):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    def create_pie_chart():
        import plotly.graph_objects as go
        df_mid = pd.DataFrame(main_data["Salgslag"].value_counts()).reset_index()
        labels = list(df_mid["index"])
        values = list(df_mid["Salgslag"])

        return go.Pie(labels=labels, values=values, title = {'text': "Salgslag", 'font': {'size': 14}})
    def create_pie_chart2():
        df_mid = pd.DataFrame(main_data["Redskap - hovedgruppe"].value_counts()).reset_index()
        labels = list(df_mid["index"])
        values = list(df_mid["Redskap - hovedgruppe"])
        return  go.Pie(labels=labels, values=values, title = {'text': "Redskap", 'font': {'size': 14}})


    def salt_innhold(salt):
        return go.Indicator(
            mode = "gauge+number+delta",
            value = salt,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "salinity ‰ (Per-mile)", 'font': {'size': 14}},
            delta = {'reference': 34.2, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [None, 40], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                })
    def sea_surface(temperatur):
        return  go.Indicator(
            mode = "gauge+number+delta",
            value = temperatur,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Sea surface temperature °C", 'font': {'size': 14}},
            delta = {'reference': 6.95, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [None, 20], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                })
    fig = make_subplots(rows=2, cols=2, specs=[[{'type' : 'indicator'},{'type' : 'pie' }], [{'type' : 'indicator'}, {'type' : 'pie' }]])
    fig.add_trace(
        create_pie_chart(), row=1, col=2
    )
    fig.add_trace(
        create_pie_chart2(), row=2, col=2
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')


    fig.add_trace(
        salt_innhold(salt), row=1, col=1
    )
    fig.add_trace(
        sea_surface(temperatur), row=2, col=1
    )

    
    fig.update_layout(height=600, width=700, showlegend=False)

    return st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")


