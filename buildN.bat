@echo off

for %%f in (data\products/*.yaml) do (
    pandoc src\document.md ^
        --template=src\template.html ^
        --css=src\style.css ^
        --metadata-file=data\base.yaml ^
        --metadata-file=data\products/%%~nf.yaml ^
        --metadata-file=data\document.yaml ^
        -o build\passport_%%~nf.pdf

    echo Собран: passport_%%~nf.pdf
)