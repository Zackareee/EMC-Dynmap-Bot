> [!IMPORTANT]
> The Discord Dynmap Bot implementation has been depricated and is still available on the `discord` branch. This version has historical tracking built in, whereas the rewrite will not include tracking until v0.3 is released. 

# EMCMap 🗺️

**EMCMap**  is a Python module and command-line tool for rendering images of towns or nations from [EarthMC](map.earthmc.net).   
It supports specifying multiple towns or nations, customizing the output filename, and enabling an **uncropped mode** for full-area renders.

---

## 👥 Installation

1. **Clone the repository:**

2. **Ensure Python is installed** (Python 3.12+ required).

3. **Install dependencies (if any):**
   ```sh
   pip install -r requirements.txt
   ```
4. **Install the module locally (optional for easier imports):**
   ```sh
   pip install .
   ```
---

## 🛠️ Usage

### **As a Command-Line Tool**

#### **Basic Command**
Render a list of towns into an image:
```sh
python -m emcmap -t town1 town2 town3
```
- The output will be saved as `out.png` by default.

Render a list of nations:
```sh
python -m emcmap -n nation1 nation2
```

---

#### **Custom Output Filename**
Specify a different output filename:
```sh
python -m emcmap -t town1 town2 -o mymap.jpg
```
- This will save the rendered image as `mymap.jpg`.

---

#### **Uncropped Mode**
By default, the rendered image is cropped.  
To disable cropping, use the `-uc` flag:
```sh
python -m emcmap -t town1 town2 -uc
```

---

## 🔍 Examples

#### **Rendering towns with a custom output file**
```sh
python emcmap.py -t spawn town1 -o render.png
```
👉 **Output:** `render.png`

#### **Rendering nations in uncropped mode**
```sh
python emcmap.py -n empire1 empire2 -o nations.svg -uc
```
👉 **Output:** `nations.svg` (uncropped)

``python emcmap.py -t limerick``

![out](https://github.com/user-attachments/assets/a7ce5b01-0f9b-4ee7-a910-97eea70e4b4e)

``python emcmap.py -n United_Kingdom``

![out](https://github.com/user-attachments/assets/91b6dfd9-8205-4acd-ac30-8588464b43ce)

---

## 🤖 Running Tests
You can run tests using `pytest`:
```sh
pytest
```

---

## ⚠️ Supported File Formats
The following output formats are supported:
- **PNG** (`.png`)
- **JPG** / **JPEG** (`.jpg`, `.jpeg`)
- **SVG** (`.svg`)

If an invalid format is specified, the script will show an error.

---
