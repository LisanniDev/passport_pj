#!/bin/bash

for file in data/products/*.yaml
do
  filename=$(basename "$file" .yaml)

  pandoc src/document.md \
    --template=src/template.html \
    --css=src/style.css \
    --metadata-file=data/base.yaml \
    --metadata-file="$file" \
    --metadata-file=data/document.yaml \
    -o "build/passport_$filename.pdf"

    echo "Собран:  passport_$filename.pdf"
done
