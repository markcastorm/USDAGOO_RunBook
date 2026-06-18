import os
import xlwt
import datetime
import zipfile
import shutil
import pandas as pd
import re
import config

def parse_pdf_date(date_str):
    # D:20260217111928-05'00'
    if not date_str: return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    match = re.search(r'D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})', str(date_str))
    if match:
        groups = match.groups()
        return f"{groups[0]}-{groups[1]}-{groups[2]}T{groups[3]}:{groups[4]}:{groups[5]}"
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def generate_files(df, pdf_metadata, target_year):
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    release_date_raw = pdf_metadata.get('creationDate') or pdf_metadata.get('modDate') or ""
    release_date = parse_pdf_date(release_date_raw)
    
    # Create output directory
    run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(config.OUTPUT_DIR, run_timestamp)
    os.makedirs(output_path, exist_ok=True)
    
    data_filename = f"{config.DATASET_NAME}_DATA_{timestamp}.xls"
    meta_filename = f"{config.DATASET_NAME}_META_{timestamp}.xls"
    zip_filename = f"{config.DATASET_NAME}_{timestamp}.zip"
    
    data_path = os.path.join(output_path, data_filename)
    meta_path = os.path.join(output_path, meta_filename)
    zip_path = os.path.join(output_path, zip_filename)
    
    # 1. Generate DATA file
    wb_data = xlwt.Workbook(encoding='utf-8')
    ws_data = wb_data.add_sheet('Sheet1')
    
    # Row 0: Absolute Codes (Exactly as in reference)
    ws_data.write(0, 0, "") # Year column header is blank
    for col_idx, (code, desc) in enumerate(config.ABSOLUTE_COLUMNS):
        ws_data.write(0, col_idx + 1, code)
        
    # Row 1: Absolute Descriptions (Subheaders)
    ws_data.write(1, 0, "")
    for col_idx, (code, desc) in enumerate(config.ABSOLUTE_COLUMNS):
        ws_data.write(1, col_idx + 1, desc)
        
    # Rows 2+: Data
    # df.index is Year
    for row_idx, (year, row) in enumerate(df.iterrows()):
        ws_data.write(row_idx + 2, 0, year)
        for col_idx, (code, desc) in enumerate(config.ABSOLUTE_COLUMNS):
            val = row.get(code, "")
            if pd.isna(val) or val == "":
                # Reference uses blank for missing values
                ws_data.write(row_idx + 2, col_idx + 1, "")
            else:
                try:
                    # Clean numerical values
                    clean_val = str(val).replace(",", "").strip()
                    ws_data.write(row_idx + 2, col_idx + 1, float(clean_val))
                except:
                    ws_data.write(row_idx + 2, col_idx + 1, str(val))
                    
    wb_data.save(data_path)
    
    # 2. Generate META file
    wb_meta = xlwt.Workbook(encoding='utf-8')
    ws_meta = wb_meta.add_sheet('Sheet1')
    
    meta_headers = [
        "CODE", "DESCRIPTION", "SOURCE", "FREQUENCY", "UNIT", "URL", 
        "LAST_RELEASE_DATE", "NEXT_RELEASE_DATE"
    ]
    
    for col_idx, h in enumerate(meta_headers):
        ws_meta.write(0, col_idx, h)
        
    # One row per time series in absolute order
    for row_idx, (code, desc) in enumerate(config.ABSOLUTE_COLUMNS):
        ws_meta.write(row_idx + 1, 0, code)
        ws_meta.write(row_idx + 1, 1, desc)
        ws_meta.write(row_idx + 1, 2, config.METADATA_ATTRIBUTES["SOURCE"])
        ws_meta.write(row_idx + 1, 3, config.METADATA_ATTRIBUTES["FREQUENCY"])
        ws_meta.write(row_idx + 1, 4, config.METADATA_ATTRIBUTES["UNIT"])
        ws_meta.write(row_idx + 1, 5, config.METADATA_ATTRIBUTES["URL"])
        ws_meta.write(row_idx + 1, 6, release_date)
        try:
            next_year = int(timestamp[:4]) + 1
            ws_meta.write(row_idx + 1, 7, f"{next_year}-02-15T15:00:00")
        except:
            ws_meta.write(row_idx + 1, 7, "")
            
    wb_meta.save(meta_path)
    
    # 3. Create ZIP
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(data_path, data_filename)
        z.write(meta_path, meta_filename)
        
    # 4. Copy to Latest
    os.makedirs(config.LATEST_DIR, exist_ok=True)
    shutil.copy(data_path, os.path.join(config.LATEST_DIR, data_filename))
    shutil.copy(meta_path, os.path.join(config.LATEST_DIR, meta_filename))
    shutil.copy(zip_path, os.path.join(config.LATEST_DIR, zip_filename))
    
    print(f"Structural identity enforced. Files generated in {output_path}")
    return zip_path

if __name__ == "__main__":
    # Test with absolute columns
    dummy_df = pd.DataFrame(index=["2023", "2024"])
    dummy_df.index.name = "Year"
    metadata = {}
    generate_files(dummy_df, metadata, "2026")
