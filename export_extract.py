import json
from datetime import datetime

# Structure du modèle attendu
expected_keys = ["id", "name", "timestamp", "collection_id", "folder_id",
                 "environment_id", "totalPass", "delay", "persist", "status",
                 "startedAt", "totalFail", "results", "count", "totalTime", "collection"]

# Fonction pour vérifier l'intégrité du fichier JSON
def check_json_integrity(json_data):
    try:
        # Charger le fichier JSON
        data = json.loads(json_data)

        # Vérifier si toutes les clés attendues sont présentes
        if all(key in data for key in expected_keys):
            print("\n")
            print("Intégrité du fichier JSON vérifiée.")
            return True, data
        else:
            print("Erreur : Le fichier JSON ne correspond pas à la structure attendue.")
            return False, None
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
        return False, None

# Fonction pour afficher les informations de la run
def display_run_info(run_data):
    run_name = run_data.get('name', 'N/A')
    started_at = run_data.get('startedAt', 'N/A')

    # Convertir la date et l'heure en un format lisible
    try:
        started_at_datetime = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        started_at_readable = started_at_datetime.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        started_at_readable = 'Format de date invalide'

    print("\n")
    print(f"Collection ou dossier : {run_name}")
    print(f"Date de l'export : {started_at_readable}")
    print("\n")

# Fonction pour charger la configuration à partir d'un fichier JSON
def load_config_from_file(config_file_path='config.json'):
    try:
        with open(config_file_path) as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print(f"Erreur : Le fichier de configuration {config_file_path} n'a pas été trouvé.")
        return None
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
        return None

# Charger la configuration depuis le fichier config.json
config_data = load_config_from_file()

# Si la configuration n'est pas chargée, interrompre le programme
if not config_data:
    print("Le programme s'arrête en raison d'une erreur de configuration.")
    exit()

# Chemin du fichier d'entrée et des fichiers de sortie à partir de la configuration
input_file_path = config_data.get('input_file_path', 'DEFAULT_CHEMIN_ENTREE.json')
names_with_tests_output_file_path = config_data.get('names_with_tests_output_file_path', 'NAMES_WITH_TESTS_SORTIE.json')
names_without_tests_output_file_path = config_data.get('names_without_tests_output_file_path', 'NAMES_WITHOUT_TESTS_SORTIE.json')

# Charger le fichier JSON d'entrée
with open(input_file_path) as json_file:
    json_data = json_file.read()

# Vérifier l'intégrité du fichier JSON
success, data = check_json_integrity(json_data)

# Si l'intégrité n'est pas vérifiée, interrompre le programme
if not success:
    print("Le programme s'arrête en raison d'une intégrité JSON invalide.")
    exit()

# Afficher les informations de la run
display_run_info(data)

# Extraire les noms avec tests et les noms sans tests
names_with_tests = []
names_without_tests = []
results = data.get('results', [])
if isinstance(results, list):
    for item in results:
        name = item.get('name')
        if name:
            if item.get('tests'):
                names_with_tests.append(name)
            else:
                names_without_tests.append(name)

# Générer un fichier JSON avec les noms avec tests
with open(names_with_tests_output_file_path, 'w') as names_with_tests_output_file:
    json.dump(names_with_tests, names_with_tests_output_file, indent=2)

print(f'Le fichier "{names_with_tests_output_file_path}" a été généré avec succès pour les noms avec tests.')

# Générer un fichier JSON avec les noms sans tests
with open(names_without_tests_output_file_path, 'w') as names_without_tests_output_file:
    json.dump(names_without_tests, names_without_tests_output_file, indent=2)


print(f'Le fichier "{names_without_tests_output_file_path}" a été généré avec succès pour les noms sans tests.')

print("\n")
total_names = len(names_with_tests) + len(names_without_tests)
print(f"Nombre total de rêquetes : {total_names}")
print(f"Nombre de rêquetes avec test : {len(names_with_tests)}")
print(f"Nombre de rêquetes sans test : {len(names_without_tests)}")
