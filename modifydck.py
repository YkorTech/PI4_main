import re

def modify_dck_file(input_file, output_file, modifications):
    with open(input_file, 'r') as file:
        content = file.read()

    # Modification des paramètres de simulation
    if 'SIMULATION' in modifications:
        sim_params = modifications['SIMULATION']
        pattern = r'(SIMULATION\s+)(\S+)(\s+)(\S+)(\s+)(\S+)'
        replacement = rf'\g<1>{sim_params["START"]}\g<3>{sim_params["STOP"]}\g<5>{sim_params["STEP"]}'
        content = re.sub(pattern, replacement, content)

    # Modification du fichier météo
    if 'WEATHER_FILE' in modifications:
        pattern = r'(ASSIGN\s+")(.*)(\.epw"\s+\d+)'
        replacement = rf'\g<1>{modifications["WEATHER_FILE"]}\g<3>'
        content = re.sub(pattern, replacement, content)

    # Modification du fichier .b18
    if 'B18_FILE' in modifications:
        pattern = r'(ASSIGN\s+")(.*)(\.b18"\s+\d+)'
        replacement = rf'\g<1>{modifications["B18_FILE"]}\g<3>'
        content = re.sub(pattern, replacement, content)

    # Modification du fichier de gains
    if 'GAINS_FILE' in modifications:
        pattern = r'(ASSIGN\s+")(.*)(\.dat"\s+\d+)'
        replacement = rf'\g<1>{modifications["GAINS_FILE"]}\g<3>'
        content = re.sub(pattern, replacement, content)

    # Modification des connexions entre composants
    if 'CONNECTIONS' in modifications:
        for component, inputs in modifications['CONNECTIONS'].items():
            for input_num, value in inputs.items():
                pattern = rf'({component}.*\n(?:.*\n)*?.*{input_num}-\s*)([^\s]+)(.*)'
                replacement = rf'\g<1>{value}\g<3>'
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    with open(output_file, 'w') as file:
        file.write(content)

# Exemple d'utilisation
modifications = {
    'WEATHER_FILE': 'CAN-QC-McTavish-7024745-CWEC23',
    'B18_FILE': 'Modified-Simple-Step3_3',
    'GAINS_FILE': 'CCHT-GainSchedule-15min',
    
}

modify_dck_file('./outputs/Simple-Step3.dck', './outputs/Modified-Simple-Step3_3.dck', modifications)