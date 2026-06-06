import cloudinary
import cloudinary.uploader
import os

# ── ADD YOUR CREDENTIALS HERE ──
# Never share these with anyone!
CLOUD_NAME = "dmfrqxlgx"
API_KEY    = "419159758487968"
API_SECRET = "7Y2O4dGa0g72GwNdO-YrKBmg5IA"

# ── CONFIGURATION ──
IMAGES_FOLDER = "images"

cloudinary.config(
    cloud_name = CLOUD_NAME,
    api_key    = API_KEY,
    api_secret = API_SECRET
)

# File types to upload
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".m4v"}

def main():
    if not os.path.exists(IMAGES_FOLDER):
        print(f"❌ Could not find folder: {IMAGES_FOLDER}")
        return

    # Get all files
    files = [f for f in sorted(os.listdir(IMAGES_FOLDER))
             if not f.startswith(".")
             and os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS]

    print(f"✅ Found {len(files)} files to upload")
    print(f"Starting upload...\n")

    success = 0
    failed  = []

    for i, filename in enumerate(files, start=1):
        filepath  = os.path.join(IMAGES_FOLDER, filename)
        public_id = os.path.splitext(filename)[0]  # filename without extension
        ext       = os.path.splitext(filename)[1].lower()
        resource_type = "video" if ext in VIDEO_EXTENSIONS else "image"

        try:
            cloudinary.uploader.upload(
                filepath,
                public_id      = public_id,
                resource_type  = resource_type,
                unique_filename = False,
                overwrite      = True
            )
            success += 1
            print(f"  ✅ [{i}/{len(files)}] {filename}")
        except Exception as e:
            failed.append(filename)
            print(f"  ❌ [{i}/{len(files)}] {filename} — {e}")

    print(f"\n{'='*40}")
    print(f"✅ Successfully uploaded: {success}")
    print(f"❌ Failed: {len(failed)}")
    if failed:
        print(f"\nFailed files:")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
