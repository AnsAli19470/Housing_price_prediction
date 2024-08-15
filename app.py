from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract and prepare input data
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        housing_median_age = float(request.form['housing_median_age'])
        total_rooms = float(request.form['total_rooms'])
        total_bedrooms = float(request.form['total_bedrooms'])
        population = float(request.form['population'])
        households = float(request.form['households'])
        median_income = float(request.form['median_income'])

        INLAND = float(request.form.get('INLAND', 0))
        ISLAND = float(request.form.get('ISLAND', 0))
        NEAR_BAY = float(request.form.get('NEAR_BAY', 0))
        NEAR_OCEAN = float(request.form.get('NEAR_OCEAN', 0))

        # Prepare the input array
        arr = np.array([[longitude, latitude, housing_median_age, total_rooms, total_bedrooms, 
                         population, households, median_income, INLAND, ISLAND, NEAR_BAY, NEAR_OCEAN]])

        # Predict
        pred = model.predict(arr)
        return render_template('index.html', data=int(pred[0]))

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
