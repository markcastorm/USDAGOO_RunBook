import pandas as pd
import os
import xlrd
import config

def verify_structural_identity():
    # 1. Load reference Excel '2026' tab
    ref_xls_path = r'D:\Projects\SIMBA-RUNBOOKS\USDAGOO_RunBook\Project_Information\USDAGOO_DATA_20240306[1].xlsx'
    print(f"Checking identity against reference: {ref_xls_path}, tab '2026'...")
    
    ref_df = pd.read_excel(ref_xls_path, sheet_name='2026', header=None)
    ref_codes = [str(c).strip() for c in ref_df.iloc[0]]
    ref_descs = [str(d).strip() for d in ref_df.iloc[1]]
    
    # 2. Load generated output
    latest_dir = config.LATEST_DIR
    data_files = [f for f in os.listdir(latest_dir) if f.startswith("USDAGOO_DATA_") and f.endswith(".xls")]
    if not data_files:
        print("No generated file found.")
        return
        
    gen_xls_path = os.path.join(latest_dir, data_files[0])
    print(f"Generated file: {gen_xls_path}")
    gen_df = pd.read_excel(gen_xls_path, header=None, engine='xlrd')
    gen_codes = [str(c).strip() for c in gen_df.iloc[0]]
    gen_descs = [str(d).strip() for d in gen_df.iloc[1]]
    
    # 3. Compare Headers
    print("\n--- Header Identity Audit ---")
    header_errors = 0
    
    # Check column count
    if len(gen_codes) != len(ref_codes):
        print(f"FAIL: Column count mismatch! Gen={len(gen_codes)}, Ref={ref_codes}")
        header_errors += 1
    else:
        print(f"PASS: Column count matched ({len(gen_codes)})")

    # Check every column identity
    for i in range(len(ref_codes)):
        gc = gen_codes[i] if i < len(gen_codes) else "MISSING"
        rc = ref_codes[i]
        gd = gen_descs[i] if i < len(gen_descs) else "MISSING"
        rd = ref_descs[i]
        
        if gc != rc or gd != rd:
            print(f"MISMATCH Col {i}:")
            print(f"  Ref: {rc} | {rd}")
            print(f"  Gen: {gc} | {gd}")
            header_errors += 1
            
    if header_errors == 0:
        print("SUCCESS: 100% Structural Header Identity achieved!")
    else:
        print(f"FAILURE: Found {header_errors} header identity errors.")

    # 4. Compare Data for 2026
    print("\n--- Data Value Audit (Year 2026) ---")
    # Identify 2026 row in Gen
    gen_data = gen_df.iloc[2:].copy()
    gen_data.columns = gen_codes
    gen_data.set_index(gen_codes[0], inplace=True)
    
    ref_data = ref_df.iloc[2:].copy()
    ref_data.columns = ref_codes
    ref_data.set_index(ref_codes[0], inplace=True)
    
    # Match years
    target_year = 2026.0
    if target_year in gen_data.index and target_year in ref_data.index:
        gen_row = gen_data.loc[target_year]
        ref_row = ref_data.loc[target_year]
        
        data_mismatches = 0
        for code in ref_codes[1:]:
            gv = str(gen_row[code]).strip() if code in gen_row else "MISSING"
            rv = str(ref_row[code]).replace(',', '').strip()
            
            # Clean "nan"
            if gv == "nan" or gv == "None": gv = ""
            if rv == "nan" or rv == "None": rv = ""
            
            if gv != rv:
                # Special case: float comparison
                try:
                    if abs(float(gv) - float(rv)) < 1e-5: continue
                except: pass
                
                print(f"DATA MISMATCH [{code}]: Gen='{gv}', Ref='{rv}'")
                data_mismatches += 1
        
        if data_mismatches == 0:
            print("SUCCESS: All 2026 data points match exactly!")
        else:
            print(f"FAILURE: Found {data_mismatches} data mismatches for 2026.")
    else:
        print("Year 2026 not found in one of the files.")

if __name__ == "__main__":
    verify_structural_identity()
