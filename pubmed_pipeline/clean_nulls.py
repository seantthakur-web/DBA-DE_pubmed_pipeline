import os

# Target directory to clean
TARGET_DIR = "etl"

for root, _, files in os.walk(TARGET_DIR):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            with open(path, "rb") as fr:
                data = fr.read()
            if b"\x00" in data:
                print(f"🧹 Removing null bytes from {path}")
                cleaned = data.replace(b"\x00", b"")
                with open(path, "wb") as fw:
                    fw.write(cleaned)

print("✅ Cleanup complete. All .py files sanitized.")
