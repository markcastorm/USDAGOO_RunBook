import sys
import logging
import orchestrator

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )

def main():
    setup_logging()
    try:
        orchestrator.run_pipeline()
    except Exception as e:
        logging.error(f"Critical error in pipeline: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
