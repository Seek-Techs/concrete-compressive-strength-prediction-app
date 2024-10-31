import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from predicted import prediction
import base64

st.set_page_config(layout="wide", page_title="Concrete Compressive Strength Prediction")

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
    
# Center-aligned title
st.markdown("<h1 style='text-align: center;'>Concrete Compressive Strength Prediction</h1>", unsafe_allow_html=True)
    
st.sidebar.subheader('Enter Concrete Mix Design Parameters')
    
# Input fields with unit selection
unit_options = 'kg/m3'
selected_unit = unit_options
    
# Collect inputs
Cement = st.sidebar.number_input(f'Cement Quantity ({selected_unit})', min_value=102.0, max_value=540.0) 
BFS = st.sidebar.number_input(f'Blast Furnace Slag ({selected_unit})', min_value=0.0, max_value=359.4) 
Fly_Ash = st.sidebar.number_input(f"Fly Ash ({selected_unit})", min_value=0.0, max_value=200.1) 
Water = st.sidebar.number_input(f"Water ({selected_unit})", min_value=121.8, max_value=247.0) 
Superplasticizer = st.sidebar.number_input(f"Super Plasticizer ({selected_unit})", min_value=0.0, max_value=32.0)
Coarse_Aggregate = st.sidebar.number_input(f"Coarse Aggregate ({selected_unit})", min_value=801.0, max_value=1145.0)
Fine_Aggregate = st.sidebar.number_input(f"Fine Aggregate ({selected_unit})", min_value=594.0, max_value=992.0)
Age = st.sidebar.number_input("Age of Concrete (Days)", min_value=1, max_value=365)

# Predict compressive strength
if st.sidebar.button("Predict Concrete Compressive Strength"):
    try:
        result = prediction(Cement, BFS, Fly_Ash, Water, Superplasticizer, Coarse_Aggregate, Fine_Aggregate, Age)
        st.success(f'**The compressive strength of concrete is : {result[0]:.2f} N/mm²**')
        
        # Sorting data for the bar chart
        component_data = {
            'Component': ['Cement', 'BFS', 'Fly Ash', 'Water', 
                        'SP', 'CA', 'FA'],
            'Quantity': [Cement, BFS, Fly_Ash, Water, Superplasticizer, Coarse_Aggregate, Fine_Aggregate]
        }
        sorted_data = pd.DataFrame(component_data).sort_values(by='Quantity', ascending=False)

        # Create side-by-side subplots with adjusted column widths
        fig = make_subplots(
            cols=2, 
            column_widths=[0.8, 0.2],  # Wider for the component chart, narrower for age
            subplot_titles=("Concrete Component Quantities", "Age of Concrete")
        )

        # First chart for concrete component quantities
        fig.add_trace(
            go.Bar(x=sorted_data['Component'], y=sorted_data['Quantity'],
            marker_color='lightskyblue'),
            row=1, col=1
        )
        fig.update_xaxes(title_text="Input Features", row=1, col=1)
        fig.update_yaxes(title_text=f"Quantity ({selected_unit})", row=1, col=1)

        # Second chart for age
        fig.add_trace(
            go.Bar(x=['Age'], y=[Age], marker_color='lightskyblue'),
            row=1, col=2
        )
        fig.update_xaxes(title_text="Input Feature", row=1, col=2)
        fig.update_yaxes(title_text="Days", row=1, col=2)

        # Update overall layout and font sizes
        fig.update_layout(
            title_text="Concrete Mix Design Parameters",
            title_font_size=24,
            font=dict(size=16),  # Set general font size
            showlegend=False  # Hide legend
        )

        # Display the plot in Streamlit
        # st.plotly_chart(fig)
        st.plotly_chart(fig, use_container_width=False, width=350)

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

# Footer
footer = """
    <style>
        /* Fix footer to bottom of the page */
        footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f0f0f0;
            padding: 10px 0;
            text-align: center;
            color: #555;
            font-size: 16px;
            border-top: 1px solid #e0e0e0;
            z-index: 9999;
        }
    </style>
    <footer>
        <p>Developed with ❤️ by Yusuff Olatunji Sikiru</p>
    </footer>
"""

st.markdown(footer, unsafe_allow_html=True)

