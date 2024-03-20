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
    # st.title('Concrete Compressive Strength Prediction')
    # Center-aligned title using Markdown syntax
    st.markdown("<h1 style='text-align: center; 'position: fixed;'>Concrete Compressive Strength Prediction</h1>", unsafe_allow_html=True)
    
    st.sidebar.subheader('Enter Concrete Mix Design Parameters')
    
    # Input fields with unit selection
    unit_options = ['kg/m3', 'lb/ft3']
    selected_unit = st.sidebar.radio('Unit for input:', unit_options)
    
    # Conversion factors
    if selected_unit == 'kg/m3':
        conversion_factor = 1
    # elif selected_unit == 'g':
    #     conversion_factor = 1000
    else:  # lb/ft3
        conversion_factor = 0.0624279606  # 1 kg/m3 = 0.0624279606 lb/ft3
        
    
    cement = st.sidebar.number_input(f'Cement quantity ({selected_unit})', min_value=0.0) * conversion_factor
    blast_furnace_slag = st.sidebar.number_input(f'Blast Furnace Slag ({selected_unit})', min_value=0.0) * conversion_factor
    fly_ash = st.sidebar.number_input(f"Fly Ash ({selected_unit})", min_value=0.0) * conversion_factor
    water = st.sidebar.number_input(f"Water ({selected_unit})", min_value=0.0) * conversion_factor
    superplasticizer = st.sidebar.number_input(f"Super Plasticizer ({selected_unit})", min_value=0.0) * conversion_factor
    coarse_aggregate = st.sidebar.number_input(f"Coarse Aggregate ({selected_unit})", min_value=0.0) * conversion_factor
    fine_aggregate = st.sidebar.number_input(f"Fine Aggregate ({selected_unit})", min_value=0.0) * conversion_factor
    age = st.sidebar.number_input("Age of Concrete (Days)", min_value=0)
    
    # Validation
    if cement == 0 or water == 0 or coarse_aggregate == 0 or fine_aggregate == 0 or age == 0:
        st.error("Input values must not be zero. Please enter valid values.")
    else:
        # st.success("All input values are valid.")
    
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
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Predict compressive strength
        if st.sidebar.button('Predict'):
            try:
                prediction = model.predict(final_features) 
                st.success(f'The compressive strength of concrete is : {prediction[0]:.2f} N/mm2')  
                
                # Visualization
                feature_names = ['Cement', 'BFS', 'FA', 'Water', 
                                'SP', 'CA', 'FA']
                
                fig, axes = plt.subplots(1, 2, figsize=(15, 8))

                # Plotting the first graph
                axes[0].bar(feature_names, float_features[:-1])  # Excluding 'Age'
                axes[0].set_xlabel('Input Features', fontsize=16)
                axes[0].set_ylabel(f'Quantity ({selected_unit})', fontsize=16)
                axes[0].set_title('Concrete Component Quantities', fontsize=16)
                axes[0].tick_params(axis='both', labelsize=14)

                # Plotting the second graph
                axes[1].bar('Age', age, color='orange')  # Plotting 'Age' separately
                axes[1].set_xlabel('Input Features', fontsize=16)
                axes[1].set_ylabel('Days', fontsize=14)
                axes[1].set_title('Age of Concrete', fontsize=16)
                axes[1].tick_params(axis='both', labelsize=14)
                
                # Set a different size for the second subplot
                axes[1].set_aspect(0.3)  # Adjust the aspect ratio

                plt.tight_layout()
                    
                # Show the plot graph
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

if __name__ == '__main__':
    main()
