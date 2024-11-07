from flask import Flask, jsonify, send_from_directory, request
import openai
import re
import os
from .config import Config
from flask_cors import CORS
from .droneflights import droneflights
import random
from datetime import date


# Initialize Flask app
app = Flask(__name__, static_folder='../react-drone/build', static_url_path='/')
CORS(app)

app.config.from_object(Config)


def ordinal_to_number(ordinal_word):
    ordinal_map = {
        "first": 1, "second": 2, "third": 3, "fourth": 4,
        "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
        "ninth": 9, "tenth": 10
    }
    return ordinal_map.get(ordinal_word, None)
# Mapping of subject keywords to fields in the droneflight records
subject_field_map = {
    "altitude": "altitude_m",
    "battery": "battery_level_pct",
    "speed": "drone_speed_mps",
    "heading": "heading_deg",
    "latitude": "latitude",
    "longitude": "longitude",
    "image": "image_id",
    "camera tilt": "camera_tilt_deg",
    "focal length": "focal_length_mm",
    "iso": "iso",
    "shutter speed": "shutter_speed",
    "aperture": "aperture",
    "color temperature": "color_temp_k",
    "file size": "file_size_mb",
    "gps accuracy": "gps_accuracy_m",
    "gimbal mode": "gimbal_mode",
    "subject detection": "subject_detection"
}

@app.route("/api/droneflights")
def index():
    return jsonify(droneflights)

@app.route("/api/query", methods=["POST"])
def process_query():
    try:
        # Extract the JSON data from the request
        data = request.get_json()

        # Check if data was received correctly
        if not data or 'query' not in data:
            return jsonify({"error": "No query found in request"}), 400

        query = data.get("query", "").lower()

        # Regex to find numbers or ordinals in the query
        match = re.search(r"\b(\d+|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\b", query)
        subject_match = re.search(r"\b(altitude|battery|speed|heading|latitude|longitude|camera tilt|focal length|iso|shutter speed|aperture|color temperature|file size|gps accuracy|gimbal mode|subject detection)\b", query)

        # Determine the record index and subject
        if match:
            number_text = match.group(1)
            if number_text.isdigit():
                index = int(number_text) - 1  # Convert 1-based index to 0-based
            else:
                index = ordinal_to_number(number_text) - 1

            # Ensure the index is within bounds
            if index < 0 or index >= len(droneflights):
                return jsonify({"response": f"No record found for the {number_text} entry."}), 200
        else:
            return jsonify({"response": "No valid number or ordinal found in query."}), 200

        if subject_match:
            subject = subject_match.group(1)
            field = subject_field_map.get(subject)
            record = droneflights[index]

            # Retrieve the requested data
            response_text = f"The {subject} for the {number_text} entry is {record.get(field, 'not available')}."
        else:
            response_text = f"I'm not sure which subject you're asking about in: {query}"

        return jsonify({"response": response_text})

    except Exception as e:
        # Print the error to the Flask console for debugging
        print("Error processing query:", e)
        return jsonify({"error": "An internal error occurred"}), 500



@app.route("/api/test", methods=["POST"])
def query():
    try:
        data = request.get_json()
        query = data.get("query", "").lower()
        # Set the OpenAI API key from the environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        # Call OpenAI API with the query
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Answer the following query: {query}",
            max_tokens=100
        )

        # Extract the generated text from the OpenAI response
        generated_text = response.choices[0].text.strip()
        return jsonify({"response": generated_text})


    except Exception as e:
        # Print the error to the Flask console for debugging
        print("Error processing query:", e)
        return jsonify({"error": "An internal error occurred"}), 500



# @app.route("/api/query", methods=["POST"])
# def process_query():
#     try:
#         # Extract the JSON data from the request
#         data = request.get_json()

#         # Check if data was received correctly
#         if not data:
#             return jsonify({"error": "No query found in request"}), 400

#         query = data.get("query", "").lower()

#         # # find the number of the record in the query
#         # prompt = f"Extract all numbers from the following sentence as a list. Sentence: '{query}'"


#         # # Call OpenAI API to process the query
#
#         # response = openai.ChatCompletion.create(
#         #     model="gpt-3.5-turbo",
#         #     messages=[{"role": "user", "content": prompt}]
#         # )



#         # Get the model's response text and extract numbers using regex
#         # extracted_text = response.choices[0].message["content"]

#          # Finds numbers and decimals
#         numbers = re.findall(r"\b(\d+(st|nd|rd|th)?|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\b", query)
#         # Convert number text to an index (1-based)
#         if numbers[0].isdigit():
#             index = int(numbers[0]) - 1  # Convert 1-based index to 0-based
#         else:
#             index = ordinal_to_number(numbers[0]) - 1 if ordinal_to_number(numbers[0]) else None

#         # Check each subject individually
#         if "altitude" in query:
#             subject = subject_field_map.get("altitude")
#             record = droneflights[index]
#             response_text = f"The altitude for the {index} entry is {record.get(subject, 'not available')}."
#         elif "battery" in query:
#             response_text = "The battery level of the drone is 85%."
#         elif "speed" in query:
#             response_text = "The drone's speed is 5.2 meters per second."
#         elif "heading" in query:
#             response_text = "The drone's heading is 180 degrees."
#         elif "latitude" in query:
#             response_text = "The latitude of the drone is 44.4280° N."
#         elif "longitude" in query:
#             response_text = "The longitude of the drone is 110.5885° W."
#         elif "camera tilt" in query:
#             response_text = "The camera tilt is set to -30 degrees."
#         elif "focal length" in query:
#             response_text = "The focal length is 35mm."
#         elif "iso" in query:
#             response_text = "The ISO setting is 200."
#         elif "shutter speed" in query:
#             response_text = "The shutter speed is 1/1000 sec."
#         elif "aperture" in query:
#             response_text = "The aperture is set to f/4."
#         elif "color temperature" in query:
#             response_text = "The color temperature is 5200K."
#         elif "image format" in query:
#             response_text = "The image format is RAW+JPEG."
#         elif "file size" in query:
#             response_text = "The file size is 27.1 MB."
#         elif "gps accuracy" in query:
#             response_text = "The GPS accuracy is 0.6 meters."
#         elif "gimbal mode" in query:
#             response_text = "The gimbal mode is Free."
#         elif "subject detection" in query:
#             response_text = "Subject detection is set to Yes."
#         else:
#             response_text = f"I'm not sure how to answer that. You asked: {query}"

#         return jsonify({"response": numbers})

#     except Exception as e:
#         # Print the error to the Flask console for debugging
#         print("Error processing query:", e)
#         return jsonify({"error": "An internal error occurred"}), 500


# Serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # If the path is a file (e.g., JS, CSS), return it from the build folder
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise, return the index.html
    else:
        return send_from_directory(app.static_folder, 'index.html')
