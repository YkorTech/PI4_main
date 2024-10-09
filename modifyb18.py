import re
import subprocess
import os
import time
# import pyautogui

def process_b18_with_trnbuild(b18_file):
    trnbuild_exe = r"C:\TRNSYS18\Building\TRNBuild.exe"
    
    if not os.path.exists(trnbuild_exe):
        raise FileNotFoundError(f"TRNBuild executable not found at {trnbuild_exe}")
    
    # Construire la commande
    command = [trnbuild_exe, b18_file,"/N"]
    
    try:
        # # Exécuter TRNBuild
        # process = subprocess.Popen(command)
        
        # # Attendre que TRNBuild s'ouvre
        # time.sleep(5)
        
        # # Fermer TRNBuild
        # pyautogui.hotkey('alt', 'f4')
        
        # # Attendre l'apparition de la boîte de dialogue de sauvegarde
        # time.sleep(2)
        
        # # Appuyer sur 'Enter' pour confirmer la sauvegarde
        # pyautogui.press('enter')
        
        # # Attendre l'apparition de la fenêtre de génération des matrices
        # time.sleep(2)
        
        # # Cliquer sur le bouton "play" pour générer les matrices
        # pyautogui.press('tab', presses=2)  # Ajustez le nombre de pressions selon le focus initial
        # pyautogui.press('enter')
        
        # # Attendre que TRNBuild se ferme complètement
        # process.wait()
        
        print(f"TRNBuild processing completed for {b18_file}")
        
        # # Vérifier si les fichiers nécessaires ont été créés
        # expected_files = [f"{os.path.splitext(b18_file)[0]}.{ext}" for ext in ['bld', 'inf', 'trn', 'vfm', 'ism', 'log']]
        # for file in expected_files:
        #     if not os.path.exists(file):
        #         print(f"Warning: Expected file {file} was not created.")
        
        return True
    except Exception as e:
        print(f"Error processing {b18_file} with TRNBuild: {e}")
        return False



def modify_b18_file(input_file, output_file, modifications):
    with open(input_file, 'r') as file:
        content = file.read()

    # Modification des LAYERs
    for layer_name, layer_props in modifications.get('LAYERS', {}).items():
        pattern = rf'(LAYER {layer_name}\s*\n\s*CONDUCTIVITY\s*=\s*)[\d.]+(\s*:\s*CAPACITY\s*=\s*)[\d.]+(\s*:\s*DENSITY\s*=\s*)[\d.]+'
        replacement = rf'\g<1>{layer_props["conductivity"]}\g<2>{layer_props["capacity"]}\g<3>{layer_props["density"]}'
        content = re.sub(pattern, replacement, content)

    # Modification des CONSTRUCTIONs
    for const_name, const_props in modifications.get('CONSTRUCTIONS', {}).items():
        pattern = rf'(CONSTRUCTION {const_name}\s*\n\s*LAYERS\s*=\s*[^\n]+\s*\n\s*THICKNESS\s*=\s*)[\d.\s]+'
        replacement = rf'\1{" ".join([f"{t:8.3f}" for t in const_props["thickness"]])}\n'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Modification des WINDOWs
    for window_name, window_id in modifications.get('WINDOWS', {}).items():
        pattern = rf'(WINDOW {window_name}\s*\n\s*WINID\s*=\s*)\d+'
        replacement = rf'\g<1>{window_id}'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Modification des ZONEs
    for zone_name, zone_props in modifications.get('ZONES', {}).items():
        # Modification des constructions dans les zones
        for surface_type, construction in zone_props.get('constructions', {}).items():
            pattern = rf'(ZONE {zone_name}[^Z]+{surface_type}\s*=\s*)[^\s:]+'
            replacement = rf'\g<1>{construction}'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Modification des fenêtres dans les zones
        for window_name, window_type in zone_props.get('windows', {}).items():
            pattern = rf'(ZONE {zone_name}[^Z]+WINDOW\s*=\s*{window_name}\s*:\s*WINID\s*=\s*)\d+'
            replacement = rf'\g<1>{window_type}'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Modification des régimes dans les zones
        for regime_name, regime_scale in zone_props.get('regimes', {}).items():
            pattern = rf'(ZONE {zone_name}[^Z]+GAIN\s*=\s*{regime_name}\s*:\s*SCALE\s*=\s*)[\d.]+'
            replacement = rf'\g<1>{regime_scale}'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Obtenir le chemin absolu du fichier de sortie
    output_file_path = os.path.abspath(output_file)

    with open(output_file_path, 'w') as file:
        file.write(content)
    
    # Utiliser process_b18_with_trnbuild pour créer les fichier bld, inf, trn etc
    process_b18_with_trnbuild(output_file_path)

# Exemple d'utilisation
modifications = {
    'LAYERS': {
        'EpsType1': {'conductivity': 0.1, 'capacity': 1.5, 'density': 15},
    },
    'CONSTRUCTIONS': {
        'ExtWall': {'thickness': [0.1, 0, 0.08, 0.04, 0, 0.19]},
    },
    'WINDOWS': {
        'EXT_WINDOW1': 6503,
        'EXT_WINDOW2': 6503,
    },
}

# modify_b18_file('Simple-Step3.b18', 'Modified-Simple-Step3_1.b18', modifications)

input_file = "./outputs/Simple-Step3.b18"
output_file = "./outputs/Modified-Simple-Step3_3.b18"

modify_b18_file(input_file, output_file, modifications)