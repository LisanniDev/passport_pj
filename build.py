# =========================
# build.py
# =========================
import os
import sys
import subprocess
from pathlib import Path
from weasyprint import HTML
import yaml

BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
BUILD_DIR = BASE_DIR / "build"
ASSETS_DIR = BASE_DIR / "assets"

BUILD_DIR.mkdir(exist_ok=True)

# -------------------------
# CONFIG
# -------------------------
SECTIONS = [
    "00-cover.html",
    "document.md"
]

TEMPLATE = SRC_DIR / "template.html"
CSS = SRC_DIR / "styles.css"
BASE_YAML = DATA_DIR / "base.yaml"

# -------------------------
# PRODUCTS (batch mode)
# -------------------------
PRODUCTS_DIR = DATA_DIR / "products"

# if argument passed → build one product
# else → build all
if len(sys.argv) > 1:
    PRODUCTS = [sys.argv[1]]
else:
    PRODUCTS = [p.stem for p in PRODUCTS_DIR.glob("*.yaml")]

# temp file
COMBINED_MD = BUILD_DIR / "combined.md"
COMBINED_MD = BUILD_DIR / "combined.md"

# -------------------------
# STEP 1: MERGE FILES
# -------------------------
def merge_files():
    with open(COMBINED_MD, "w", encoding="utf-8") as out:
        for file in SECTIONS:
            path = SRC_DIR / file
            if not path.exists():
                raise FileNotFoundError(f"Missing file: {path}")
            with open(path, encoding="utf-8") as f:
                out.write(f.read() + "\n\n")

# -------------------------
# STEP 2: RUN PANDOC
# -------------------------
def run_pandoc():
    cmd = [
        "pandoc",
        str(COMBINED_MD),
        "-o", str(OUTPUT_HTML),
        "--css", str(CSS),
        "--template", str(TEMPLATE),
        "--metadata-file", str(BASE_YAML),
        "--metadata-file", str(PRODUCT_YAML),
        "--resource-path", f"{SRC_DIR}:{ASSETS_DIR}"
    ]

    subprocess.run(cmd, check=True)

# -------------------------
# STEP 3: HTML → PDF
# -------------------------
def build_pdf():
    HTML(str(OUTPUT_HTML)).write_pdf(str(OUTPUT_PDF))

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    for product in PRODUCTS:
        print(f"
=== Building product: {product} ===")

        PRODUCT_YAML = PRODUCTS_DIR / f"{product}.yaml"

        if not PRODUCT_YAML.exists():
            print(f"[ERROR] Missing YAML: {PRODUCT_YAML}")
            continue

        # -------------------------
        # READ YAML VARIABLES
        # -------------------------
        with open(PRODUCT_YAML, encoding="utf-8") as f:
            ydata = yaml.safe_load(f) or {}

        code = ydata.get("code", product)
        execution = ydata.get("execution", "unknown")
        version = ydata.get("version", "v0")

        filename = f"{code}-{execution}_{version}"

        OUTPUT_HTML = BUILD_DIR / f"{filename}.html"
        OUTPUT_PDF = BUILD_DIR / f"{filename}.pdf"

        merge_files()

        cmd = [
            "pandoc",
            str(COMBINED_MD),
            "-o", str(OUTPUT_HTML),
            "--css", str(CSS),
            "--template", str(TEMPLATE),
            "--metadata-file", str(BASE_YAML),
            "--metadata-file", str(PRODUCT_YAML),
            "--resource-path", f"{SRC_DIR}:{ASSETS_DIR}"
        ]

        subprocess.run(cmd, check=True)

        HTML(str(OUTPUT_HTML)).write_pdf(str(OUTPUT_PDF))

        print(f"[OK] PDF generated: {OUTPUT_PDF}")

    print("
=== Done ===")
