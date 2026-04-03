pandoc src\document.md ^
    --template=src\template.html ^
    --css=src\style.css ^
    --metadata-file=data\base.yaml ^
    --metadata-file=data\products\product.yaml ^
    --metadata-file=data\document.yaml ^
    -o build\output.pdf