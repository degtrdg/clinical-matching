from gradio_client import Client
import pandas as pd

# Read the data frame and get the first column 
df = pd.read_csv(r"x_test2.csv")
df = df.iloc[:, 0]
# Assuming 'df' is now a Series after you've isolated the first column

# Extract the header; this is the name of the Series
header = [df.name]

# Extract the data; this skips the first element
data = [[item] for item in df.iloc[1:]]

# Combine into the desired format
result = {"headers": header, "data": data}

#Set the client and then pass the info
client = Client("https://arnav-jain1-clinical-matching.hf.space/--replicas/9nhzd/")
result = client.predict(result, 
                        api_name="/predict" 
)

#Print the result
print(result)