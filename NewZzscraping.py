# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 08:42:39 2023

@author: ZAM0335
"""

import pdfplumber
import pandas as pd
import re

# Define a function to split 9-digit values into three 3-digit values
def split_9_digit_values(value):
    return re.sub(r'(\d{3})(\d{3})(\d{3})', r'\1 \2 \3', value)

# Define the path to the PDF file and a list of target headers
pdf_path = r'\\tedfil01\DataDropDev\PythonPOC\Adam M\Wheat Aug 24.pdf'

# Open the PDF and extract text
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    page_text = page.extract_text()
    lines = page_text.split('\n')

    # Find the index of the matching row
    matching_index = None
    for index, line in enumerate(lines):
        if "2SRW" in line:
            matching_index = index
            break

# Create DataFrame using the matching row and the next five rows
if matching_index is not None:
    data_rows = [line.strip() for line in lines[matching_index:matching_index + 6]]
    df = pd.DataFrame({"Value": data_rows})

    print("DataFrame with matching row and the next five rows:")
    print(df)
else:
    print("No matching row found.")

# Split 9-digit values into three 3-digit values in rows with 9-digit values
for index, row in df.iterrows():
    if re.search(r'\b\d{9}\b', row['Value']):
        df.at[index, "Value"] = split_9_digit_values(row['Value'])

print("DataFrame after splitting 9-digit values:")
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


# Define the new headers and their corresponding values
new_headers = ["USFOB", "Prem", "$/mt", "PNW", "Prem_values", "mt_prem", "Prem_next", "mt_next", "Lakes", "PNW_next"]
new_values = ["", "2SRWGulf", "", "White Wht", "HRW 11/12.5 Gulf", "", "HRW 12/13.5 Gulf", "", "2HRS 13.5 pro", "2HRS 13.5 pro2nd"]

# Add the new row with headers and values to the top of the DataFrame
new_row = pd.DataFrame([new_values], columns=new_headers)
new_df = pd.concat([new_row, new_df], ignore_index=True)







import re

# Initialize a list to store lines containing month codes between dashes
lines_with_month_codes = []

# Search for lines with month codes between dashes
for line in lines:
    matches = re.findall(r'-(\w{3})-', line)
    if matches:
        formatted_line = re.sub(r'-(\w{3})-', r'-\1-', line)  # Format month code as two-digit number
        lines_with_month_codes.append(formatted_line)

# Store lines with month codes between dashes in Date_value variable
Date_value = "\n".join(lines_with_month_codes)

# Print lines with month codes between dashes
print("Line containing month codes between dashes:")
print(Date_value)



# Select the first row as column names
cols_to_keep = new_df.iloc[0, :].tolist()

# Filter the desired columns
desired_columns = ['2SRWGulf', 'White Wht', 'HRW 11/12.5 Gulf', 'HRW 12/13.5 Gulf', '2HRS 13.5 pro', '2HRS 13.5 pro2nd']
filtered_columns_indices = [cols_to_keep.index(col) for col in desired_columns]

# Extract the values from the rows under the desired columns
values = new_df.values[1:, filtered_columns_indices]

# Create a new DataFrame in the desired format
final_data = []

for i, col_name in enumerate(desired_columns):
    for value in values[:, i]:
        if pd.notna(value):  # Skip empty cases
            final_data.append([col_name, value])

finaloutput = pd.DataFrame(final_data, columns=['Market_price_group_name', 'Base Market price'])

# Print the finaloutput DataFrame
print(finaloutput)

# Initialize a list to store lines containing month codes between dashes
lines_with_month_codes = []

# Search for lines with month codes between dashes
for line in lines:
    matches = re.findall(r'-(\w{3})-', line)
    if matches:
        formatted_line = re.sub(r'-(\w{3})-', r'-\1-', line)  # Format month code as two-digit number
        lines_with_month_codes.append(formatted_line)

# Store lines with month codes between dashes in Date_value variable
Date_value = "\n".join(lines_with_month_codes)

# Add a new column 'COB Date' to the DataFrame and populate it with Date_value
finaloutput['COB Date'] = Date_value

# Print the updated DataFrame
print(finaloutput)



# Extract the month codes from the USFOB column in new_df
month_mapping = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

# Find the index where the months start
start_index = new_df[new_df['USFOB'] == ''].index[0] + 1

# Iterate through the desired columns and create Trading Period for each
for col in desired_columns:
    month_column = new_df.loc[start_index:, 'USFOB']  # Extract months starting from start_index
    trading_periods = month_column.apply(lambda x: f"{month_mapping[x[:3]]}-20")
    
    # Add Trading Period to the corresponding rows in finaloutput
    finaloutput.loc[finaloutput['Market_price_group_name'] == col, 'Trading Period'] = trading_periods.values

# Print the updated DataFrame
print(finaloutput)

# Convert COB Date to datetime format
finaloutput['COB Date'] = pd.to_datetime(finaloutput['COB Date'])

# Iterate through the rows and update Trading Period year
for index, row in finaloutput.iterrows():
    trading_period_parts = row['Trading Period'].split('-')
    updated_trading_period = f"{trading_period_parts[0]}-{row['COB Date'].year % 100:02d}"
    finaloutput.at[index, 'Trading Period'] = updated_trading_period

# Print the updated DataFrame
print(finaloutput)

# Define the path to save the Excel file
output_path = r'\\tedfil01\DataDropDev\PythonPOC\Adam M\finaloutput.xlsx'

# Save the DataFrame to an Excel file
finaloutput.to_excel(output_path, index=False)

print("Excel file saved successfully.")






 #######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
v#######################################################################################################
#######################################################################################################



















matching_index = None
for index, line in enumerate(lines):
    if "CWRS 13.5" in line:
        matching_index = index
        break

if matching_index is not None:
    df_additional = pd.DataFrame({"Value": lines[matching_index + 1:matching_index + 6]})

    second_row_value = df_additional.at[1, "Value"]
    third_row_month = next((month for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] if month in df_additional.at[2, "Value"]), None)

    if third_row_month and not third_row_month in second_row_value:
        month_index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(third_row_month)
        previous_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][month_index - 1]
        df_additional.at[1, "Value"] = f"{previous_month} {second_row_value}"

    print("DataFrame with matching row and the next five rows:")
    print(df_additional)

    other_fob_values = {
        "Other Fob": [row.split()[0] for row in df_additional.loc[1:, "Value"]]
    }

    other_fob_df = pd.DataFrame(other_fob_values)

    df_additional["Value"] = df_additional["Value"].apply(lambda row: ' '.join(row.split()[1:]))

    # Process the "Value" column to handle dashes consistently using regular expressions
    df_additional["Value"] = df_additional["Value"].apply(lambda row: re.sub(r'(\d+)-(\d+)', r'\1 - \2', row))

    print("DataFrame with extracted 'Other Fob' values:")
    print(other_fob_df)
    print("Modified DataFrame with the first row of the Value column updated:")
    print(df_additional)

else:
    print("No matching row found.")
    
def process_dashes(row):
    items = row.split()
    processed_items = []

    for item in items:
        if item == '--':
            processed_items.extend(['-', '-'])
        elif '-' in item and item.count('-') > 1:
            processed_items.extend(item.split('-'))
        else:
            processed_items.append(item)
    
    return ' '.join(processed_items)

df_additional["Value"] = df_additional["Value"].apply(process_dashes)

print("DataFrame with matching row and the next five rows after handling dashes:")
print(df_additional)


def split_large_numbers(row):
    items = row.split()
    processed_items = []

    for item in items:
        if len(item) == 9 and item.isdigit():
            parts = [item[i:i+3] for i in range(0, 9, 3)]
            processed_items.extend(parts)
        else:
            processed_items.append(item)

    return ' '.join(processed_items)

df_additional["Value"] = df_additional["Value"].apply(split_large_numbers)

print("DataFrame with matching row and the next five rows after splitting large numbers:")
print(df_additional)






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

def process_first_row(value):
    parts = value.split()
    if parts[0] == "Up" and parts[1] == "River":
        parts = ["VCVR", "UpRiver"] + parts[2:]
    return ' '.join(parts)

# Apply the process_first_row function to the first row of the "Value" column in df_additional
df_additional.at[df_additional.index[0], "Value"] = process_first_row(df_additional.at[df_additional.index[0], "Value"])


# Split and organize the data within the "Value" column into separate columns
df_split = df_additional["Value"].str.split(expand=True)

# Keep the first row as is and assign headers to the split DataFrame columns
df_split.columns = df_split.iloc[0]
df_split = df_split[1:]  # Remove the first row (redundant headers)


# Apply the process_pro function to the "Value" column
df_additional["Value"] = df_additional["Value"].apply(process_pro)

# Split and organize the data within the "Value" column into separate columns
df_split = df_additional["Value"].str.split(expand=True)

# Keep the first row as is and assign headers to the split DataFrame columns
df_split.columns = df_split.iloc[0]
df_split = df_split[1:]  # Remove the first row (redundant headers)

print("DataFrame with split and organized data:")
print(df_split)

# Set the index of other_fob_df to match the index of df_split
other_fob_df.index = df_split.index

# Add the "Other Fob" column from other_fob_df to df_split
df_split['Other Fob'] = other_fob_df['Other Fob']

# Print the updated df_split DataFrame
print(df_split)