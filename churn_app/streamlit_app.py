#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 18:10:08 2023

@author: disha.dubey
"""

#Import necessary libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

#read prediction data that we saved as a csv file while working on the ai_accelerator_modelInsights_streamlit_v1.ipynb notebook
predictions = pd.read_csv('prediction_output.csv',index_col=False)

max_rows = predictions.shape[0] #calculates the number of rows in predictions dataset


#--------setting page config -------------------------------------------------------
im = Image.open("./DR_icon.jpeg")
st.set_page_config(
    page_title="Customer Churn Prediction", #edit this for your usecase
    page_icon=im, #Adds datarobot logo to the tab
    layout="wide",
    initial_sidebar_state="collapsed",
)
#st.image('./DR_logo.png', width=200) #Image for logo
st.header("Customer Churn prediction") #edit this for your usecase
#st.sidebar.header("Customer Churn Prediction ") #edit this for your usecase


#-----Code to hide index when displaying dataframes-------- 
# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
#--------------------------------------------------------------------
#Specify columns to display from prediction dataset
#This should be edited based on your usecase 
columns= [['Customer_ID_x',
       'Dependents','Number_of_Referrals', 'Tenure_in_Months',
       'Internet_Type','Internet_Service','Contract', 'Paperless_Billing','Payment_Method', 
       'Monthly_Charge', 'Zip_Code', 'Churn_Value_1_PREDICTION']]

#Code to show different visualizations in the app
with st.container():
    
    

    with st.expander('Make your criteria selctions'):
            threshold = st.slider('Select churn threshold',min_value=0.00, max_value= 1.00, value=(0.0,1.00))
            max_rows = predictions[(predictions['Churn_Value_1_PREDICTION']>=threshold[0]) & (predictions['Churn_Value_1_PREDICTION']<=threshold[-1]) ].shape[0] #calculates the number of rows in predictions dataset based on churn threshold criteria
            display_rows = st.slider('How many customers you want to see ',min_value=1, max_value= max_rows, value = 10)
        #st.write(''''The table below shows churn risk scores for the number of customers you selected. The table is sorted based on **churn risk score**
         #        \'and the churn label is absed on the threshold setup in your deployment''')
    #columns to display in churn scores table
    columns_to_display = ['Customer_ID_x', 'Churn_Value_1_PREDICTION', 'Churn_Value_PREDICTION'] 
    #code to create dynamic dataframe based on user selection in the slider
    predictions_subset = predictions.sort_values(by='Churn_Value_1_PREDICTION' ,ascending= False).reset_index(drop=True).head(display_rows)
    #Plot to show top churn reason
    plot_df = predictions_subset['EXPLANATION_1_FEATURE_NAME'].value_counts().reset_index().rename(columns = {'index':'Feature_name', 'EXPLANATION_1_FEATURE_NAME':'customers'}).sort_values(by='customers' )
    fig = px.bar(plot_df, x= 'customers', y= 'Feature_name', orientation='h',title = "Top churn reason distribution")
 
with st.container():
    st.subheader(':blue[Churn score and top reason]')
    col1, col2 =st.columns(2)
    with col1:
        #code to show dataframe in the app
        st.markdown('**Show churn scores for customers**')
        #st.write('Churn risk score')
        st.dataframe(predictions_subset[columns_to_display].rename(columns = {'Customer_ID_x':'Customer_ID', 'Churn_Value_1_PREDICTION': 'Churn score', 'Churn_Value_PREDICTION': 'churn label'}))
        st.markdown('**Note**: _Churn label in the table above is based on the defualt churn threshold set for the deployment_')
    with col2:
        st.markdown("**Top churn reason distribution**")
        tab1, tab2 = st.tabs(['View plot', 'View data'])
        #Plot to show top reason for churn (prediction explanation ) by #customers
        tab1.plotly_chart(fig)
        #code to display the information in above plot as table
        tab2.table(plot_df.sort_values(by='customers' , ascending=False))


with st.container():
    st.subheader(':blue[Analyze customers based on a specific churn reason]')
    #Cdoe to further drill down on customers based on their top reason to churn
    reason_select = st.selectbox('Select churn reason to view customers', list(pd.unique(predictions['EXPLANATION_1_FEATURE_NAME'])))
    st.dataframe(predictions[predictions['EXPLANATION_1_FEATURE_NAME']==reason_select].sort_values(by='Churn_Value_1_PREDICTION' ,ascending= False))

