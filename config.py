import os

# Dataset Information
DATASET_NAME = "USDAGOO"
BASE_URL = "https://www.usda.gov/oce/ag-outlook-forum/commodity-outlooks"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_INFO_DIR = os.path.join(BASE_DIR, "Project_Information")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LATEST_DIR = os.path.join(OUTPUT_DIR, "latest")

# Selenium Settings
HEADLESS = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Extraction Settings
TARGET_REPORT_NAME = "Grains and Oilseeds Outlook"
TARGET_YEAR = 2022 # Default to latest

# Absolute Column Structure (Ordered as per reference CSV/XLSX)
# Each entry is (CODE, DESCRIPTION)
ABSOLUTE_COLUMNS = [
    ("USDAGOO.CORNSDP.AREAPLANTED.A", "Corn Supply, Demand, and Price, Area planted (mil. ac.)"),
    ("USDAGOO.CORNSDP.AREAHARVESTED.A", "Corn Supply, Demand, and Price, Area harvested"),
    ("USDAGOO.CORNSDP.YIELD.A", "Corn Supply, Demand, and Price, Yield (bu./ac.)"),
    ("USDAGOO.CORNSDP.PRODUCTION.A", "Corn Supply, Demand, and Price, Production (mil. bu.)"),
    ("USDAGOO.CORNSDP.BEGINNINGSTOCKS.A", "Corn Supply, Demand, and Price, Beginning stocks"),
    ("USDAGOO.CORNSDP.IMPORTS.A", "Corn Supply, Demand, and Price, Imports"),
    ("USDAGOO.CORNSDP.SUPPLY.A", "Corn Supply, Demand, and Price, Supply"),
    ("USDAGOO.CORNSDP.FEEDRESIDUAL.A", "Corn Supply, Demand, and Price, Feed & residual"),
    ("USDAGOO.CORNSDP.ETHANOL.A", "Corn Supply, Demand, and Price, Ethanol"),
    ("USDAGOO.CORNSDP.FOODSEEDOTHERINDUSTRIAL.A", "Corn Supply, Demand, and Price, Food, seed & other industrial"),
    ("USDAGOO.CORNSDP.TOTALFOODSEEDINDUSTRIAL.A", "Corn Supply, Demand, and Price, Total food, seed & industrial"),
    ("USDAGOO.CORNSDP.TOTALDOMESTICUSE.A", "Corn Supply, Demand, and Price, Total domestic use"),
    ("USDAGOO.CORNSDP.EXPORTS.A", "Corn Supply, Demand, and Price, Exports"),
    ("USDAGOO.CORNSDP.TOTALUSE.A", "Corn Supply, Demand, and Price, Total use"),
    ("USDAGOO.CORNSDP.ENDINGSTOCKS.A", "Corn Supply, Demand, and Price, Ending stocks"),
    ("USDAGOO.CORNSDP.STOCKSUSE.A", "Corn Supply, Demand, and Price, Stocks/use (percent)"),
    ("USDAGOO.CORNSDP.SEASONAVGFARMPRICE.A", "Corn Supply, Demand, and Price, Season-avg. farm price ($/bu.)"),
    ("USDAGOO.CORNSDP.FARMPRICE.A", "Corn Supply, Demand, and Price, Farm Price ($/bushel)"),
    ("USDAGOO.SOYBEANSDP.AREAPLANTED.A", "Soybean Supply, Demand, and Price, Area planted (mil. ac.)"),
    ("USDAGOO.SOYBEANSDP.AREAHARVESTED.A", "Soybean Supply, Demand, and Price, Area harvested"),
    ("USDAGOO.SOYBEANSDP.YIELD.A", "Soybean Supply, Demand, and Price, Yield (bu./ac.)"),
    ("USDAGOO.SOYBEANSDP.PRODUCTION.A", "Soybean Supply, Demand, and Price, Production (mil. bu.)"),
    ("USDAGOO.SOYBEANSDP.BEGINNINGSTOCKS.A", "Soybean Supply, Demand, and Price, Beginning stocks"),
    ("USDAGOO.SOYBEANSDP.IMPORTS.A", "Soybean Supply, Demand, and Price, Imports"),
    ("USDAGOO.SOYBEANSDP.SUPPLY.A", "Soybean Supply, Demand, and Price, Supply"),
    ("USDAGOO.SOYBEANSDP.CRUSH.A", "Soybean Supply, Demand, and Price, Crush"),
    ("USDAGOO.SOYBEANSDP.SEEDANDRESIDUAL.A", "Soybean Supply, Demand, and Price, Seed and Residual"),
    ("USDAGOO.SOYBEANSDP.SEED.A", "Soybean Supply, Demand, and Price, Seed"),
    ("USDAGOO.SOYBEANSDP.RESIDUAL.A", "Soybean Supply, Demand, and Price, Residual"),
    ("USDAGOO.SOYBEANSDP.TOTALDOMESTICUSE.A", "Soybean Supply, Demand, and Price, Total domestic use"),
    ("USDAGOO.SOYBEANSDP.EXPORTS.A", "Soybean Supply, Demand, and Price, Exports"),
    ("USDAGOO.SOYBEANSDP.TOTALUSE.A", "Soybean Supply, Demand, and Price, Total use"),
    ("USDAGOO.SOYBEANSDP.ENDINGSTOCKS.A", "Soybean Supply, Demand, and Price, Ending stocks"),
    ("USDAGOO.SOYBEANSDP.STOCKSUSE.A", "Soybean Supply, Demand, and Price, Stocks/use (percent)"),
    ("USDAGOO.SOYBEANSDP.SEASONAVGFARMPRICE.A", "Soybean Supply, Demand, and Price, Season-avg. farm price ($/bu.)"),
    ("USDAGOO.SOYBEANSDP.FARMPRICE.A", "Soybean Supply, Demand, and Price, Farm Price ($/bushel)"),
    ("USDAGOO.SOYBEANMEALSDP.PRODUCTION.A", "Soybean Meal Supply, Demand, and Price, Production (thou. short tons)"),
    ("USDAGOO.SOYBEANMEALSDP.BEGINNINGSTOCKS.A", "Soybean Meal Supply, Demand, and Price, Beginning stocks"),
    ("USDAGOO.SOYBEANMEALSDP.IMPORTS.A", "Soybean Meal Supply, Demand, and Price, Imports"),
    ("USDAGOO.SOYBEANMEALSDP.SUPPLY.A", "Soybean Meal Supply, Demand, and Price, Supply"),
    ("USDAGOO.SOYBEANMEALSDP.DOMESTICUSE.A", "Soybean Meal Supply, Demand, and Price, Domestic Use"),
    ("USDAGOO.SOYBEANMEALSDP.EXPORTS.A", "Soybean Meal Supply, Demand, and Price, Exports"),
    ("USDAGOO.SOYBEANMEALSDP.TOTALUSE.A", "Soybean Meal Supply, Demand, and Price, Total use"),
    ("USDAGOO.SOYBEANMEALSDP.ENDINGSTOCKS.A", "Soybean Meal Supply, Demand, and Price, Ending stocks"),
    ("USDAGOO.SOYBEANMEALSDP.AVGPRICE.A", "Soybean Meal Supply, Demand, and Price, Avg. price ($/short ton)"),
    ("USDAGOO.SOYBEANOILSDP.PRODUCTION.A", "Soybean Oil Supply, Demand, and Price, Production (mil. lbs.)"),
    ("USDAGOO.SOYBEANOILSDP.BEGINNINGSTOCKS.A", "Soybean Oil Supply, Demand, and Price, Beginning stocks"),
    ("USDAGOO.SOYBEANOILSDP.IMPORTS.A", "Soybean Oil Supply, Demand, and Price, Imports"),
    ("USDAGOO.SOYBEANOILSDP.SUPPLY.A", "Soybean Oil Supply, Demand, and Price, Supply"),
    ("USDAGOO.SOYBEANOILSDP.DOMESTICUSE.A", "Soybean Oil Supply, Demand, and Price, Domestic Use"),
    ("USDAGOO.SOYBEANOILSDP.METHYLESTER.A", "Soybean Oil Supply, Demand, and Price, Methyl Ester"),
    ("USDAGOO.SOYBEANOILSDP.BIODIESEL.A", "Soybean Oil Supply, Demand, and Price, Biodiesel"),
    ("USDAGOO.SOYBEANOILSDP.FOODFEEDOTHERINDUSTRIAL.A", "Soybean Oil Supply, Demand, and Price, Food, Feed, Other Industrial"),
    ("USDAGOO.SOYBEANOILSDP.EXPORTS.A", "Soybean Oil Supply, Demand, and Price, Exports"),
    ("USDAGOO.SOYBEANOILSDP.TOTALUSE.A", "Soybean Oil Supply, Demand, and Price, Total use"),
    ("USDAGOO.SOYBEANOILSDP.ENDINGSTOCKS.A", "Soybean Oil Supply, Demand, and Price, Ending stocks"),
    ("USDAGOO.SOYBEANOILSDP.AVGPRICE.A", "Soybean Oil Supply, Demand, and Price, Avg. price (cents/lb.)"),
    ("USDAGOO.WHEATSDP.AREAPLANTED.A", "Wheat Supply, Demand, and Price, Area planted (mil. ac.)"),
    ("USDAGOO.WHEATSDP.AREAHARVESTED.A", "Wheat Supply, Demand, and Price, Area harvested"),
    ("USDAGOO.WHEATSDP.YIELD.A", "Wheat Supply, Demand, and Price, Yield (bu./ac.)"),
    ("USDAGOO.WHEATSDP.PRODUCTION.A", "Wheat Supply, Demand, and Price, Production (mil. bu.)"),
    ("USDAGOO.WHEATSDP.BEGINNINGSTOCKS.A", "Wheat Supply, Demand, and Price, Beginning stocks"),
    ("USDAGOO.WHEATSDP.IMPORTS.A", "Wheat Supply, Demand, and Price, Imports"),
    ("USDAGOO.WHEATSDP.SUPPLY.A", "Wheat Supply, Demand, and Price, Supply"),
    ("USDAGOO.WHEATSDP.FEEDRESIDUAL.A", "Wheat Supply, Demand, and Price, Feed & residual"),
    ("USDAGOO.WHEATSDP.FOODSEED.A", "Wheat Supply, Demand, and Price, Food & seed"),
    ("USDAGOO.WHEATSDP.FOODSEEDINDUSTRIAL.A", "Wheat Supply, Demand, and Price, Food, seed & industrial"),
    ("USDAGOO.WHEATSDP.TOTALDOMESTICUSE.A", "Wheat Supply, Demand, and Price, Total domestic use"),
    ("USDAGOO.WHEATSDP.EXPORTS.A", "Wheat Supply, Demand, and Price, Exports"),
    ("USDAGOO.WHEATSDP.TOTALUSE.A", "Wheat Supply, Demand, and Price, Total use"),
    ("USDAGOO.WHEATSDP.ENDINGSTOCKS.A", "Wheat Supply, Demand, and Price, Ending stocks"),
    ("USDAGOO.WHEATSDP.STOCKSUSE.A", "Wheat Supply, Demand, and Price, Stocks/use (percent)"),
    ("USDAGOO.WHEATSDP.SEASONAVGFARMPRICE.A", "Wheat Supply, Demand, and Price, Season-avg. farm price ($/bu.)"),
    ("USDAGOO.WHEATSDP.FARMPRICE.A", "Wheat Supply, Demand, and Price, Farm Price ($/bushel)")
]

# Mapping Config (Used to identify extracted labels from PDF)
TABLE_CONFIGS = {
    "CORN": {
        "keywords": ["Corn Supply, Demand, and Price"],
        "mapping": {
            "Area planted (mil. ac.)": "USDAGOO.CORNSDP.AREAPLANTED.A",
            "Area harvested": "USDAGOO.CORNSDP.AREAHARVESTED.A",
            "Yield (bu./ac.)": "USDAGOO.CORNSDP.YIELD.A",
            "Production (mil. bu.)": "USDAGOO.CORNSDP.PRODUCTION.A",
            "Beginning stocks": "USDAGOO.CORNSDP.BEGINNINGSTOCKS.A",
            "Imports": "USDAGOO.CORNSDP.IMPORTS.A",
            "Supply": "USDAGOO.CORNSDP.SUPPLY.A",
            "Feed & residual": "USDAGOO.CORNSDP.FEEDRESIDUAL.A",
            "Ethanol": "USDAGOO.CORNSDP.ETHANOL.A",
            "Food, seed & other industrial": "USDAGOO.CORNSDP.FOODSEEDOTHERINDUSTRIAL.A",
            "Total food, seed & industrial": "USDAGOO.CORNSDP.TOTALFOODSEEDINDUSTRIAL.A",
            "Total domestic use": "USDAGOO.CORNSDP.TOTALDOMESTICUSE.A",
            "Exports": "USDAGOO.CORNSDP.EXPORTS.A",
            "Total use": "USDAGOO.CORNSDP.TOTALUSE.A",
            "Ending stocks": "USDAGOO.CORNSDP.ENDINGSTOCKS.A",
            "Stocks/use (percent)": "USDAGOO.CORNSDP.STOCKSUSE.A",
            "Season-avg. farm price ($/bu.)": "USDAGOO.CORNSDP.SEASONAVGFARMPRICE.A",
            "Farm Price ($/bushel)": "USDAGOO.CORNSDP.FARMPRICE.A"
        }
    },
    "SOYBEAN": {
        "keywords": ["Soybean Supply, Demand, and Price"],
        "mapping": {
            "Area planted (mil. ac.)": "USDAGOO.SOYBEANSDP.AREAPLANTED.A",
            "Area harvested": "USDAGOO.SOYBEANSDP.AREAHARVESTED.A",
            "Yield (bu./ac.)": "USDAGOO.SOYBEANSDP.YIELD.A",
            "Production (mil. bu.)": "USDAGOO.SOYBEANSDP.PRODUCTION.A",
            "Beginning stocks": "USDAGOO.SOYBEANSDP.BEGINNINGSTOCKS.A",
            "Imports": "USDAGOO.SOYBEANSDP.IMPORTS.A",
            "Supply": "USDAGOO.SOYBEANSDP.SUPPLY.A",
            "Crush": "USDAGOO.SOYBEANSDP.CRUSH.A",
            "Seed and Residual": "USDAGOO.SOYBEANSDP.SEEDANDRESIDUAL.A",
            "Seed": "USDAGOO.SOYBEANSDP.SEED.A",
            "Residual": "USDAGOO.SOYBEANSDP.RESIDUAL.A",
            "Total domestic use": "USDAGOO.SOYBEANSDP.TOTALDOMESTICUSE.A",
            "Exports": "USDAGOO.SOYBEANSDP.EXPORTS.A",
            "Total use": "USDAGOO.SOYBEANSDP.TOTALUSE.A",
            "Ending stocks": "USDAGOO.SOYBEANSDP.ENDINGSTOCKS.A",
            "Stocks/use (percent)": "USDAGOO.SOYBEANSDP.STOCKSUSE.A",
            "Season-avg. farm price ($/bu.)": "USDAGOO.SOYBEANSDP.SEASONAVGFARMPRICE.A",
            "Farm Price ($/bushel)": "USDAGOO.SOYBEANSDP.FARMPRICE.A"
        }
    },
    "SOYBEAN_MEAL": {
        "keywords": ["Soybean Meal Supply, Demand, and Price"],
        "mapping": {
            "Production (thou. short tons)": "USDAGOO.SOYBEANMEALSDP.PRODUCTION.A",
            "Beginning stocks": "USDAGOO.SOYBEANMEALSDP.BEGINNINGSTOCKS.A",
            "Imports": "USDAGOO.SOYBEANMEALSDP.IMPORTS.A",
            "Supply": "USDAGOO.SOYBEANMEALSDP.SUPPLY.A",
            "Domestic Use": "USDAGOO.SOYBEANMEALSDP.DOMESTICUSE.A",
            "Exports": "USDAGOO.SOYBEANMEALSDP.EXPORTS.A",
            "Total use": "USDAGOO.SOYBEANMEALSDP.TOTALUSE.A",
            "Ending stocks": "USDAGOO.SOYBEANMEALSDP.ENDINGSTOCKS.A",
            "Avg. price ($/short ton)": "USDAGOO.SOYBEANMEALSDP.AVGPRICE.A"
        }
    },
    "SOYBEAN_OIL": {
        "keywords": ["Soybean Oil Supply, Demand, and Price"],
        "mapping": {
            "Production (mil. lbs.)": "USDAGOO.SOYBEANOILSDP.PRODUCTION.A",
            "Beginning stocks": "USDAGOO.SOYBEANOILSDP.BEGINNINGSTOCKS.A",
            "Imports": "USDAGOO.SOYBEANOILSDP.IMPORTS.A",
            "Supply": "USDAGOO.SOYBEANOILSDP.SUPPLY.A",
            "Domestic Use": "USDAGOO.SOYBEANOILSDP.DOMESTICUSE.A",
            "Methyl Ester": "USDAGOO.SOYBEANOILSDP.METHYLESTER.A",
            "Biodiesel": "USDAGOO.SOYBEANOILSDP.BIODIESEL.A",
            "Biofuel": "USDAGOO.SOYBEANOILSDP.BIODIESEL.A",
            "Food, Feed, Other Industrial": "USDAGOO.SOYBEANOILSDP.FOODFEEDOTHERINDUSTRIAL.A",
            "Exports": "USDAGOO.SOYBEANOILSDP.EXPORTS.A",
            "Total use": "USDAGOO.SOYBEANOILSDP.TOTALUSE.A",
            "Ending stocks": "USDAGOO.SOYBEANOILSDP.ENDINGSTOCKS.A",
            "Avg. price (cents/lb.)": "USDAGOO.SOYBEANOILSDP.AVGPRICE.A"
        }
    },
    "WHEAT": {
        "keywords": ["Wheat Supply, Demand, and Price"],
        "mapping": {
            "Area planted (mil. ac.)": "USDAGOO.WHEATSDP.AREAPLANTED.A",
            "Area harvested": "USDAGOO.WHEATSDP.AREAHARVESTED.A",
            "Yield (bu./ac.)": "USDAGOO.WHEATSDP.YIELD.A",
            "Production (mil. bu.)": "USDAGOO.WHEATSDP.PRODUCTION.A",
            "Beginning stocks": "USDAGOO.WHEATSDP.BEGINNINGSTOCKS.A",
            "Imports": "USDAGOO.WHEATSDP.IMPORTS.A",
            "Supply": "USDAGOO.WHEATSDP.SUPPLY.A",
            "Feed & residual": "USDAGOO.WHEATSDP.FEEDRESIDUAL.A",
            "Food & seed": "USDAGOO.WHEATSDP.FOODSEED.A",
            "Food, seed & industrial": "USDAGOO.WHEATSDP.FOODSEEDINDUSTRIAL.A",
            "Total domestic use": "USDAGOO.WHEATSDP.TOTALDOMESTICUSE.A",
            "Exports": "USDAGOO.WHEATSDP.EXPORTS.A",
            "Total use": "USDAGOO.WHEATSDP.TOTALUSE.A",
            "Ending stocks": "USDAGOO.WHEATSDP.ENDINGSTOCKS.A",
            "Stocks/use (percent)": "USDAGOO.WHEATSDP.STOCKSUSE.A",
            "Season-avg. farm price ($/bu.)": "USDAGOO.WHEATSDP.SEASONAVGFARMPRICE.A",
            "Farm Price ($/bushel)": "USDAGOO.WHEATSDP.FARMPRICE.A"
        }
    }
}

# Metadata Attributes
METADATA_ATTRIBUTES = {
    "SOURCE": "USDA Office of the Chief Economist",
    "FREQUENCY": "Annual",
    "UNIT": "Various",
    "URL": BASE_URL
}
