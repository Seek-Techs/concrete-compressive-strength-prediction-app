import joblib
import numpy

def predict(Cement, BFS, Fly_Ash, Water, Superplasticizer, Coarse_Agg, Fine_Agg, Age):
    
    # Load GradientBoost Regression Model
    model = joblib.load("cement_model_GB.sav")
    
           
    # Making Prediction
    result = model.predict([[Cement, BFS, Fly_Ash, Water, Superplasticizer, Coarse_Agg, Fine_Agg, Age]])
    result = numpy.round(result, 4)
    return result[0]
