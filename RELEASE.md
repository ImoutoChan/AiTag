### Ai tagging for anime pictures

1. Download the [latest release](https://github.com/ImoutoChan/AiTag/releases/latest).
2. Extract the zip archive to a folder.
3. Run the following command in PowerShell:

```powershell
./aitag.exe --dry-run
```

or

```powershell
./aitag.exe "c:\images\1.png" "c:\images\2.png" "c:\images\3.png" "c:\images\4.png"
```

The tag results will be stored in files named {md5}.json in the current working folder.