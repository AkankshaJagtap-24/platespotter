import requests

# Define the region for Indian license plates
regions = ['in']

# Provide the path to the image file
image_path = 'C:/Users/NITIN/Documents/Vehicle-Plate-Recognition-main/cut.jpg'

# Read the image file as binary data
with open(image_path, 'rb') as fp:
    # Make a POST request to the Plate Recognizer API
    response = requests.post(
        'https://api.platerecognizer.com/v1/plate-reader/',
        data=dict(regions=regions),
        files=dict(upload=fp),
        headers={'Authorization': 'Token eea3f25dd03596bb429aab3de722fa70f83b0ef7'}
    )

# Parse the response JSON
data = response.json()

# Check if license plate information is present in the response
if 'results' in data and data['results']:
    # Extract and print the detected license plate(s)
    plates = [result['plate'] for result in data['results']]
    for plate in plates:
        print(plate)
else:
    print("No license plate detected.")
