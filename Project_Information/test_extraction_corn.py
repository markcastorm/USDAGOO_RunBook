import fitz
import re
import pandas as pd
import os
import config

def normalize_year(year_str):
    # Matches 2023/24 or 2025/26 1/
    match = re.search(r'(\d{4})/\d{2}', year_str)
    if match:
        return match.group(1)
    return year_str

def extract_corn_table(pdf_path):
    doc = fitz.open(pdf_path)
    target_table = None
    target_page_num = -1
    
    # Search for the table
    for i in range(len(doc)):
        text = doc[i].get_text()
        if "Corn Supply, Demand, and Price" in text:
            tables = doc[i].find_tables()
            if tables.tables:
                for table in tables.tables:
                    # Check if the table header or first row contains relevant keywords
                    extracted = table.extract()
                    if any("Area planted" in str(row) for row in extracted):
                        target_table = extracted
                        target_page_num = i + 1
                        break
        if target_table:
            break
            
    if not target_table:
        print("Corn table not found.")
        return None

    print(f"Found Corn table on page {target_page_num}")
    
    # Process the extracted table
    # Based on probe, Row 0 is headers, Row 1 contains merged data
    headers = target_table[0]
    data_row = target_table[1]
    
    years = [normalize_year(h) for h in headers[1:]]
    labels = data_row[0].split('\n')
    
    extracted_data = []
    for col_idx in range(1, len(data_row)):
        values = data_row[col_idx].split('\n')
        extracted_data.append(values)
        
    # Build dictionary
    results = []
    for i, year in enumerate(years):
        year_data = {"Year": year}
        for j, label in enumerate(labels):
            # Clean label from footnotes like "Ethanol 3/"
            clean_label = re.sub(r'\s*\d+/$', '', label).strip()
            if i < len(extracted_data) and j < len(extracted_data[i]):
                val = extracted_data[i][j].replace(',', '').strip()
                year_data[clean_label] = val
        results.append(year_data)
        
    df = pd.DataFrame(results)
    return df

if __name__ == "__main__":
    pdf_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\Samplepdfs\2026AOF-grains-oilseeds-outlook.pdf'
    df = extract_corn_table(pdf_path)
    if df is not None:
        print("\nExtracted Corn Data:")
        print(df.to_string(index=False))
        
        # Test mapping
        corn_config = config.TABLE_CONFIGS["CORN"]
        mapping = corn_config["mapping"]
        
        print("\nMapping Verification:")
        for label, code in mapping.items():
            if label in df.columns:
                print(f"PASS: {label} -> {code}")
            else:
                # Try partial match or fuzzy match
                found = False
                for col in df.columns:
                    if label in col or col in label:
                        print(f"PARTIAL PASS: '{col}' matched to config '{label}' -> {code}")
                        found = True
                        break
                if not found:
                    print(f"FAIL: {label} not found in extracted columns")
