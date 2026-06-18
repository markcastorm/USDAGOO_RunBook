import fitz
import re
import pandas as pd
import os
import config

def normalize_year(year_str):
    if not year_str: return ""
    match = re.search(r'(\d{4})/\d{2}', str(year_str))
    if match:
        return match.group(1)
    # Check for 4 digit year
    match = re.search(r'\b(\d{4})\b', str(year_str))
    if match:
        return match.group(1)
    return str(year_str)

def clean_label(label):
    if not label: return ""
    # Remove footnotes like "1/", "3/", "/1", "/2"
    label = re.sub(r'\s*/?\d+/?$', '', str(label)).strip()
    return label

def extract_table_generic(pdf_path, table_config):
    doc = fitz.open(pdf_path)
    target_table = None
    
    keywords = table_config["keywords"]
    
    for i in range(len(doc)):
        text = doc[i].get_text()
        if all(kw in text for kw in keywords):
            tables = doc[i].find_tables()
            if tables.tables:
                for table in tables.tables:
                    extracted = table.extract()
                    # Look for "Area planted" or "Production" to confirm it's the right table
                    if any("Area planted" in str(row) or "Production" in str(row) for row in extracted):
                        target_table = extracted
                        break
        if target_table:
            break
            
    if not target_table:
        return None

    # Identify Year Columns and Labels Column
    # Filter out completely empty rows/cols
    df_raw = pd.DataFrame(target_table)
    df_raw = df_raw.dropna(how='all').dropna(axis=1, how='all')
    
    # Re-extract years and data
    headers = []
    data_rows = []
    
    # Strategy: 
    # Find the row containing years (e.g. 2023/24)
    # Find the column containing labels (the one with the most text)
    
    year_row_idx = -1
    for idx, row in df_raw.iterrows():
        if any(re.search(r'\d{4}/\d{2}', str(cell)) for cell in row):
            year_row_idx = idx
            headers = [str(c) if c else "" for c in row]
            break
            
    if year_row_idx == -1:
        # Fallback: first row
        headers = [str(c) if c else "" for c in df_raw.iloc[0]]
        year_row_idx = 0

    # Identify Label Column (usually the first one with significant text)
    label_col_idx = -1
    for col_idx in range(df_raw.shape[1]):
        col_content = " ".join([str(x) for x in df_raw.iloc[:, col_idx] if x])
        if "Area planted" in col_content or "Production" in col_content:
            label_col_idx = col_idx
            break
            
    if label_col_idx == -1: label_col_idx = 0
    
    # Extract Years
    years = []
    year_to_col = {}
    for col_idx, h in enumerate(headers):
        y = normalize_year(h)
        if y and col_idx != label_col_idx:
            years.append(y)
            year_to_col[y] = col_idx
            
    # If years are missing from header, they might be in the same cell as labels or elsewhere
    # but based on probes, they are in the header row.

    # Extract Labels and Values
    # Case 1: All labels and values are merged with \n in one or two rows
    # Case 2: Labels and values are in separate rows
    
    raw_labels = []
    raw_values = {y: [] for y in years}
    
    for idx in range(year_row_idx + 1, df_raw.shape[1]): # Wait, should be range(df_raw.shape[0])
        pass
    
    # Let's use a simpler approach: iterate all rows below year header
    for idx in range(year_row_idx + 1, df_raw.shape[0]):
        row = df_raw.iloc[idx]
        label_cell = str(row[label_col_idx]) if row[label_col_idx] else ""
        
        if '\n' in label_cell:
            # Merged labels
            split_labels = [clean_label(l) for l in label_cell.split('\n') if l.strip()]
            raw_labels.extend(split_labels)
            for y in years:
                col_idx = year_to_col[y]
                val_cell = str(row[col_idx]) if row[col_idx] else ""
                split_vals = [v.replace(',', '').strip() for v in val_cell.split('\n')]
                # Pad split_vals if needed, though they usually match
                raw_values[y].extend(split_vals)
        else:
            # Single row label
            l = clean_label(label_cell)
            if l:
                raw_labels.append(l)
                for y in years:
                    col_idx = year_to_col[y]
                    val = str(row[col_idx]).replace(',', '').strip() if row[col_idx] else ""
                    raw_values[y].append(val)

    # Build Final DataFrame
    final_data = []
    for y in years:
        row_dict = {"Year": y}
        for i, l in enumerate(raw_labels):
            if i < len(raw_values[y]):
                row_dict[l] = raw_values[y][i]
        final_data.append(row_dict)
        
    return pd.DataFrame(final_data)

def run_tests():
    sample_dir = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\Samplepdfs'
    pdf_files = [f for f in os.listdir(sample_dir) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        print(f"\n{'='*50}")
        print(f"TESTING PDF: {pdf_file}")
        print(f"{'='*50}")
        
        pdf_path = os.path.join(sample_dir, pdf_file)
        
        for table_name, table_config in config.TABLE_CONFIGS.items():
            print(f"\n--- Table: {table_name} ---")
            df = extract_table_generic(pdf_path, table_config)
            if df is not None and not df.empty:
                # print(df.to_string(index=False))
                
                # Check mapping coverage
                mapping = table_config["mapping"]
                matched = 0
                for label, code in mapping.items():
                    if any(label in col or col in label for col in df.columns):
                        matched += 1
                
                print(f"Result: SUCCESS ({matched}/{len(mapping)} fields matched)")
                if matched < len(mapping):
                    print(f"Missing fields: {[l for l in mapping.keys() if not any(l in col or col in label for col in df.columns)]}")
            else:
                print("Result: FAILED (Table not found or extraction empty)")

if __name__ == "__main__":
    run_tests()
