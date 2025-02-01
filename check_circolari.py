import os
import requests
from bs4 import BeautifulSoup

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
    # Usa un percorso assoluto ma corretto per essere sicuri che il file venga creato nel posto giusto
    file_path = os.path.join(os.getcwd(), 'Prove-varie', 'ultima.txt')
    
    print(f"Directory corrente: {os.getcwd()}")
    print(f"Percorso del file: {file_path}")
    
    try:
        # Se la cartella non esiste, creala
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        # Verifica se il file esiste
        if os.path.exists(file_path):
            print(f"Il file {file_path} esiste già.")
            with open(file_path, 'r') as file:
                saved_title = file.read().strip()
            
            # Confronta il titolo salvato con circular_title
            if saved_title == circular_title:
                print("Il titolo è uguale all'ultimo salvato. Programma terminato.")
                return False
            else:
                # Se sono diversi, aggiorna il file con il nuovo titolo
                with open(file_path, 'w') as file:
                    file.write(circular_title)
                print(f"Il titolo è cambiato. File aggiornato con: {circular_title}")
                return True
        else:
            print(f"Il file {file_path} non esiste.")
            # Se il file non esiste, crealo e scrivi circular_title
            with open(file_path, 'w') as file:
                file.write(circular_title)
            print(f"File creato. Titolo circolare salvato: {circular_title}")
            return True
    except Exception as e:
        print(f"Errore durante la gestione del file: {e}")
        return False

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
        else:
            print("Nessun nuovo messaggio inviato.")

