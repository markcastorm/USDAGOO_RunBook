
import pandas as pd
import os
import xlrd
import config

def detailed_validation():
    # 1. Load reference CSV
    ref_csv_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\USDAGOO_DATA_20240306 - 2026.csv'
    ref_df = pd.read_csv(ref_csv_path, header=None)
    ref_codes = ref_df.iloc[0].tolist()
    ref_subs = ref_df.iloc[1].tolist()
    ref_data = ref_df.iloc[2:].copy()
    ref_data.columns = ref_codes
    ref_data.set_index(ref_data.columns[0], inplace=True)
    
    # 2. Load generated XLS
    gen_xls_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\output\20260618_112152\USDAGOO_DATA_20260618.xls'
    if not os.path.exists(gen_xls_path):
        print(f"File not found: {gen_xls_path}")
        return
        
    gen_df = pd.read_excel(gen_xls_path, header=None, engine='xlrd')
    gen_codes = gen_df.iloc[0].tolist()
    gen_subs = gen_df.iloc[1].tolist()
    gen_data = gen_df.iloc[2:].copy()
    gen_data.columns = gen_codes
    gen_data.set_index(gen_data.columns[0], inplace=True)
    
    print(f"Validating {gen_xls_path} against {ref_csv_path}")
    
    # Check Headers
    print("\n--- Header Validation ---")
    if len(gen_codes) != len(ref_codes):
        print(f"Header length mismatch: Gen={len(gen_codes)}, Ref={len(ref_codes)}")
    else:
        for i, (g, r) in enumerate(zip(gen_codes, ref_codes)):
            if str(g) != str(r):
                print(f"Header mismatch at col {i}: Gen='{g}', Ref='{r}'")
                
    # Check Subheaders
    print("\n--- Subheader Validation ---")
    if len(gen_subs) != len(ref_subs):
        print(f"Subheader length mismatch: Gen={len(gen_subs)}, Ref={len(ref_subs)}")
    else:
        for i, (g, r) in enumerate(zip(gen_subs, ref_subs)):
            if str(g) != str(r):
                print(f"Subheader mismatch at col {i}: Gen='{g}', Ref='{r}'")
                
    # Check Data
    print("\n--- Data Validation ---")
    mismatches = []
    for year in gen_data.index:
        year_str = str(year)
        # Handle decimal year in Excel if necessary
        if year_str.endswith(".0"): year_str = year_str[:-2]
        
        ref_year_matches = [i for i, x in enumerate(ref_data.index) if str(x) == year_str]
        if not ref_year_matches:
            print(f"Year {year_str} not found in reference.")
            continue
            
        ref_row = ref_data.iloc[ref_year_matches[0]]
        gen_row = gen_data.loc[year]
        
        for code in gen_codes[1:]: # Skip year col
            if code in ref_codes:
                gen_val = str(gen_row[code]).strip()
                ref_val = str(ref_row[code]).replace(',', '').strip()
                
                # Normalize values
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
                    mismatches.append(f"Year {year_str}, Code {code}: Gen='{gen_val}', Ref='{ref_val}'")
                    
    if not mismatches:
        print("SUCCESS: All data points match exactly (including blanks)!")
    else:
        print(f"FAILURE: Found {len(mismatches)} mismatches:")
        for m in mismatches[:20]: # Show first 20
            print(f"  {m}")
        if len(mismatches) > 20:
            print(f"  ... and {len(mismatches) - 20} more.")

if __name__ == "__main__":
    detailed_validation()
