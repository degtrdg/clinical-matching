from gradio_client import Client
import pandas as pd
import requests
import numpy as np


api_url = 'https://huggingface.co/spaces/Arnav-Jain1/clinical-matching/app.py'


df = pd.read_csv(r"x_test2.csv")
df = df.iloc[:, 0]
# Assuming 'df' is now a Series after you've isolated the first column

# Extract the header; this is the name of the Series
header = [df.name]

# Extract the data; this skips the first element
data = [[item] for item in df.iloc[1:]]

# Combine into the desired format
result = {"headers": header, "data": data}

response = requests.post(api_url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Get the prediction from the response
    prediction = response.json()
    print(prediction)
else:
    # If the request failed, print the error
    print(f"Request failed: {response.status_code}")
    print(response.text)


# client = Client("http://0.0.0.0:7860")
# result = client.predict(result
# )
# print(result)