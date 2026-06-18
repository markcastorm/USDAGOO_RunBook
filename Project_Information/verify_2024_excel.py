import pandas as pd
import os
import xlrd
import config

def verify_2023():
    # 1. Load reference Excel '2023' tab
    ref_xls_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\USDAGOO_DATA_20240306[1].xlsx'
    print(f"Loading reference from {ref_xls_path}, tab '2023'...")
    
    ref_df = pd.read_excel(ref_xls_path, sheet_name='2023', header=None)
    ref_codes = [str(c).strip() for c in ref_df.iloc[0]]
    ref_data = ref_df.iloc[2:].copy()
    ref_data.columns = ref_codes
    year_col = ref_codes[0]
    ref_data.set_index(year_col, inplace=True)
    
    # 2. Load generated output
    latest_dir = config.LATEST_DIR
    data_files = [f for f in os.listdir(latest_dir) if f.startswith("USDAGOO_DATA_") and f.endswith(".xls")]
    if not data_files:
        print("No generated data file found.")
        return
        
    gen_xls_path = os.path.join(latest_dir, data_files[0])
    print(f"Loading generated data from {gen_xls_path}...")
    
    gen_df = pd.read_excel(gen_xls_path, header=None, engine='xlrd')
    gen_codes = [str(c).strip() for c in gen_df.iloc[0]]
    gen_data = gen_df.iloc[2:].copy()
    gen_data.columns = gen_codes
    gen_data.set_index(gen_codes[0], inplace=True)
    
    # 3. Compare 2023
    target_year = 2023.0
    if target_year not in gen_data.index:
        target_year = 2023
        if target_year not in gen_data.index:
            target_year = "2023"
            
    if target_year not in gen_data.index:
        print(f"Year 2023 not found in generated data. Available: {list(gen_data.index)}")
        return

    print(f"\n--- Verifying Year 2023 ---")
    mismatches = 0
    total_checks = 0
    
    gen_row = gen_data.loc[target_year]
    ref_year = 2023.0
    if ref_year not in ref_data.index: ref_year = 2023
        
    if ref_year not in ref_data.index:
        print(f"Year 2023 not found in reference tab '2023'.")
        return
        
    ref_row = ref_data.loc[ref_year]
    
    for code in gen_codes[1:]:
        if code in ref_codes:
            gen_val = str(gen_row[code]).strip()
            ref_val = str(ref_row[code]).replace(',', '').strip()
            
            if (gen_val == "NA" or gen_val == "nan" or gen_val == "") and (ref_val == "nan" or ref_val == "" or ref_val == "None"):
                continue
            
            try:
                gv = float(gen_val)
                rv = float(ref_val)
                if abs(gv - rv) > 1e-5:
                    print(f"MISMATCH [{code}]: Gen={gv}, Ref={rv}")
                    mismatches += 1
            except:
                if gen_val != ref_val:
                    print(f"MISMATCH [{code}]: Gen='{gen_val}', Ref='{ref_val}'")
                    mismatches += 1
            total_checks += 1
            
    if mismatches == 0:
        print(f"\nSUCCESS: All {total_checks} fields for 2023 match exactly with the Excel tab!")
    else:
        print(f"\nFAILURE: Found {mismatches} mismatches for 2023.")

if __name__ == "__main__":
    verify_2023()
