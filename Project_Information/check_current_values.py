import pandas as pd
import xlrd
import os
import config

latest_dir = config.LATEST_DIR
data_files = [f for f in os.listdir(latest_dir) if f.startswith("USDAGOO_DATA_") and f.endswith(".xls")]
if not data_files:
    print("No generated data file found.")
    exit()

gen_xls_path = os.path.join(latest_dir, data_files[0])
df = pd.read_excel(gen_xls_path, header=None, engine='xlrd')

codes = df.iloc[0].tolist()
years = df.iloc[2:, 0].tolist()

# Find indices
seed_idx = codes.index("USDAGOO.SOYBEANSDP.SEED.A")
residual_idx = codes.index("USDAGOO.SOYBEANSDP.RESIDUAL.A")
biodiesel_idx = codes.index("USDAGOO.SOYBEANOILSDP.BIODIESEL.A")

print(f"Checking file: {gen_xls_path}")
for i, year in enumerate(years):
    row_idx = i + 2
    seed_val = df.iloc[row_idx, seed_idx]
    residual_val = df.iloc[row_idx, residual_idx]
    biodiesel_val = df.iloc[row_idx, biodiesel_idx]
    print(f"Year {year}: Seed={seed_val}, Residual={residual_val}, Biodiesel={biodiesel_val}")
