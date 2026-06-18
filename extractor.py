import fitz
import re
import pandas as pd
import config
import os

def normalize_year(year_str):
    if not year_str: return ""
    match = re.search(r'(\d{4})/\d{2}', str(year_str))
    if match: return match.group(1)
    match = re.search(r'\b(\d{4})\b', str(year_str))
    if match: return match.group(1)
    return str(year_str)

def clean_label(label):
    if not label: return ""
    # Remove footnotes like 1/, /1, 1 /
    label = re.sub(r'\s*/?\d+/?\s*$', '', str(label))
    label = label.strip().strip('.')
    label = re.sub(r'\s+', ' ', label)
    return label

def trace_log(msg):
    with open("extraction_trace.log", "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")

def extract_table(pdf_path, table_config, table_name):
    doc = fitz.open(pdf_path)
    target_table = None
    keywords = table_config["keywords"]
    
    trace_log(f"\n--- Extracting {table_name} ---")
    
    for i in range(len(doc)):
        text = doc[i].get_text()
        if all(kw in text for kw in keywords):
            tables = doc[i].find_tables()
            if tables.tables:
                for t_idx, table in enumerate(tables.tables):
                    extracted = table.extract()
                    flat_table = str(extracted).lower()
                    # Generic presence check
                    generic_match = any(x in flat_table for x in ["planted", "production", "crush", "yield", "beginning", "imports", "supply"])
                    if not generic_match:
                        continue
                    # Per-table discriminator: if config specifies 'discriminators', at least one must match
                    discriminators = table_config.get("discriminators", [])
                    if discriminators and not any(d.lower() in flat_table for d in discriminators):
                        trace_log(f"  Skipping table {t_idx} on page {i+1} (discriminator mismatch)")
                        continue
                    # Reject discriminators: if config specifies 'reject_if', skip if any match
                    reject_if = table_config.get("reject_if", [])
                    if reject_if and any(r.lower() in flat_table for r in reject_if):
                        trace_log(f"  Skipping table {t_idx} on page {i+1} (reject_if match)")
                        continue
                    target_table = extracted
                    trace_log(f"Found target table on page {i+1}, index {t_idx}")
                    break
        if target_table: break
            
    if not target_table: 
        trace_log(f"Table {table_name} NOT FOUND.")
        return None

    # Step 1: Find Year Header Row
    year_row_idx = -1
    headers = []
    for idx, row in enumerate(target_table):
        row_str = " ".join([str(c) for c in row if c])
        if re.search(r'\d{4}/\d{2}', row_str):
            year_row_idx = idx
            headers = [str(c) if c else "" for c in row]
            trace_log(f"Year Header Row found at index {idx}: {headers}")
            break
    
    if year_row_idx == -1: return None

    # Step 2: Map Years to Columns
    years = []
    col_to_year = {}
    last_year = ""
    for col_idx, h in enumerate(headers):
        y = normalize_year(h)
        if y:
            years.append(y)
            last_year = y
            col_to_year[col_idx] = y
        elif last_year and any(char.isdigit() for char in h):
            col_to_year[col_idx] = last_year
            
    # Step 3: Extract Data using Greedy Consumer Logic
    table_data = {} # {label: {year: value}}
    
    remaining_rows = []
    for idx in range(year_row_idx + 1, len(target_table)):
        row = target_table[idx]
        has_data = any(str(row[c_idx]).strip() for c_idx in col_to_year.keys())
        label_cell = ""
        for c_idx in [0, 1]:
            if c_idx < len(row) and row[c_idx]:
                label_cell = str(row[c_idx])
                break
        if label_cell or has_data:
            remaining_rows.append({"label_cell": label_cell, "row": row, "has_data": has_data, "orig_idx": idx})

    row_ptr = 0
    while row_ptr < len(remaining_rows):
        current = remaining_rows[row_ptr]
        label_cell = current["label_cell"]
        
        if not label_cell:
            row_ptr += 1
            continue

        sub_labels = [clean_label(l) for l in label_cell.split("\n") if l.strip()]
        if not sub_labels or sub_labels[0].replace(".","").isdigit():
            row_ptr += 1
            continue

        trace_log(f"Processing label block at Row {current['orig_idx']}: {sub_labels}")

        first_col_val = str(current["row"][list(col_to_year.keys())[0]])
        if "\n" in first_col_val and len(first_col_val.split("\n")) >= len(sub_labels):
            # Corn/Wheat style
            trace_log("Detected Merged Style")
            for label in sub_labels:
                if label not in table_data: table_data[label] = {}
                for col_idx, year in col_to_year.items():
                    val_cell = str(current["row"][col_idx])
                    vals = [v.replace(",", "").strip() for v in val_cell.split("\n")]
                    idx = sub_labels.index(label)
                    val = vals[idx] if idx < len(vals) else ""
                    table_data[label][year] = val
                    trace_log(f"  Captured (Merged): {label} [{year}] = {val}")
            row_ptr += 1
        else:
            # Hybrid / Row-by-Row
            trace_log("Detected Sequential Style")
            for label in sub_labels:
                consumed = False
                search_ptr = row_ptr
                while search_ptr < len(remaining_rows):
                    cand = remaining_rows[search_ptr]
                    if cand["has_data"]:
                        if label not in table_data: table_data[label] = {}
                        for col_idx, year in col_to_year.items():
                            val = str(cand["row"][col_idx]).replace(",", "").strip()
                            if val: 
                                table_data[label][year] = val
                                trace_log(f"  Captured (Seq): {label} [{year}] = {val}")
                        row_ptr = search_ptr + 1
                        consumed = True
                        break
                    search_ptr += 1
                if not consumed:
                    trace_log(f"  Warning: No data row found for label: {label}")
                    row_ptr += 1

    # Step 4: Map to Configuration
    results = []
    mapping = table_config["mapping"]
    
    # Pre-calculate clean labels for matching
    clean_mappings = []
    for cfg_label, cfg_code in mapping.items():
        clean_mappings.append({
            "cfg_label": cfg_label,
            "clean_cfg": clean_label(cfg_label).lower(),
            "cfg_code": cfg_code
        })

    for y in sorted(list(set(years))):
        row_dict = {"Year": y}
        # Initialize all codes to empty string
        for code in mapping.values():
            row_dict[code] = ""
            
        for cm in clean_mappings:
            cfg_label = cm["cfg_label"]
            clean_cfg = cm["clean_cfg"]
            cfg_code = cm["cfg_code"]
            
            # If we already have a value for this code in this year, don't overwrite with blank
            if row_dict.get(cfg_code):
                continue

            best_match_val = ""
            best_match_type = 0 # 0: None, 1: Fuzzy, 2: Partial, 3: Exact
            
            for extracted_label, year_vals in table_data.items():
                ext_clean = extracted_label.lower()
                val = year_vals.get(y, "")
                if not val: continue
                
                match_type = 0
                if clean_cfg == ext_clean:
                    match_type = 3
                elif clean_cfg == "biodiesel" and "biodiesel" in ext_clean:
                    match_type = 2
                elif clean_cfg == "biofuel" and "biofuel" in ext_clean:
                    match_type = 2
                elif len(clean_cfg) > 10 and (clean_cfg in ext_clean or ext_clean in clean_cfg):
                    match_type = 1
                
                if match_type > best_match_type:
                    best_match_type = match_type
                    best_match_val = val
                    if match_type == 3: break # Exact match found
            
            if best_match_val:
                row_dict[cfg_code] = best_match_val
                
        results.append(row_dict)
        
    return pd.DataFrame(results)

def extract_all(pdf_path):
    if os.path.exists("extraction_trace.log"): os.remove("extraction_trace.log")
    all_year_data = {} # {year: {code: val}}
    for table_name, table_config in config.TABLE_CONFIGS.items():
        print(f"Extracting {table_name}...")
        df = extract_table(pdf_path, table_config, table_name)
        if df is not None and not df.empty:
            for _, row in df.iterrows():
                year = row["Year"]
                if year not in all_year_data: all_year_data[year] = {}
                for col in df.columns:
                    if col != "Year" and str(row[col]).strip():
                        if not all_year_data[year].get(col):
                            all_year_data[year][col] = row[col]
    
    if not all_year_data: return None
    
    final_rows = []
    for year in sorted(all_year_data.keys()):
        row_dict = {"Year": year}
        for code, desc in config.ABSOLUTE_COLUMNS:
            row_dict[code] = all_year_data[year].get(code, "")
        final_rows.append(row_dict)
    
    final_df = pd.DataFrame(final_rows)
    final_df.set_index("Year", inplace=True)
    return final_df

if __name__ == "__main__":
    pdf_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\Samplepdfs\2026AOF-grains-oilseeds-outlook.pdf'
    if os.path.exists(pdf_path):
        df = extract_all(pdf_path)
        if df is not None:
            print(f"\nExtraction complete. Log saved to extraction_trace.log")
