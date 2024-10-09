import sqlite3

def create_database():
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()

    # Création des tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TypesBatiments (
        ID INTEGER PRIMARY KEY,
        Nom TEXT,
        Secteur TEXT,
        NombreZones INTEGER,
        FichierGeometrieBase TEXT,
        FichierDCKBase TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Regions (
        ID INTEGER PRIMARY KEY,
        Nom TEXT,
        FichierClimatique TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PeriodesConstruction (
        ID INTEGER PRIMARY KEY,
        NomPeriode TEXT,
        AnneeDebut INTEGER,
        AnneeFin INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Materiaux (
        ID INTEGER PRIMARY KEY,
        Nom TEXT,
        Conductivite REAL,
        Capacite REAL,
        Densite REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Constructions (
        ID INTEGER PRIMARY KEY,
        Nom TEXT,
        TypeBatimentID INTEGER,
        RegionID INTEGER,
        PeriodeConstructionID INTEGER,
        Type TEXT,
        FOREIGN KEY (TypeBatimentID) REFERENCES TypesBatiments(ID),
        FOREIGN KEY (RegionID) REFERENCES Regions(ID),
        FOREIGN KEY (PeriodeConstructionID) REFERENCES PeriodesConstruction(ID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CouchesConstruction (
        ID INTEGER PRIMARY KEY,
        ConstructionID INTEGER,
        MateriauID INTEGER,
        Epaisseur REAL,
        Ordre INTEGER,
        FOREIGN KEY (ConstructionID) REFERENCES Constructions(ID),
        FOREIGN KEY (MateriauID) REFERENCES Materiaux(ID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Fenetres (
        ID INTEGER PRIMARY KEY,
        WinID INTEGER,
        Description TEXT,
        UValue REAL,
        gValue REAL,
        Tsol REAL,
        Rfsol REAL,
        TvisDaylight REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Regimes (
        ID INTEGER PRIMARY KEY,
        Nom TEXT,
        TypeBatimentID INTEGER,
        RegionID INTEGER,
        PeriodeConstructionID INTEGER,
        Type TEXT,
        FichierGains TEXT,
        FOREIGN KEY (TypeBatimentID) REFERENCES TypesBatiments(ID),
        FOREIGN KEY (RegionID) REFERENCES Regions(ID),
        FOREIGN KEY (PeriodeConstructionID) REFERENCES PeriodesConstruction(ID)
    )
    ''')

    conn.commit()
    conn.close()

# Fonctions d'insertion
def insert_type_batiment(nom, secteur, nombre_zones, fichier_geometrie_base, fichier_dck_base):
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO TypesBatiments (Nom, Secteur, NombreZones, FichierGeometrieBase, FichierDCKBase)
    VALUES (?, ?, ?, ?, ?)
    ''', (nom, secteur, nombre_zones, fichier_geometrie_base, fichier_dck_base))
    conn.commit()
    conn.close()

def insert_region(nom, fichier_climatique):
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Regions (Nom, FichierClimatique)
    VALUES (?, ?)
    ''', (nom, fichier_climatique))
    conn.commit()
    conn.close()

def insert_periode_construction(nom_periode, annee_debut, annee_fin):
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO PeriodesConstruction (NomPeriode, AnneeDebut, AnneeFin)
    VALUES (?, ?, ?)
    ''', (nom_periode, annee_debut, annee_fin))
    conn.commit()
    conn.close()

def insert_materiau(nom, conductivite, capacite, densite):
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Materiaux (Nom, Conductivite, Capacite, Densite)
    VALUES (?, ?, ?, ?)
    ''', (nom, conductivite, capacite, densite))
    conn.commit()
    conn.close()

def insert_construction(nom, type_batiment_id, region_id, periode_construction_id, type):
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Constructions (Nom, TypeBatimentID, RegionID, PeriodeConstructionID, Type)
    VALUES (?, ?, ?, ?, ?)
    ''', (nom, type_batiment_id, region_id, periode_construction_id, type))
    conn.commit()
    conn.close()

def insert_couche_construction(construction_id, materiau_id, epaisseur, ordre):
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO CouchesConstruction (ConstructionID, MateriauID, Epaisseur, Ordre)
    VALUES (?, ?, ?, ?)
    ''', (construction_id, materiau_id, epaisseur, ordre))
    conn.commit()
    conn.close()

def insert_fenetre(win_id, description, u_value, g_value, t_sol, rf_sol, tvis_daylight):
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Fenetres (WinID, Description, UValue, gValue, Tsol, Rfsol, TvisDaylight)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (win_id, description, u_value, g_value, t_sol, rf_sol, tvis_daylight))
    conn.commit()
    conn.close()

def insert_regime(nom, type_batiment_id, region_id, periode_construction_id, type, fichier_gains):
    conn = sqlite3.connect('batiments.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Regimes (Nom, TypeBatimentID, RegionID, PeriodeConstructionID, Type, FichierGains)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (nom, type_batiment_id, region_id, periode_construction_id, type, fichier_gains))
    conn.commit()
    conn.close()

# Création de la base de données
create_database()

# Exemple d'utilisation des fonctions d'insertion
insert_type_batiment(
    "Maison individuelle non attenante", 
    "Résidentiel", 
    3, 
    "Simple-Step3.b18",
    "Simple-Step3.dck"
)
insert_region("Montréal", "CAN-QC-McTavish-7024745-CWEC23.epw")
insert_periode_construction("1960-1980", 1960, 1980)
insert_materiau("Brique", 0.72, 840, 1920)
insert_construction("Mur extérieur standard", 1, 1, 1, "Mur")
insert_couche_construction(1, 1, 0.1, 1)
insert_fenetre(6502, "ENE6510 Double Clear Air", 2.9, 0.699, 0.765, 0.138, 0.82)
insert_regime("Occupation standard", 1, 1, 1, "Occupation", "CCHT-GainSchedule-15min.dat")

print("Base de données créée et exemples de données insérées avec succès.")