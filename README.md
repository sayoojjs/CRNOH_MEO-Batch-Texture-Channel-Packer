```
##################################################
#  ________         _____  ____________________  #
# /   __   \______ /  _  \ \_   _____/\______  \ #
# \____    /  ___//  /_\  \ |    __)_     /    / #
#    /    /\___ \/    |    \|        \   /    /  #
#   /____//____  >____|__  /_______  /  /____/   #
#              \/        \/        \/            #
##################################################
#  CRNOH/MEO Texture Channel Packer 1.0          #
#  written by 9sAE7 — github.com/sayoojjs        #
##################################################
```

# CRNOH / MEO Texture Channel Packer

A batch texture channel packing tool for **Unreal Engine 5** material workflows. Drop your raw texture maps in a folder, run the script, and get packed `.TGA` files ready to import — no manual Photoshop channel work needed.

---

## What It Does

Scans a folder for texture maps and automatically packs them into optimized channel-packed textures used by UE5 material pipelines:

| Pack | Channels | Output |
|------|----------|--------|
| **CR** — BaseColor + Roughness | RGB = BaseColor, A = Roughness | `*_packed_BR.TGA` |
| **NOH** — Normal + AO + Displacement | R = Normal.R, G = Normal.G, B = AO, A = Displacement | `*_packed_NOH.TGA` |
| **MEO** — Metallic + Emissive + Opacity | R = Metallic, G = Emissive, B = Opacity | `*_packed_MEO.TGA` |

> If a texture set has Metallic / Emissive / Opacity maps, the NOH pipeline is **automatically skipped** for that set.

---

## Folder Setup

Place your textures in the **same folder** as the script. Textures must follow this naming convention:

```
📁 YourTextureFolder
 ├── CRNOHPacker.py
 ├── Rock_basecolor.png
 ├── Rock_roughness.png
 ├── Rock_normal.png
 ├── Rock_AO.png
 ├── Rock_displacement.png
 │
 ├── Glass_basecolor.png       ← MEO set — NOH will be skipped for this key
 ├── Glass_roughness.png
 ├── Glass_metallic.png
 ├── Glass_emissive.png
 └── Glass_opacity.png
```

Accepted name variants:

| Map | Accepted suffixes |
|-----|-------------------|
| Base Color | `_basecolor`, `_albedo`, `_diffuse` |
| Roughness | `_roughness` |
| Normal | `_normal` |
| Ambient Occlusion | `_ao` |
| Displacement | `_displacement` |
| Metallic | `_metallic` |
| Emissive | `_emissive` |
| Opacity | `_opacity` |

> Names are **case-insensitive**. Supported formats: `.png` `.jpg` `.jpeg` `.tga` `.tif` `.tiff` `.bmp` `.exr`

---

## Output

Packed textures are saved under a `PackedTextures/` folder created automatically next to the script:

```
📁 YourTextureFolder
 └── 📁 PackedTextures
      ├── 📁 rock
      │    ├── rock_packed_BR.TGA
      │    └── rock_packed_NOH.TGA
      └── 📁 glass
           ├── glass_packed_BR.TGA
           └── glass_packed_MEO.TGA
```

---

## Running


**Step A — Double-click `install_dependencies.bat`** (recommended for sharing):

Create a `install_dependencies.bat` in the same folder:
```bat
@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [MSG] Python not found. Downloading installer...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo [MSG] Installing Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del python_installer.exe
    echo [MSG] Python installed. Restarting script...
    timeout /t 3 >nul
    call "%~f0"
    exit
) else (
    echo [MSG] Python found. Skipping install.
)

pip install -r requirements.txt
python CRNOH-MEO_Texture_Channel_Packer.py
pause
```
**Step B — Running Python script:**
```
python CRNOH-MEO_Texture_Channel_Packer.py
```
***Or double-click and open the CRNOH-MEO_Texture_Channel_Packer.py from the working directory***
## Dependencies

```
pip install -r requirements.txt
```

```
Pillow
numpy
colorama
```

Requires **Python 3.7+**

---

## Terminal Output

The script uses color-coded logging so you can see exactly what happened at a glance:

| Color | Meaning |
|-------|---------|
| 🟢 Green `[MSG]` | Texture packed successfully |
| 🟡 Yellow `[INFO]` | Processing stage info |
| 🔵 Cyan `[SKIP]` | NOH skipped — MEO set detected |
| 🔴 Red `[ERROR]` | Missing map in a set |
| 🔵 Blue `[FIX]` | Expected filename hint |

---

## Error Handling

- **No textures found** — if the folder has no recognizable texture maps, the script exits immediately with a clear error message before creating any output folders
- **Missing map in a set** — if a texture set is incomplete (e.g. has `_normal` and `_ao` but no `_displacement`), the script reports the missing map with the expected filename and pauses for input
- **Size mismatch** — if maps in a set have different resolutions, they are automatically resized to match the first map using Lanczos resampling

---

## License

MIT — free to use, modify, and distribute.
