import os
import requests
from bs4 import BeautifulSoup
import subprocess

# Configurazione Telegram
chat_id = '1885923992'  # Il tuo ID
token = '7305004967:AAGe1tySkfUANi9yp0Jh2uBNAJeWwHUG2SI'  # Il token del bot

# URL della pagina delle circolari
url = 'https://liceoartisticopistoia.edu.it/circolari/'

# Funzione per inviare un messaggio su Telegram tramite l'API
def send_telegram_message(message):
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(api_url, data=payload)
    if response.status_code == 200:
        print("Messaggio inviato con successo!")
    else:
        print(f"Errore nell'invio del messaggio: {response.status_code}")

# Funzione per ottenere l'ultima circolare
def get_latest_circular():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trova il primo elemento della circolare più recente
    latest_circular_element = soup.find('div', class_='wpdm-link-tpl')
    if latest_circular_element is None:
        print("Impossibile trovare l'elemento della circolare più recente.")
        return None, None

    circular_title = latest_circular_element.find('strong', class_='ptitle').text.strip()
    circular_link = latest_circular_element.find('a')['href']
    
    return circular_title, circular_link

# Funzione per gestire la creazione e l'aggiornamento del file ultima.txt
def manage_circular_file(circular_title):
    file_path = 'Prove-varie'  # Assicurati che il percorso sia relativo al tuo repository
    
    try:
        # Controlla se il file esiste
        if not os.path.exists(file_path):
            # Se il file non esiste, crealo e scrivi circular_title
            with open(file_path, 'w') as file:
                file.write(circular_title)
            print(f"File creato in: {os.path.abspath(file_path)}")
            print(f"Titolo circolare salvato: {circular_title}")
        else:
            # Se il file esiste, leggi il contenuto
            with open(file_path, 'r') as file:
                saved_title = file.read().strip()
            
            # Confronta il titolo salvato con circular_title
            if saved_title == circular_title:
                # Se sono uguali, interrompe l'esecuzione
                print("Il titolo è uguale all'ultimo salvato. Programma terminato.")
                return False
            else:
                # Se sono diversi, aggiorna il file con il nuovo titolo
                with open(file_path, 'w') as file:
                    file.write(circular_title)
                print(f"Il titolo è cambiato. File aggiornato in: {os.path.abspath(file_path)}")
                print(f"File aggiornato con: {circular_title}")
                return True
    except Exception as e:
        print(f"Errore durante la gestione del file: {e}")
        return False

# Funzione per fare il commit e il push del file nel repository GitHub
def commit_and_push_changes():
    try:
        # Esegui il commit e il push delle modifiche al repository
        subprocess.run(['git', 'add', 'Prove-varie/ultima.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Aggiornato ultima.txt con il titolo della nuova circolare'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("Modifiche commesse e pushate correttamente su GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il commit o il push: {e}")

# Main
if __name__ == "__main__":
    # Ottieni l'ultima circolare dal sito
    circular_title, circular_link = get_latest_circular()
    
    if circular_title is None or circular_link is None:
        print("Errore nel recuperare l'ultima circolare.")
    else:
        # Confronta le circolari
        if manage_circular_file(circular_title):
            # Crea il messaggio da inviare
            message = f"Ultima circolare pubblicata:\nTitolo: {circular_title}\nLink: {circular_link}"
            
            # Invia il messaggio su Telegram
            send_telegram_message(message)
            
            # Fai il commit e il push del file nel repository GitHub
            commit_and_push_changes()
        else:
            print("Nessun nuovo messaggio inviato.")
