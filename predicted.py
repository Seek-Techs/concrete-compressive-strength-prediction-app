import joblib
import numpy

def prediction(Cement, BFS, Fly_Ash, Water, Superplasticizer, Coarse_Aggregate, Fine_Aggregate, Age):
    
    # Load GradientBoost Regression Model
    model = joblib.load("cement_model_GB.sav")
    
           
    # Making Prediction
    result = model.predict([[Cement, BFS, Fly_Ash, Water, Superplasticizer, Coarse_Aggregate, Fine_Aggregate, Age]])
    result = numpy.round(result, 4)
    return result
