
import re

def clean_label(label):
    if not label: return ""
    label = re.sub(r'\s*/?\d+/?\s*$', '', str(label))
    label = label.strip().strip('.')
    label = re.sub(r'\s+', ' ', label)
    return label

def test_match(cfg_label, extracted_label):
    clean_cfg = clean_label(cfg_label).lower()
    ext_clean = clean_label(extracted_label).lower()
    
    match = False
    if clean_cfg == ext_clean: match = True
    elif clean_cfg == "biodiesel" and "biodiesel" in ext_clean: match = True
    elif clean_cfg == "biofuel" and "biofuel" in ext_clean: match = True
    elif len(clean_cfg) > 10 and (clean_cfg in ext_clean or ext_clean in clean_cfg): match = True
    
    print(f"CFG: '{cfg_label}' ({len(clean_cfg)}) | EXT: '{extracted_label}' | MATCH: {match}")

test_match("Seed", "Seed and Residual")
test_match("Residual", "Seed and Residual")
test_match("Seed and Residual", "Seed and Residual")
test_match("Biodiesel", " Biodiesel 3/")
