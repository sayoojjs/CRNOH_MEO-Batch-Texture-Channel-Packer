from PIL import Image
import numpy as np
import os
import sys
from colorama import init
init()

#---------------------BANNER-----------------------
def show_banner():
   CYAN = "\033[96m"
   RESET = "\033[0m"
   print(CYAN + """
##################################################
#  ________         _____  ____________________  #
# /   __   \______ /  _  \ \_   _____/\______  \ #
# \____    /  ___//  /_\  \ |    __)_     /    / #
#    /    /\___ \/    |    \|        \   /    /  #
#   /____//____  >____|__  /_______  /  /____/   #
#              \/        \/        \/            #
##################################################
#   CRNOH/MEO Batch Texture Channel Packer 1.0   # 
#     written by 9sAE7 — github.com/sayoojjs     #
##################################################
""" + RESET)

#-----------TEXTURE DETECTION CHECK----------------
def check_for_valid_textures(input_folder: str):
 
   RED         = "\033[91m"
   LIGHT_WHITE = "\033[97m"
   RESET       = "\033[0m"

   KNOWN_KEYWORDS = [
      "basecolor", "albedo", "diffuse", "roughness",
      "normal", "ao", "displacement",
      "metallic", "emissive", "opacity"
   ]

   IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tga", ".tif", ".tiff", ".bmp", ".exr"}

   found = False
   for file in os.listdir(input_folder):
      name, ext = os.path.splitext(file)
      if ext.lower() not in IMAGE_EXTENSIONS:
         continue
      lower = name.lower()
      if any(kw in lower for kw in KNOWN_KEYWORDS):
         found = True
         break

   if not found:
      print(RED + "\n[ERROR] No texture maps found for channel packing!" + RESET)
      print(LIGHT_WHITE + "        Make sure your textures are in the same folder as this script" + RESET)
      print(LIGHT_WHITE + "        and follow the naming convention:" + RESET)
      print(LIGHT_WHITE + "        e.g.  Rock_basecolor.png  Rock_roughness.png  Rock_normal.png" + RESET)
      input("\nPress Enter to quit...")
      sys.exit(1)

#-----------------------FILE LOADERS---------------------
def load_as_array(path: str, mode: str = "RGB") -> np.ndarray:
    img = Image.open(path).convert(mode)
    return np.array(img, dtype=np.uint8)

def load_grayscale(path: str) -> np.ndarray:
    return load_as_array(path, mode="L")

def ensure_same_size(*arrays: np.ndarray, size: tuple = None) -> list:

    if size is None:

     h, w = arrays[0].shape[:2]
     size = (w, h)

     resized = []
     for arr in arrays:
      img = Image.fromarray(arr)
      img = img.resize(size, Image.LANCZOS)
      resized.append(np.array(img, dtype=np.uint8))
    return resized


#----------------BASE COLOR + ROUGHNESS PACKER-----------------
def pack_basecolor_roughnes(
      base_color_path: str,
      roughness_path: str,
      output_path: str
):
   
   GREEN   = "\033[92m"
   RESET = "\033[0m"
   base_color = load_as_array(base_color_path, mode="RGB")
   roughness = load_grayscale(roughness_path)

   base_color, roughness = ensure_same_size(base_color, roughness)

   r = base_color[:, :, 0]
   g = base_color[:, :, 1]
   b = base_color[:, :, 2]
   a = roughness

   packed = np.stack([r, g, b, a], axis=-1)
   result = Image.fromarray(packed, mode="RGBA")
   result.save(output_path)
   print(GREEN + f"[MSG] (CR Pack) Saved Basecolor + Roughness -> {output_path}" + RESET)

#---------------NORMAL AO DISPLACEMENT PACKER-------------------
def pack_normal_ao_displacement(
      normal_path: str,
      AO_path: str,
      displacement_path: str,
      output_path: str,
):
        GREEN   = "\033[92m"
        RESET = "\033[0m"

        normal = load_as_array(normal_path, mode="RGB")
        AO = load_grayscale(AO_path)
        displacement = load_grayscale(displacement_path)

        normal, AO, displacement = ensure_same_size(normal, AO, displacement)

        r = normal[:, :, 0]
        g = normal[:, :, 1]
        b = AO
        a = displacement

        packed = np.stack([r, g, b, a], axis=-1)

        result = Image.fromarray(packed, mode="RGBA")
        result.save(output_path)
        print(GREEN + f"[MSG] (NOH Pack) Saved Normal + AO + Displacement -> {output_path}" + RESET)

#-----------METALLIC EMISSIVE OPACITY PACKER--------------------
def pack_metallic_emissive_opacity(
      metallic_path: str,
      emissive_path: str,
      opacity_path: str,
      output_path: str,
):
        GREEN   = "\033[92m"
        RESET = "\033[0m"

        metallic    = load_grayscale(metallic_path)
        emissive    = load_grayscale(emissive_path)
        opacity     = load_grayscale(opacity_path)

        metallic, emissive, opacity = ensure_same_size(metallic, emissive, opacity)

        packed = np.stack([metallic, emissive, opacity], axis=-1)

        result = Image.fromarray(packed, mode="RGB")
        result.save(output_path)
        print(GREEN + f"[MSG] (MEO Pack) Saved Metallic + Emissive + Opacity -> {output_path}" + RESET)

def extract_key(name):
    parts = name.split("_")
    return "_".join(parts[:-1])

#---------------BATCH PROCESS CR------------------
def batch_pack_br(input_folder: str, output_folder: str):
    
   RED     = "\033[91m" 
   BLUE    = "\033[34m"
   RESET = "\033[0m"

   files = os.listdir(input_folder)
   texture_sets = {}
   
   for file in files:
       name, ext = os.path.splitext(file)
       full_path = os.path.join(input_folder, file)
       lower = name.lower()

       if any(x in lower for x in ["basecolor", "albedo", "diffuse"]):
          key = extract_key(lower)
          texture_sets.setdefault(key, {})["basecolor"] = full_path

       elif "roughness" in name.lower():
          key = name.lower().replace("_roughness", "")
          texture_sets.setdefault(key, {})["roughness"] = full_path

   for key, maps in texture_sets.items():
      if "basecolor" in maps and "roughness" in maps:
         texture_folder = os.path.join(output_folder, key)
         os.makedirs(texture_folder, exist_ok=True)
         output_path = os.path.join(texture_folder, f"{key}_packed_BR.TGA")
      
         pack_basecolor_roughnes(
           base_color_path=maps["basecolor"],
           roughness_path=maps["roughness"],
           output_path=output_path
         )    
      else:
          print(RED + f"[ERROR] (CR Packing skip) Missing maps for {key}" + RESET)
          print(BLUE + f"[FIX] The filename must be {key}_basecolor / Albedo / Diffuse, {key}_roughness" + RESET)
          input("\nPress Enter to abort...")

#----------------BATCH PROCESS NOH------------------
def batch_pack_noh(input_folder: str, output_folder: str, skip_keys: set = None):

   RED     = "\033[91m" 
   BLUE    = "\033[34m"
   CYAN    = "\033[96m"
   RESET = "\033[0m"

   if skip_keys is None:
      skip_keys = set()

   files = os.listdir(input_folder)
   texture_sets = {}

   for file in files:
      name, ext = os.path.splitext(file)
      full_path = os.path.join(input_folder, file)
      lower = name.lower()
      
      if "normal" in lower:
         key = lower.replace("_normal", "")
         texture_sets.setdefault(key, {})["normal"] = full_path

      elif "ao" in lower:
         key = lower.replace("_ao", "")
         texture_sets.setdefault(key, {})["ao"] = full_path

      elif "displacement" in lower:
         key = lower.replace("_displacement", "")
         texture_sets.setdefault(key, {})["displacement"] = full_path

   for key, maps in texture_sets.items():
      if key in skip_keys:
         print(CYAN + f"[SKIP] {key} — Metallic, Emissive, Opacity maps are detected for this texture set, skipping NOH packing pipeline" + RESET)
         continue

      if all(k in maps for k in ["normal", "ao", "displacement"]):
         texture_folder = os.path.join(output_folder, key)
         os.makedirs(texture_folder, exist_ok=True)
         output_path = os.path.join(texture_folder, f"{key}_packed_NOH.TGA")

         pack_normal_ao_displacement(
            normal_path=maps["normal"],
            AO_path=maps["ao"],
            displacement_path=maps["displacement"],
            output_path=output_path
         )
      else:
         print(RED + f"[ERROR] (NOH Packing Skip) Missing maps for {key}" + RESET)  
         print(BLUE + f"[FIX] The filename must be {key}_normal, {key}_AO, {key}_displacement" + RESET)
         input("\nPress Enter to abort...")

#----------------BATCH PROCESS MEO------------------
def batch_pack_meo(input_folder: str, output_folder: str) -> set:
  
   RED     = "\033[91m"
   BLUE    = "\033[34m"
   RESET   = "\033[0m"

   files = os.listdir(input_folder)
   texture_sets = {}
   meo_packed_keys = set()

   for file in files:
      name, ext = os.path.splitext(file)
      full_path = os.path.join(input_folder, file)
      lower = name.lower()

      if "metallic" in lower:
         key = lower.replace("_metallic", "")
         texture_sets.setdefault(key, {})["metallic"] = full_path

      elif "emissive" in lower:
         key = lower.replace("_emissive", "")
         texture_sets.setdefault(key, {})["emissive"] = full_path

      elif "opacity" in lower:
         key = lower.replace("_opacity", "")
         texture_sets.setdefault(key, {})["opacity"] = full_path

   for key, maps in texture_sets.items():
      if all(k in maps for k in ["metallic", "emissive", "opacity"]):
         texture_folder = os.path.join(output_folder, key)
         os.makedirs(texture_folder, exist_ok=True)
         output_path = os.path.join(texture_folder, f"{key}_packed_MEO.TGA")

         pack_metallic_emissive_opacity(
            metallic_path=maps["metallic"],
            emissive_path=maps["emissive"],
            opacity_path=maps["opacity"],
            output_path=output_path
         )
         meo_packed_keys.add(key)
      else:
         print(RED + f"[ERROR] (MEO Packing Skip) Missing maps for {key}" + RESET)
         print(BLUE + f"[FIX] The filename must be {key}_metallic, {key}_emissive, {key}_opacity" + RESET)
         input("\nPress Enter to abort...")

   return meo_packed_keys

#-------------------CLEAR SCREEN-------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#------------------MAIN-------------------
if __name__ == "__main__" :
  
  YELLOW      = "\033[93m"
  MAGENTA     = "\033[95m"
  LIGHT_WHITE = "\033[97m"
  ORANGE      = "\033[33m"
  UNDERLINE   = "\033[4m"
  RESET       = "\033[0m"

  clear_screen()
  show_banner()
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))

  input_folder = BASE_DIR
  root_output = os.path.join(BASE_DIR, "PackedTextures")

  # ── EARLY EXIT IF NO VALID TEXTURES FOUND ───────────────────────────────────
  check_for_valid_textures(input_folder)

  os.makedirs(root_output, exist_ok=True)
  print(LIGHT_WHITE + UNDERLINE + f"NOTE - Directory has been created for this batch '{input_folder}\PackedTextures'" + RESET)

  # ── CR ──────────────────────────────────────────────────────────────────────
  print(ORANGE + r""" 
--------------------------------------------------------       
----------BASE COLOR + ROUGHNESS BATCH RUNNING----------
--------------------------------------------------------
                      Output Log"""+ RESET)
  print(YELLOW + f"[INFO] Processing CR pack -> {root_output}" + RESET)
  batch_pack_br(input_folder, root_output)

  # ── MEO ─────────────────────────────────────────────────────────────────────
  print(ORANGE + r""" 
--------------------------------------------------------       
------METALLIC + EMISSIVE + OPACITY BATCH RUNNING-------
--------------------------------------------------------
                      Output Log""" + RESET)
  print(YELLOW + f"[INFO] Processing MEO pack -> {root_output}" + RESET)
  meo_keys = batch_pack_meo(input_folder, root_output)

  # ── NOH (skip MEO texture sets) ─────────────────────────────────────────────
  print(ORANGE + r""" 
--------------------------------------------------------       
-------NORMAL + AO + DISPLACEMENT BATCH RUNNING---------
--------------------------------------------------------
                     Output Log""" + RESET)
  print(YELLOW + f"[INFO] Processing NOH pack -> {root_output}" + RESET)
  batch_pack_noh(input_folder, root_output, skip_keys=meo_keys)

  print(ORANGE + "\n #############################################" + RESET)
  print(LIGHT_WHITE + "\n \033[42m          -> Batch is completed! <-         " + RESET)
  print(MAGENTA + "\n    Files are under PackedTextures folder   " + RESET)
  print(ORANGE + "\n #############################################" + RESET)
  input("\nPress Enter to quit...")

