# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:17:35 2023

@author: ZAM0335
"""


import pdfplumber
import re
import pandas as pd

# Define the path to the PDF file and a list of target headers
pdf_path = r'\\tedfil01\DataDropDev\PythonPOC\Adam M\brokers report\Agribrokers2.pdf'

# Create lists to store lines containing "gmo" and "Wheaat"
gmo_lines = []
wheat_lines = []

# Open the PDF and extract text
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    page_text = page.extract_text()
    lines_text = page_text.split('\n')

    # Find the index of the line containing the keyword "gmo"
    gmo_index = None
    for index, line in enumerate(lines_text):
        if "gmo" in line.lower():
            gmo_index = index
            break

    if gmo_index is not None:
        # Append lines before and after "gmo" to gmo_lines list
        if gmo_index > 0:
            gmo_lines.append(lines_text[gmo_index - 1])
        gmo_lines.append(lines_text[gmo_index])
        
        # Find and append lines containing month codes after "gmo"
        month_codes = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for index in range(gmo_index + 1, len(lines_text)):
            line = lines_text[index]
            if any(month in line for month in month_codes):
                gmo_lines.append(line)
            elif "gmo" in line.lower():
                break
            else:
                break

    # Find the index of the line containing the keyword "Wheaat"
    wheat_index = None
    for index, line in enumerate(lines_text):
        if "wheat" in line.lower():
            wheat_index = index
            break

    if wheat_index is not None:
        # Append line with "Wheaat" to wheat_lines list
        wheat_lines.append(lines_text[wheat_index])
        
        # Find and append lines containing month codes after "Wheaat"
        for index in range(wheat_index + 1, len(lines_text)):
            line = lines_text[index]
            if any(month in line for month in month_codes):
                wheat_lines.append(line)
            else:
                break

#if statment to sepratt gmoa nd non gmo uinder 