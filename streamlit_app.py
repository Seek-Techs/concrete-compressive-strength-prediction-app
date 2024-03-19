import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Load the model
    try:
        # Load the pre-trained model and scaler
        model = pickle.load(open('gbr.pkl', 'rb'))
        scaler = pickle.load(open('scaler.pkl', 'rb'))
    except FileNotFoundError:
        st.error("Model file not found. Please make sure the model file exists.")
        return
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return
    
    # Set up the UI
    st.title('Concrete Compressive Strength Prediction')
    st.sidebar.subheader('Enter Concrete Mix Design Parameters')
    
    # Input fields with unit selection
    unit_options = ['kg', 'g', 'lb']
    selected_unit = st.sidebar.radio('Unit for input:', unit_options)
    
    # Conversion factors
    if selected_unit == 'kg':
        conversion_factor = 1
    elif selected_unit == 'g':
        conversion_factor = 1000
    else:  # lb
        conversion_factor = 2.20462  # 1 kg = 2.20462 lb
    
    cement = st.sidebar.number_input(f'Cement quantity ({selected_unit})', min_value=0.0) * conversion_factor
    blast_furnace_slag = st.sidebar.number_input(f'Blast Furnace Slag ({selected_unit})', min_value=0.0) * conversion_factor
    fly_ash = st.sidebar.number_input(f"Fly Ash ({selected_unit})", min_value=0.0) * conversion_factor
    water = st.sidebar.number_input(f"Water (%)", min_value=0.0)
    superplasticizer = st.sidebar.number_input(f"Super Plasticizer ({selected_unit})", min_value=0.0) * conversion_factor
    coarse_aggregate = st.sidebar.number_input(f"Coarse Aggregate ({selected_unit})", min_value=0.0) * conversion_factor
    fine_aggregate = st.sidebar.number_input(f"Fine Aggregate ({selected_unit})", min_value=0.0) * conversion_factor
    age = st.sidebar.number_input("Age of Concrete (Days)", min_value=0.0)
    
    float_features = [
            cement, 
            blast_furnace_slag, 
            fly_ash, 
            water, 
            superplasticizer, 
            coarse_aggregate,
            fine_aggregate, 
            age,
            ]
    features = [np.array(float_features)]
    final_features = scaler.transform(features)
    
    # Predict compressive strength
    if st.sidebar.button('Predict'):
        try:
            prediction = model.predict(final_features) 
            st.success(f'The compressive strength of concrete is : {prediction[0]:.2f} N/mm2')  
            
            # Visualization
            feature_names = ['Cement', 'BFS', 'FA', 'Water', 
                             'SP', 'CA', 'FA', 'Age']
            st.set_option('deprecation.showPyplotGlobalUse', False)
            fig = plt.figure(figsize=(10, 6))
            plt.bar(feature_names, float_features)
            plt.xlabel('Input Features', fontsize=14)
            plt.ylabel('Quantity', fontsize=14)
            plt.title('Concrete Component Quantities', fontsize=16)
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

if __name__ == '__main__':
    main()
