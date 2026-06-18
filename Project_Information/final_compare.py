
import pandas as pd
import os
import xlrd
import config

def compare_results():
    # 1. Load reference CSV
    ref_csv_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\USDAGOO_DATA_20240306 - 2026.csv'
    ref_df = pd.read_csv(ref_csv_path, header=None)
    ref_codes = [str(c).strip() for c in ref_df.iloc[0].tolist()]
    ref_data = ref_df.iloc[2:].copy()
    ref_data.columns = ref_codes
    ref_data.iloc[:, 0] = ref_data.iloc[:, 0].astype(str).str.strip()
    ref_data.set_index(ref_data.columns[0], inplace=True)
    
    # 2. Load generated XLS (Specifically the 20260618 one)
    gen_xls_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\output\latest\USDAGOO_DATA_20260618.xls'
    if not os.path.exists(gen_xls_path):
        print(f"File not found: {gen_xls_path}")
        return
        
    gen_df = pd.read_excel(gen_xls_path, header=None, engine='xlrd')
    gen_codes = [str(c).strip() for c in gen_df.iloc[0].tolist()]
    gen_data = gen_df.iloc[2:].copy()
    gen_data.columns = gen_codes
    def clean_year(y):
        s = str(y).strip()
        if s.endswith(".0"): return s[:-2]
        return s
    gen_data.iloc[:, 0] = gen_data.iloc[:, 0].apply(clean_year)
    gen_data.set_index(gen_data.columns[0], inplace=True)
    
    # 3. Compare
    print(f"Comparing {gen_xls_path} with {ref_csv_path}...")
    
    mismatches = 0
    total_checks = 0
    
    for year in gen_data.index:
        if year not in ref_data.index:
            continue
            
        ref_row = ref_data.loc[year]
        gen_row = gen_data.loc[year]
        
        for code in gen_codes[1:]:
            if code in ref_codes:
                gen_val = str(gen_row[code]).strip()
                ref_val = str(ref_row[code]).replace(',', '').strip()
                
                # Normalize NA
                if gen_val.lower() in ["nan", "none", "na", ""]: gen_val = "BLANK"
                if ref_val.lower() in ["nan", "none", "na", ""]: ref_val = "BLANK"
                
                match = False
                if gen_val == ref_val:
                    match = True
                else:
                    try:
                        gv = float(gen_val)
                        rv = float(ref_val)
                        if abs(gv - rv) < 1e-5: match = True
                    except:
                        pass
                
                if not match:
                    print(f"MISMATCH for {year} {code}: Gen='{gen_val}', Ref='{ref_val}'")
                    mismatches += 1
                total_checks += 1
                
    if mismatches == 0:
        print(f"SUCCESS: All {total_checks} checked fields match exactly (including blanks)!")
    else:
        print(f"FAILURE: Found {mismatches} mismatches out of {total_checks} checks.")

if __name__ == "__main__":
    compare_results()
