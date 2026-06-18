import fitz
import re
import pandas as pd
import os
import config

def normalize_year(year_str):
    if not year_str: return ""
    match = re.search(r'(\d{4})/\d{2}', str(year_str))
    if match: return match.group(1)
    return str(year_str)

def clean_label(label):
    if not label: return ""
    label = re.sub(r'\s*/?\d+/?$', '', str(label)).strip()
    return label

def extract_soybean_perfected(pdf_path):
    doc = fitz.open(pdf_path)
    # Soybean is usually on page 7 or search for "Soybean Supply"
    target_table = None
    for i in range(len(doc)):
        if "Soybean Supply, Demand, and Price" in doc[i].get_text():
            tables = doc[i].find_tables()
            if tables.tables:
                target_table = tables.tables[0].extract()
                break
    
    if not target_table:
        print("Soybean table not found.")
        return None

    # Find Year Header
    year_row_idx = -1
    for idx, row in enumerate(target_table):
        row_str = " ".join([str(c) for c in row if c])
        if re.search(r'\d{4}/\d{2}', row_str):
            year_row_idx = idx
            headers = [str(c) if c else "" for c in row]
            break
            
    # Map years to columns
    years = []
    year_to_cols = {}
    for col_idx, h in enumerate(headers):
        y = normalize_year(h)
        if y:
            years.append(y)
            year_to_cols[y] = col_idx

    # Find Label Block
    label_block_row_idx = -1
    labels = []
    for idx in range(year_row_idx + 1, len(target_table)):
        row = target_table[idx]
        # Label block is usually the first row with a lot of \n
        cell = str(row[0]) if row[0] else ""
        if "\n" in cell and "Area planted" in cell:
            label_block_row_idx = idx
            labels = [clean_label(l) for l in cell.split("\n") if l.strip()]
            break
            
    if not labels:
        print("Could not find Soybean label block.")
        return None

    print(f"Found {len(labels)} Soybean labels.")
    
    # Collect values
    # We need to find the next N non-empty data rows
    data_rows = []
    for idx in range(label_block_row_idx + 1, len(target_table)):
        row = target_table[idx]
        # Check if row has any numerical values in year columns
        has_data = False
        for y in years:
            c_idx = year_to_cols[y]
            val = str(row[c_idx]) if row[c_idx] else ""
            if any(char.isdigit() for char in val):
                has_data = True
                break
        
        if has_data:
            data_rows.append(row)
        
        if len(data_rows) == len(labels):
            break

    print(f"Collected {len(data_rows)} data rows for Soybean.")

    # Build Results
    results = []
    for y in years:
        row_dict = {"Year": y}
        c_idx = year_to_cols[y]
        for i, label in enumerate(labels):
            val = ""
            if i < len(data_rows):
                val = str(data_rows[i][c_idx]).replace(",", "").strip()
            row_dict[label] = val
        results.append(row_dict)
        
    return pd.DataFrame(results)

if __name__ == "__main__":
    pdf_2026 = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\Samplepdfs\2026AOF-grains-oilseeds-outlook.pdf'
    df = extract_soybean_perfected(pdf_2026)
    if df is not None:
        print("\nPerfected Soybean Extraction (2026 PDF):")
        print(df.to_string(index=False))
        
        # Verify against mapping
        mapping = config.TABLE_CONFIGS["SOYBEAN"]["mapping"]
        print("\nMapping Audit:")
        for label, code in mapping.items():
            found = False
            for col in df.columns:
                if label in col or col in label:
                    val_2026 = df[df["Year"] == "2026"][col].values[0]
                    print(f"OK: {label} -> {code} | Value 2026: {val_2026}")
                    found = True
                    break
            if not found:
                print(f"MISSING: {label}")
