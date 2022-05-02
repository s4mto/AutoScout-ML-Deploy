#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:37:58 2022

@author: PyBoys
"""

#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import date
current_year = date.today().year



#load the model from disk
import joblib
filename = 'finalized_model_new.sav'
model = joblib.load(filename)

# y_pred = gbm.predict(X_test_scaled)
# test_back = np.exp(y_test)
# pred_back = np.exp(y_pred)
# print(r2_score(test_back,pred_back))
# print(mean_squared_error(test_back, pred_back, squared=False))

#Import python scripts
from preprocessing import preprocess,make_model_dict, n_dict

def main():
    #Setting Application title
    st.title('PyBoys AutoScout Model App')

      #Setting Application description
    st.markdown("""
     :dart:  This Streamlit app is made to predict AutoScout use case.
    The application is functional for online prediction. \n
    """)
    st.markdown("<h3></h3>", unsafe_allow_html=True)

    #Setting Application sidebar default
    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?", ("Online", "Default"))
    st.sidebar.info('This app is created to predict AutoScout use case')
    


    if add_selectbox == "Online":
        st.info("Input data below")
        #Based on our optimal features selection
        st.subheader("Top 10 Most Important Features:")
        make_model_label = st.selectbox('Make and Model of the Car' , (make_model_dict))
        first_registration = st.number_input('First Registration Year of the Car', min_value=1940, max_value=2022, value=2000)
        empty_weight = st.number_input('Empty Weight of the Car', min_value=600, max_value=10000000, value=650) #### ok
        mileage = st.number_input('Mileage of the Car',  value=0)
        Power = st.number_input('Power of the Car', value=0)
        fuel_consumption = st.number_input('Fuel Consumption of the Car', value=0)
        # total_consumption = st.number_input('Power of the Car', value=0)
        co2_emissions = st.number_input('Co2 emission per km')
        # total_co2_emissions = st.number_input('Power of the Car', value=0)  
        
        engine_size = st.number_input('Engine Size of the Car',value=0) 
        gears = st.selectbox('Gear of the Car', ('2','3', '4','5','6','7', '8','9'))
        seats = st.selectbox('Seat of the Car', ('2','5','6')) 
        doors = st.selectbox('Door of the Car', ('2','4','5','6'))      
        full_service_history_Yes = st.selectbox('Does the Car have a Service History', ('No','Yes'))

        age = current_year - first_registration 
        total_consumption =  fuel_consumption * mileage/100 
        total_co2_emissions = mileage * co2_emissions
        data = {
                'Make-Model': make_model_label,
                'Registration': age,
                'Empty Weight':empty_weight,
                'Milage/Year': mileage/age,
                'Milage': mileage,
                'Power': Power,
                'Total Consumption': total_consumption,
                'Total Co2 Emissions': total_co2_emissions,
                'Fuel Consumption': fuel_consumption,
                'Engine Size': engine_size,
                'Gear': n_dict[gears],
                'Seat': n_dict[seats],
                'Door': n_dict[doors],
                'Service History': full_service_history_Yes
                }
        features_df = pd.DataFrame.from_dict([data])
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        st.write('Overview of input is shown below')
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        st.dataframe(features_df)


        #Preprocess inputs
        preprocess_df = preprocess(features_df, 'Online')

        prediction = model.predict(preprocess_df)
        prediction = np.exp(prediction)

        if st.button('Predict'):
            st.warning('Prediction: ',prediction)
        

if __name__ == '__main__':
        main()