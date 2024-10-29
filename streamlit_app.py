import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prediction import predict
import base64

st.set_page_config(layout="wide", page_title="Concrete Compressive Strength Prediction")

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
    
# Center-aligned title
st.markdown("<h1 style='text-align: center;'>Concrete Compressive Strength Prediction</h1>", unsafe_allow_html=True)
    
st.sidebar.subheader('Enter Concrete Mix Design Parameters')
    
# Input fields with unit selection
unit_options = ['kg/m3', 'lb/ft3']
selected_unit = st.sidebar.radio('Unit for input:', unit_options)
    
# Conversion factors
conversion_factor = 1 
if selected_unit == 'kg/m3' else 0.0624279606  # lb/ft3

# Collect inputs
cement = st.sidebar.number_input(f'Cement quantity ({selected_unit})', min_value=102.0, max_value=540.0) * conversion_factor
blast_furnace_slag = st.sidebar.number_input(f'Blast Furnace Slag ({selected_unit})', min_value=72.04, max_value=359.4) * conversion_factor
fly_ash = st.sidebar.number_input(f"Fly Ash ({selected_unit})", min_value=0.0, max_value=200.1) * conversion_factor
water = st.sidebar.number_input(f"Water ({selected_unit})", min_value=121.8, max_value=247.0) * conversion_factor
superplasticizer = st.sidebar.number_input(f"Super Plasticizer ({selected_unit})", min_value=0.0, max_value=32) * conversion_factor
fine_aggregate = st.sidebar.number_input(f"Fine Aggregate ({selected_unit})", min_value=594.0, max_value=992.0) * conversion_factor
coarse_aggregate = st.sidebar.number_input(f"Coarse Aggregate ({selected_unit})", min_value=801.0, max_value=1145.0) * conversion_factor
age = st.sidebar.number_input("Age of Concrete (Days)", min_value=1, max_value=365)

# Predict compressive strength
if st.sidebar.button('Predict'):
    try:
        # Call prediction function
        result = predict(cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age)
        st.success(f'**The compressive strength of concrete is : {result:.2f} N/mm²**')
        
        # Visualization
        feature_names = ['Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water', 
                         'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate']
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 8))

        # First bar chart
        axes[0].bar(feature_names, [cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate])
        axes[0].set_xlabel('Input Features', fontsize=16)
        axes[0].set_ylabel(f'Quantity ({selected_unit})', fontsize=16)
        axes[0].set_title('Concrete Component Quantities', fontsize=16)
        axes[0].tick_params(axis='both', labelsize=14)

        # Second bar chart for Age
        axes[1].bar(['Age'], [age], color='orange')
        axes[1].set_xlabel('Input Features', fontsize=16)
        axes[1].set_ylabel('Days', fontsize=14)
        axes[1].set_title('Age of Concrete', fontsize=16)
        axes[1].tick_params(axis='both', labelsize=14)
        
        plt.tight_layout()
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

# Footer
footer = """
<footer style='position: fixed; bottom: 0; background-color: #f0f0f0; padding: 10px; text-align: center; width: 100%;'>
<p>Developed with ❤️ by Yusuff Olatunji Sikiru</p>
</footer>
"""
st.markdown(footer, unsafe_allow_html=True)
