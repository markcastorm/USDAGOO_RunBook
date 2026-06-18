import fitz
import scraper
import extractor
import file_generator
import config

def run_pipeline():
    print(f"{'='*50}")
    print(f"Starting {config.DATASET_NAME} Pipeline")
    print(f"{'='*50}")
    
    # Step 1: Scrape
    print("\n[Step 1/3] Scraping for latest PDF...")
    pdf_path, target_year = scraper.scrape()
    
    if not pdf_path:
        print("Pipeline failed at Step 1: Scraper could not find the PDF.")
        return
        
    # Step 2: Extract
    print(f"\n[Step 2/3] Extracting data from {pdf_path}...")
    df = extractor.extract_all(pdf_path)
    
    if df is None or df.empty:
        print("Pipeline failed at Step 2: Extractor could not find target tables.")
        return
        
    # Get PDF metadata for release date
    doc = fitz.open(pdf_path)
    pdf_metadata = doc.metadata
    doc.close()
    
    # Step 3: Generate Files
    print("\n[Step 3/3] Generating output files...")
    zip_path = file_generator.generate_files(df, pdf_metadata, target_year)
    
    print(f"\n{'='*50}")
    print(f"Pipeline finished successfully!")
    print(f"Final output: {zip_path}")
    print(f"{'='*50}")

if __name__ == "__main__":
    run_pipeline()
