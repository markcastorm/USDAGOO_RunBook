
import config
import re

def clean_label(label):
    if not label: return ""
    # Remove footnotes like 1/, /1, 1 /
    label = re.sub(r'\s*/?\d+/?\s*$', '', str(label))
    label = label.strip().strip('.')
    label = re.sub(r'\s+', ' ', label)
    return label

def test_mapping():
    table_data = {
        "Seed and Residual": {"2023": "119"},
        "Biodiesel": {"2023": "12995"},
        "Food, Feed, Other Industrial": {"2023": "14158"}
    }
    
    soybean_mapping = config.TABLE_CONFIGS["SOYBEAN"]["mapping"]
    soybean_oil_mapping = config.TABLE_CONFIGS["SOYBEAN_OIL"]["mapping"]
    
    print("Testing Soybean Mapping:")
    for cfg_label, cfg_code in soybean_mapping.items():
        clean_cfg = clean_label(cfg_label).lower()
        matched = False
        for extracted_label, year_vals in table_data.items():
            ext_clean = extracted_label.lower()
            match = False
            if clean_cfg == ext_clean: match = True
            elif clean_cfg == "biodiesel" and "biodiesel" in ext_clean: match = True
            elif clean_cfg == "biofuel" and "biofuel" in ext_clean: match = True
            elif len(clean_cfg) > 10 and (clean_cfg in ext_clean or ext_clean in clean_cfg): match = True
            
            if match:
                print(f"  CFG: '{cfg_label}' -> EXT: '{extracted_label}' (MATCH)")
                matched = True
        if not matched:
            print(f"  CFG: '{cfg_label}' -> NO MATCH")

    print("\nTesting Soybean Oil Mapping:")
    for cfg_label, cfg_code in soybean_oil_mapping.items():
        clean_cfg = clean_label(cfg_label).lower()
        matched = False
        for extracted_label, year_vals in table_data.items():
            ext_clean = extracted_label.lower()
            match = False
            if clean_cfg == ext_clean: match = True
            elif clean_cfg == "biodiesel" and "biodiesel" in ext_clean: match = True
            elif clean_cfg == "biofuel" and "biofuel" in ext_clean: match = True
            elif len(clean_cfg) > 10 and (clean_cfg in ext_clean or ext_clean in clean_cfg): match = True
            
            if match:
                print(f"  CFG: '{cfg_label}' -> EXT: '{extracted_label}' (MATCH)")
                matched = True
        if not matched:
            print(f"  CFG: '{cfg_label}' -> NO MATCH")

if __name__ == "__main__":
    test_mapping()
