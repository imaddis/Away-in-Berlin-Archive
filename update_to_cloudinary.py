import csv
import urllib.request
import json

CLOUD_NAME = "dmfrqxlgx"
INPUT_CSV  = "archive_sheets.csv"
OUTPUT_CSV = "archive_cloudinary.csv"
BASE_URL   = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/"
VIDEO_URL  = f"https://res.cloudinary.com/{CLOUD_NAME}/video/upload/"

def get_cloudinary_url(filename, file_type):
    if file_type == "video":
        return VIDEO_URL + filename
    return BASE_URL + filename

def main():
    rows = []
    missing = []
    found   = []

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["title"].strip().upper() == "DELETE":
                continue
            if not row["filename"].strip():
                continue

            filename  = row["filename"].strip()
            file_type = row["type"].strip()

            # Build new Cloudinary URL
            new_url = get_cloudinary_url(filename, file_type)

            # Check if file exists on Cloudinary
            try:
                req = urllib.request.Request(new_url, method="HEAD")
                urllib.request.urlopen(req, timeout=5)
                found.append(filename)
                row["src"] = new_url
            except Exception:
                missing.append(filename)
                # Keep old src so we know what's missing
                print(f"  ❌ Missing: {filename}")

            rows.append(row)

    # Write updated CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Found on Cloudinary: {len(found)}")
    print(f"❌ Missing from Cloudinary: {len(missing)}")
    if missing:
        print(f"\nMissing files:")
        for f in missing:
            print(f"  - {f}")
    print(f"\n✅ Updated CSV saved as '{OUTPUT_CSV}'")
    print(f"Bring '{OUTPUT_CSV}' back to Claude to generate the final website code!")

if __name__ == "__main__":
    main()
