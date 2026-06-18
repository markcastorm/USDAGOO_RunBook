import pandas as pd
import os
import xlrd
import config

def compare_results():
    # 1. Load reference CSV
    ref_csv_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\USDAGOO_DATA_20240306 - 2026.csv'
    ref_df = pd.read_csv(ref_csv_path, header=None)
    ref_codes = ref_df.iloc[0].tolist()
    ref_data = ref_df.iloc[2:].copy()
    ref_data.columns = ref_codes
    ref_data.set_index(ref_data.columns[0], inplace=True)
    
    # 2. Load generated XLS
    latest_dir = config.LATEST_DIR
    data_files = [f for f in os.listdir(latest_dir) if f.startswith("USDAGOO_DATA_") and f.endswith(".xls")]
    if not data_files:
        print("No generated data file found.")
        return
        
    gen_xls_path = os.path.join(latest_dir, data_files[0])
    
    # Read XLS (using xlrd since it's .xls)
    # We'll use pandas read_excel with xlrd engine
    gen_df = pd.read_excel(gen_xls_path, header=None, engine='xlrd')
    gen_codes = gen_df.iloc[0].tolist()
    gen_data = gen_df.iloc[2:].copy()
    gen_data.columns = gen_codes
    gen_data.set_index(gen_data.columns[0], inplace=True)
    
    # 3. Compare
    print(f"Comparing {gen_xls_path} with {ref_csv_path}...")
    
    mismatches = 0
    total_checks = 0
    
    for year in gen_data.index:
        year_str = str(year)
        if year_str not in [str(x) for x in ref_data.index]:
            print(f"Year {year_str} not found in reference.")
            continue
            
        ref_year_idx = [i for i, x in enumerate(ref_data.index) if str(x) == year_str][0]
        ref_row = ref_data.iloc[ref_year_idx]
        gen_row = gen_data.loc[year]
        
        for code in gen_codes[1:]: # Skip year col
            if code in ref_codes:
                gen_val = str(gen_row[code]).strip()
                ref_val = str(ref_row[code]).replace(',', '').strip()
                
                # Handle NA
                if gen_val == "NA" and (ref_val == "" or ref_val == "nan"):
                    continue
                
                # Convert to float for comparison if possible
                try:
                    gv = float(gen_val)
                    rv = float(ref_val)
                    if abs(gv - rv) > 1e-5:
                        print(f"MISMATCH for {year} {code}: Gen={gv}, Ref={rv}")
                        mismatches += 1
                except:
                    if gen_val != ref_val:
                        print(f"MISMATCH for {year} {code}: Gen={gen_val}, Ref={ref_val}")
                        mismatches += 1
                total_checks += 1
                
    if mismatches == 0:
        print(f"SUCCESS: All {total_checks} checked fields match exactly!")
    else:
        print(f"FAILURE: Found {mismatches} mismatches out of {total_checks} checks.")

if __name__ == "__main__":
    compare_results()
