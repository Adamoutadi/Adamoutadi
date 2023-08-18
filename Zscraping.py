# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 13:46:23 2023

@author: ZAM0335
"""

import pdfplumber
import pandas as pd
import re

# Define a function to extract numeric values from strings using regular expressions
def process_values(values):
    processed_values = []
    for value in values:
        parts = re.findall(r'\d{3}|\d+\.\d+', value)
        processed_values.extend(parts)
    return processed_values

# Define the path to the PDF file and a list of target headers
pdf_path = r'\\tedfil01\DataDropDev\PythonPOC\Adam M\Wheat May 5.pdf'

# Initialize variables to track header and data capture
found_header = False
capturing_data = False
extracted_data = []

# Initialize variable to store the matching row index
matching_index = None

# Open the PDF and extract text
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    page_text = page.extract_text()
    lines = page_text.split('\n')

    # Process each line of text
    for index, line in enumerate(lines):
        # Check if the line contains "2SRW"
        if "2SRW" in line:
            found_header = True
            capturing_data = True
            matching_index = index  # Store the matching row index
            extracted_data.append(line)
            continue

        # Capture data if a target header was found
        if capturing_data and line.strip() and len(extracted_data) < 4:
            extracted_data.append(line.strip())

# Print the extracted data
for line in extracted_data:
    print(line)

# Create DataFrame using the matching row and the next five rows
if matching_index is not None:
    df = pd.DataFrame({"Value": lines[matching_index:matching_index + 6]})

    print("DataFrame with matching row and the next five rows:")
    print(df)
else:
    print("No matching row found.")

# Modify the DataFrame by replacing a value in the second row
if len(df) >= 2:
    df.at[1, "Value"] = "USFob     prem    $/mt    PNW   prem    $/mt    prem    $/mt    Lakes    PNW"

print("Modified DataFrame:")
print(df)









# Initialize a dictionary to store new data
new_data = {
    "USFOB": [],
    "Prem": [],
    "$/mt": [],
    "PNW": [],
    "Prem_values": [],
    "mt_prem": [],
    "Prem_next": [],
    "mt_next": [],
    "Lakes": [],
    "PNW_next": []
}

# Process rows in the DataFrame to extract specific values
if len(df) >= 6:
    for index in range(2, 6):
        row_value = df.at[index, "Value"]
        row_values = row_value.split()
        new_data["USFOB"].append(row_values[0])
        new_data["Prem"].append(row_values[1] if len(row_values) > 1 else '')
        new_data["$/mt"].append(row_values[2] if len(row_values) > 2 else '')
        new_data["PNW"].append(row_values[3] if len(row_values) > 3 else '')
        prem_values = row_values[4:] if len(row_values) > 4 else []
        new_data["Prem_values"].append(prem_values[0] if prem_values else '')
        new_data["mt_prem"].append(prem_values[1] if len(prem_values) > 1 else '')
        new_data["Prem_next"].append(prem_values[2] if len(prem_values) > 2 else '')
        new_data["mt_next"].append(prem_values[3] if len(prem_values) > 3 else '')
        new_data["Lakes"].append(prem_values[4] if len(prem_values) > 4 else '')
        new_data["PNW_next"].append(prem_values[5] if len(prem_values) > 5 else '')

# Create a new DataFrame using the extracted data
new_df = pd.DataFrame(new_data)

print("New DataFrame with extracted USFOB, Prem, $/mt, PNW, Prem_values, mt_prem, Prem_next, mt_next, Lakes, and PNW_next values:")
print(new_df)








# Search for another specific header and create another DataFrame
matching_index = None
for index, line in enumerate(lines):
    if "CWRS 13.5" in line:
        matching_index = index
        break

if matching_index is not None:
    # Create a DataFrame using specific rows
    df_additional = pd.DataFrame({"Value": lines[matching_index + 1:matching_index + 6]})

    print("DataFrame with matching row and the next five rows:")
    print(df_additional)
else:
    print("No matching row found.")

# Modify the new DataFrame by updating the first row of the "Value" column
#if not df_additional.empty:

#    new_first_row = "VCVR UpRiver WA SA 14pro 12.5pro 12.5pro 12pro 11.5pro 11.5pro"
#    df_additional.at[df_additional.index[0], "Value"] = new_first_row


#print("Modified DataFrame with the first row of the Value column updated:")
#print(df_additional)

# Extract "Other Fob" values starting from the second row
# Extract "Other Fob" values starting from the second row
other_fob_values = {
    "Other Fob": [row.split()[0] for row in df_additional.loc[1:, "Value"]]
}

# Create a DataFrame with extracted "Other Fob" values
other_fob_df = pd.DataFrame(other_fob_values)

print("DataFrame with extracted 'Other Fob' values:")
print(other_fob_df)

selected_other_fob_words = other_fob_df["Other Fob"].tolist()



def process_pro(value):
    parts = value.split()
    new_parts = []
    i = 0
    while i < len(parts):
        if i < len(parts) - 1 and parts[i+1] == "pro":
            new_parts.append(parts[i] + "pro")
            i += 2
        else:
            new_parts.append(parts[i])
            i += 1
    return " ".join(new_parts)



# Apply the process_pro function to the "Value" column
df_additional["Value"] = df_additional["Value"].apply(process_pro)

# Split and organize the data within the "Value" column into separate columns
df_split = df_additional["Value"].str.split(expand=True)

# Keep the first row as is and assign headers to the split DataFrame columns
df_split.columns = df_split.iloc[0]
df_split = df_split[1:]  # Remove the first row (redundant headers)

print("DataFrame with split and organized data:")
print(df_split)


