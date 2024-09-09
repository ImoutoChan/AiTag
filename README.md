Ai tagging for danbooru-like pictures

# Set Up (powershell)

```powershell
# get latest deepdanbooru (not nessesary)
git clone https://github.com/KichangKim/DeepDanbooru Source
Copy-Item ./Source/deepdanbooru . -Recurse -Force
Remove-Item ./Source -Force -Recurse

# prepare deepdanbooru model
$zipUrl = "https://github.com/KichangKim/DeepDanbooru/releases/download/v3-20211112-sgd-e28/deepdanbooru-v3-20211112-sgd-e28.zip"
$zipPath = "$Pwd\deepdanbooru.zip"
$extractPath = "$Pwd\model"

Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

if (-not (Test-Path $extractPath)) { New-Item -Path $extractPath -ItemType Directory }

Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
Remove-Item $zipPath -Force

#prepare python (you can install it with choco https://community.chocolatey.org/packages/python)
python -m venv .venv
.\.venv\Scripts\activate
pip install -r .\requirements.txt

#python aitag.py "path-to-file1.jpg", "path-to-file2.jpg"
python aitag.py "--dry-run"

```

# Build

```powershell
pyinstaller --onedir --add-data "model;model" aitag.py

# test run
.\dist\aitag\aitag.exe --dry-run
```

# Based on
https://github.com/KichangKim/DeepDanbooru
https://github.com/sky-cake/ddb_scripts