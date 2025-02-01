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
    print("Invio del messaggio su Telegram...")
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
    print("Recupero dell'ultima circolare dal sito...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trova il primo elemento della circolare più recente
    latest_circular_element = soup.find('div', class_='wpdm-link-tpl')
    if latest_circular_element is None:
        print("Impossibile trovare l'elemento della circolare più recente.")
        return None, None

    circular_title = latest_circular_element.find('strong', class_='ptitle').text.strip()
    circular_link = latest_circular_element.find('a')['href']
    
    print(f"Ultima circolare trovata: {circular_title}")
    return circular_title, circular_link

# Funzione per gestire la creazione e l'aggiornamento del file ultima.txt
def manage_circular_file(circular_title):
    file_path = 'Prove-varie/ultima.txt'  # Path corretto per il file nel repository
    print(f"Directory corrente: {os.getcwd()}")  # Stampa la directory corrente per debug
    print(f"Percorso del file: {file_path}")  # Stampa il percorso del file per debug

    try:
        # Controlla se il file esiste
        if not os.path.exists(file_path):
            # Se il file non esiste, crealo e scrivi circular_title
            with open(file_path, 'w') as file:
                file.write(circular_title)
            print(f"File creato. Titolo circolare salvato: {circular_title}")
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
                print(f"Il titolo è cambiato. File aggiornato con: {circular_title}")
                return True
    except Exception as e:
        print(f"Errore durante la gestione del file: {e}")
        return False

# Funzione per eseguire il commit e il push delle modifiche al repository
def commit_and_push_changes():
    try:
        print("Configurazione dell'identità Git...")
        # Configura l'identità dell'utente Git (necessario per GitHub Actions)
        subprocess.run(['git', 'config', '--global', 'user.email', 'actions@github.com'], check=True)
        subprocess.run(['git', 'config', '--
