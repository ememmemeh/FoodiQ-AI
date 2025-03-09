import requests
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import streamlit as st

# Streamlit UI Integration
st.title('🍔 FoodiQ: AI for Food Science')

# Food Composition Analyzer (Using Image Upload)
st.subheader('Food Composition Analyzer_MLZ')
image_file = st.file_uploader('Upload Food Image', type=['jpg', 'png'])

# Using Edamam Food Image Recognition API
EDAMAM_API_URL = "https://api.edamam.com/api/food-database/v2/parser"
APP_ID = "YOUR_EDAMAM_APP_ID"
APP_KEY = "YOUR_EDAMAM_APP_KEY"

def analyze_food(image_file):
    try:
        files = {'image': image_file.getvalue()}
        params = {
            'app_id': APP_ID,
            'app_key': APP_KEY
        }
        result = requests.post(EDAMAM_API_URL, files=files, params=params)
        if result.status_code == 200:
            return result.json()
        else:
            return {'error': 'Invalid response from API'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

if image_file and st.button('Analyze Food Composition'):
    response = analyze_food(image_file)
    if 'error' in response:
        st.write(f"Error: {response['error']}")
    else:
        parsed_foods = response.get('parsed', [])
        for food in parsed_foods:
            food_name = food['food']['label']
            nutrients = food['food']['nutrients']
            st.write(f"### {food_name}")
            for nutrient, value in nutrients.items():
                st.write(f"{nutrient}: {value}")


# Spoilage Prediction Section
st.subheader('Food Spoilage Prediction')
ingredients = st.text_input('Enter Ingredients (comma-separated)')
storage_temp = st.number_input('Storage Temperature (°C)', value=4)

def predict_spoilage(ingredients, storage_temp):
    shelf_life_data = {
        'milk': 5,
        'eggs': 7,
        'chicken': 3,
        'lettuce': 4
    }

    ingredients_list = [i.strip().lower() for i in ingredients.split(',') if i.strip()]
    if not ingredients_list:
        return "No ingredients provided."

    total_shelf_life = sum([shelf_life_data.get(i, 2) for i in ingredients_list]) / len(ingredients_list)

    if storage_temp < 4:
        total_shelf_life *= 1.5
    elif storage_temp > 20:
        total_shelf_life *= 0.5

    return round(total_shelf_life, 1)

if st.button('Predict Shelf-life'):
    if ingredients:
        shelf_life = predict_spoilage(ingredients, storage_temp)
        st.write(f'Estimated Shelf-life: {shelf_life} days')
    else:
        st.write('Please enter ingredients.')


# HACCP Risk Assessment Section
st.subheader('HACCP Risk Assessment')
process_description = st.text_area('Describe your food process')

def generate_haccp_plan(process_description):
    critical_points = {
        'baking': ['Raw eggs', 'Undercooked meat'],
        'packaging': ['Contaminated packaging', 'Dirty surfaces'],
        'frying': ['Hot oil splashes', 'Cross-contamination']
    }

    process = process_description.lower()
    detected_points = []
    for key, risks in critical_points.items():
        if key in process:
            detected_points.extend(risks)

    if detected_points:
        return f"Critical Points: {', '.join(set(detected_points))}. Implement proper sanitation and cooking standards."

    return "No critical control points detected. Ensure good manufacturing practices."

if st.button('Generate HACCP Plan'):
    if process_description:
        haccp_plan = generate_haccp_plan(process_description)
        st.write(haccp_plan)
    else:
        st.write('Please describe your food process.')
