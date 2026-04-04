import yaml
import subprocess
import glob
for file in glob.glob("data/products/*.yaml"):
    with open(file, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    code = data["product"]["designation"]
    execution = data["product"]["execution"]
    version = data["product"]["version"]
    output = f"build/{code}-{execution}ПС_{version}.pdf"
    subprocess.run([
        "pandoc",
        "src/document.md",
        "--template=src/template.html",
        "--css=src/styles.css",
        "--metadata-file=data/base.yaml",
        "--metadata-file=" + file,
        "-o", output,
        "--pdf-engine=xelatex"
    ])
    print(f"Собран: {output}")