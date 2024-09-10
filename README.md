Ai tagging for danbooru-like pictures

## Simple usage

1. Download [latest release](https://github.com/ImoutoChan/AiTag/releases/latest)
2. Extract zip archive to a folder
3. Run

```powershell
./aitag.exe --dry-run
```
or

```powershell
./aitag.exe "c:\images\1.png" "c:\images\2.png" "c:\images\3.png" "c:\images\4.png"
```

## Advanced 
## Set up repo (powershell)

### get latest deepdanbooru (not nessesary)
```powershell
git clone https://github.com/KichangKim/DeepDanbooru Source
Copy-Item ./Source/deepdanbooru . -Recurse -Force
Remove-Item ./Source -Force -Recurse
```

### prepare deepdanbooru model
```powershell
$zipUrl = "https://github.com/KichangKim/DeepDanbooru/releases/download/v3-20211112-sgd-e28/deepdanbooru-v3-20211112-sgd-e28.zip"
$zipPath = "$Pwd\deepdanbooru.zip"
$extractPath = "$Pwd\model"

Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

if (-not (Test-Path $extractPath)) { New-Item -Path $extractPath -ItemType Directory }

Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
Remove-Item $zipPath -Force
```

### prepare python (you can install it with choco https://community.chocolatey.org/packages/python)
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r .\requirements.txt
```

### sample runs
```powershell
python aitag.py "path-to-file1.jpg", "path-to-file2.jpg"
python aitag.py "--dry-run"
```

## Build
```powershell
pyinstaller --onedir --add-data "model;model" aitag.py
```

```powershell
# test run
.\dist\aitag\aitag.exe --dry-run
```

## Based on
* https://github.com/KichangKim/DeepDanbooru
* https://github.com/sky-cake/ddb_scripts