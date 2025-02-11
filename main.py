import argparse
from lib.af3_downloader import AF3Downloader

def main():
    parser = argparse.ArgumentParser(
        description="Automatically download structures from the AlphaFold 3 server."
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the extracted download links to a CSV file."
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="links.csv",
        help="Path to save the CSV file (default: links.csv)."
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the files after extracting the links."
    )
    args = parser.parse_args()

    downloader = AF3Downloader(debugger_address="127.0.0.1:9222")
    
    # Navigate to AlphaFold 3 site
    print('Going to AlphaFold 3 website')
    downloader.driver.get("https://alphafoldserver.com/")
    # Pause for the user to log in
    input("Please log in with your Google account in the opened Chrome window and press Enter to continue...")

    # Extract download links
    print("Extracting download links...")
    links = downloader.get_download_links()
    print(f"Total links found: {len(links)} (Unique: {len(set(links))})")

    # Optionally save links to CSV
    if args.save:
        downloader.save_links_csv(links, args.csv)

    # Optionally download files
    if args.download:
        print("Starting downloads...")
        downloader.download_files(links)

    downloader.close()

if __name__ == "__main__":
    main()
