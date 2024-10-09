import os
import subprocess
import time
# import pyautogui

def run_trnsys_simulation(dck_file):
    """
    Fonction pour exécuter une simulation TRNSYS avec un fichier .dck donné
    """
    trnsys_exe = r"C:\TRNSYS18\Exe\TrnEXE64.exe "
    
    if not os.path.exists(trnsys_exe):
        raise FileNotFoundError(f"TRNSYS executable not found at {trnsys_exe}")
    
    if not os.path.exists(dck_file):
        raise FileNotFoundError(f"DCK file not found: {dck_file}")
    
    command = [trnsys_exe, dck_file,"/N", "/h"]
    
    try:
        process = subprocess.Popen(command)
        
        # Attendre que la simulation se termine
        process.wait()
        
        # # Attendre un moment pour s'assurer que la fenêtre est prête
        # time.sleep(2)  # Ajustez ce délai si nécessaire
        
        # # Appuyer sur 'Enter' pour fermer la fenêtre de notification
        # pyautogui.press('enter')
        
        print(f"Simulation completed successfully for {dck_file}")
        
        return True
    
    except Exception as e:
        print(f"An error occurred while running the simulation for {dck_file}: {str(e)}")
        return False

def batch_run_simulations(dck_files):
    """
    Fonction pour exécuter une série de simulations TRNSYS
    """
    results = []
    for dck_file in dck_files:
        print(f"Starting simulation for {dck_file}")
        start_time = time.time()
        print(dck_file)
        success = run_trnsys_simulation(dck_file)
        end_time = time.time()
        
        results.append({
            'file': dck_file,
            'success': success,
            'duration': end_time - start_time
        })
        
    return results

# Exemple d'utilisation
if __name__ == "__main__":
    dck_files = [
        # "./outputs/Modified-Simple-Step3_1.dck",
        # "./outputs/Modified-Simple-Step3_2.dck",
        "C:\PI4_main\outputs\Modified-Simple-Step3_3.dck"
    ]
    
    results = batch_run_simulations(dck_files)
    
    print("\nSimulation Results:")
    for result in results:
        status = "Success" if result['success'] else "Failed"
        print(f"{result['file']}: {status} (Duration: {result['duration']:.2f} seconds)")


        