import pandas as pd
import numpy as np

def modify_dat_file(input_file, output_file, modifications):
    # Lire le fichier .dat original
    df = pd.read_csv(input_file, sep='\s+', header=0)
    
    # Convertir la colonne 'Time' en float
    df['Time'] = df['Time'].astype(float)
    
    # Appliquer les modifications
    for column, modification in modifications.items():
        if column in df.columns:
            if isinstance(modification, (int, float)):
                # Modification par un facteur multiplicatif
                df[column] *= modification
            elif isinstance(modification, dict):
                # Modification par plage horaire
                for time_range, value in modification.items():
                    start, end = map(float, time_range.split('-'))
                    mask = (df['Time'] >= start) & (df['Time'] < end)
                    df.loc[mask, column] = value
            elif callable(modification):
                # Modification par fonction personnalisée
                df[column] = df.apply(lambda row: modification(row['Time'], row[column]), axis=1)
    
    # Sauvegarder le fichier modifié
    df.to_csv(output_file, sep=' ', index=False, float_format='%.12f')

def create_custom_dat_file(output_file, duration=8760.0, step=0.25):
    # Créer un DataFrame avec la colonne Time
    times = np.arange(0, duration + step, step)
    df = pd.DataFrame({'Time': times})
    
    # Ajouter les colonnes pour chaque type de gain
    columns = ['Stove', 'Dishwasher', 'Fridge', 'Clothwasher', 'Dryer', 
               'LightRecp1st', 'LightRecp2nd', 'Occup1st', 'Occup2nd', 'isDst', 'Time(Dst)']
    
    for col in columns:
        df[col] = 0  # Initialiser toutes les valeurs à 0
    
    # Définir des profils personnalisés
    df['Fridge'] = 47.016  # Consommation constante du réfrigérateur
    df['Time(Dst)'] = df['Time']  # Copier la colonne Time dans Time(Dst)
    
    # Définir des profils d'occupation
    df.loc[(df['Time'] % 24 >= 22) | (df['Time'] % 24 < 6), 'Occup2nd'] = 4  # Nuit
    df.loc[(df['Time'] % 24 >= 17) & (df['Time'] % 24 < 22), 'Occup1st'] = 4  # Soirée
    
    # Définir des profils d'éclairage
    df.loc[(df['Time'] % 24 >= 6) & (df['Time'] % 24 < 8), 'LightRecp1st'] = 200  # Matin
    df.loc[(df['Time'] % 24 >= 18) & (df['Time'] % 24 < 23), 'LightRecp1st'] = 300  # Soir
    
    # Sauvegarder le fichier
    df.to_csv(output_file, sep=' ', index=False, float_format='%.12f')

# Exemple d'utilisation
modifications = {
    'Stove': {
        '7-9': 1000,  # Utilisation du four le matin
        '18-20': 1500  # Utilisation du four le soir
    },
    'LightRecp1st': 1.2,  # Augmentation de 20% de l'éclairage
    'Occup1st': lambda t, v: 4 if 8 <= t % 24 < 18 else v  # 4 personnes pendant la journée
}

modify_dat_file('CCHT-GainSchedule-15min_1.dat', 'Modified-GainSchedule_1.dat', modifications)

# Création d'un fichier .dat personnalisé
create_custom_dat_file('Custom-GainSchedule.dat')