import sqlite3
from modifyb18 import modify_b18_file
from modifydck import modify_dck_file
from modifydat import modify_dat_file
import subprocess
import os
import time
import pyautogui

def process_b18_with_trnbuild(b18_file):
    trnbuild_exe = r"C:\TRNSYS18\Building\TRNBuild.exe"
    
    if not os.path.exists(trnbuild_exe):
        raise FileNotFoundError(f"TRNBuild executable not found at {trnbuild_exe}")
    
    # Construire la commande
    command = [trnbuild_exe, b18_file]
    
    try:
        # Exécuter TRNBuild
        process = subprocess.Popen(command)
        
        # Attendre que TRNBuild s'ouvre
        time.sleep(5)
        
        # Fermer TRNBuild
        pyautogui.hotkey('alt', 'f4')
        
        # Attendre l'apparition de la boîte de dialogue de sauvegarde
        time.sleep(2)
        
        # Appuyer sur 'Enter' pour confirmer la sauvegarde
        pyautogui.press('enter')
        
        # Attendre l'apparition de la fenêtre de génération des matrices
        time.sleep(2)
        
        # Cliquer sur le bouton "play" pour générer les matrices
        pyautogui.press('tab', presses=2)  # Ajustez le nombre de pressions selon le focus initial
        pyautogui.press('enter')
        
        # Attendre que TRNBuild se ferme complètement
        process.wait()
        
        print(f"TRNBuild processing completed for {b18_file}")
        
        # Vérifier si les fichiers nécessaires ont été créés
        expected_files = [f"{os.path.splitext(b18_file)[0]}.{ext}" for ext in ['bld', 'inf', 'trn', 'vfm', 'ism', 'log']]
        for file in expected_files:
            if not os.path.exists(file):
                print(f"Warning: Expected file {file} was not created.")
        
        return True
    except Exception as e:
        print(f"Error processing {b18_file} with TRNBuild: {e}")
        return False


def get_db_connection():
    return sqlite3.connect('batiments.db')

def get_type_batiments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TypesBatiments")
    types = cursor.fetchall()
    conn.close()
    return types

def get_regions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Regions")
    regions = cursor.fetchall()
    conn.close()
    return regions

def get_periodes_construction():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PeriodesConstruction")
    periodes = cursor.fetchall()
    conn.close()
    return periodes

def generate_b18_modifications(type_batiment_id, region_id, periode_construction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtenir les modifications spécifiques pour cette combinaison
    cursor.execute("""
        SELECT c.Nom, cc.Epaisseur, m.Conductivite, m.Capacite, m.Densite
        FROM Constructions c
        JOIN CouchesConstruction cc ON c.ID = cc.ConstructionID
        JOIN Materiaux m ON cc.MateriauID = m.ID
        WHERE c.TypeBatimentID = ? AND c.RegionID = ? AND c.PeriodeConstructionID = ?
    """, (type_batiment_id, region_id, periode_construction_id))
    
    constructions = cursor.fetchall()
    
    # Créer le dictionnaire de modifications
    modifications = {
        'CONSTRUCTIONS': {},
        'LAYERS': {},
        'WINDOWS': {},
        'ZONES': {}
    }
    
    for const in constructions:
        const_name, thickness, conductivity, capacity, density = const
        if const_name not in modifications['CONSTRUCTIONS']:
            modifications['CONSTRUCTIONS'][const_name] = {'thickness': []}
        modifications['CONSTRUCTIONS'][const_name]['thickness'].append(thickness)
        
        layer_name = f"Layer_{const_name}_{len(modifications['CONSTRUCTIONS'][const_name]['thickness'])}"
        modifications['LAYERS'][layer_name] = {
            'conductivity': conductivity,
            'capacity': capacity,
            'density': density
        }
    
    # Ajouter d'autres modifications nécessaires (fenêtres, zones, etc.)
    
    conn.close()
    return modifications

def generate_dck_modifications(region_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT FichierClimatique FROM Regions WHERE ID = ?", (region_id,))
    weather_file = cursor.fetchone()[0]
    conn.close()
    
    return {
        'WEATHER_FILE': os.path.splitext(os.path.basename(weather_file))[0],
        # Ajouter d'autres modifications nécessaires
    }

def run_trnsys_simulation(dck_file):
    trnsys_exe = r"C:\TRNSYS18\Exe\TrnEXE64.exe"
    command = [trnsys_exe, dck_file]
    
    try:
        subprocess.run(command, check=True)
        print(f"Simulation completed successfully for {dck_file}")
        return True
    except subprocess.CalledProcessError:
        print(f"Error running simulation for {dck_file}")
        return False

def main():
    types_batiments = get_type_batiments()
    regions = get_regions()
    periodes = get_periodes_construction()
    
    dck_files_to_simulate = []
    
    for type_batiment in types_batiments:
        for region in regions:
            for periode in periodes:
                # Générer les noms de fichiers
                base_name = f"{type_batiment[1]}_{region[1]}_{periode[1]}"
                b18_file = f"{base_name}.b18"
                dck_file = f"{base_name}.dck"
                
                # Générer et appliquer les modifications au fichier .b18
                b18_mods = generate_b18_modifications(type_batiment[0], region[0], periode[0])
                modify_b18_file(type_batiment[4], b18_file, b18_mods)
            
                #
                # process_b18_with_trnbuild(b18_file)
                
                # Traiter le fichier .b18 avec TRNBuild
                if process_b18_with_trnbuild(b18_file):
                    # Générer et appliquer les modifications au fichier .dck
                    dck_mods = generate_dck_modifications(region[0])
                    dck_mods['B18_FILE'] = os.path.splitext(b18_file)[0]
                    modify_dck_file(type_batiment[5], dck_file, dck_mods)
                    
                    dck_files_to_simulate.append(dck_file)
                else:
                    print(f"Skipping DCK file generation for {b18_file} due to TRNBuild processing error")
    
    # Lancer les simulations
    for dck_file in dck_files_to_simulate:
        run_trnsys_simulation(dck_file)

if __name__ == "__main__":
    main()