# Main.py fa partire tutte le API all'interno della cartella del progetto secondo le rotte prestabilite

# http://0.0.0.0:8000/ --> Jupyter Server per il notebook

 # # Swagger # #
# http://0.0.0.0:8001/docs#/ --> API Agriturismi
# http://0.0.0.0:8002/docs#/ --> API Alberghi
# http://0.0.0.0:8003/docs#/ --> API Campeggi e Villaggi

# Librerie per il multiprocessing delle API
import multiprocessing
import os

# funzione che fa partire il server uvicorn + configurazione delle rotte per le rispettive API
def start_api(api_name, port):
    os.system(f"uvicorn {api_name}:app --host 0.0.0.0 --port {port}")


if __name__ == "__main__":
    # Configurazioni per le API + nome dei moduli e delle porte
    api_configs = [
        {"name": "API.api_agriturismi", "port": 8001},
        {"name": "API.api_alberghi", "port": 8002},
        {"name": "API.api_campeggi", "port": 8003}
    ]

    processes = []

    # Avvia un processo separato per ciascuna API utilizzando multiprocessing
    # Ogni processo avvierà l'API specificata con Uvicorn sulla porta specificata
    for config in api_configs:
        process = multiprocessing.Process(target=start_api, args=(config["name"], config["port"]))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

