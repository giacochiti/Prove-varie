import os
import requests
from bs4 import BeautifulSoup

# Configurazione Telegram
chat_id = '1885923992'  # Il tuo ID
token = '7305004967:AAGe1tySkfUANi9yp0Jh2uBNAJeWwHUG2SI'  # Il token el bot

# URL della pagina delle circolari
url = 'https://liceoartisticopistoia.edu.it/circolari/'

# Percorso del file per salvare l'ultimo titolo
file_path = os.path.join(os.getcwd(), 'last_circular.txt')

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
    circular_title = latest_circular_element.find('strong', class_='ptitle').text.strip()
    circular_link = latest_circular_element.find('a')['href']
    
    return circular_title, circular_link

# Funzione per leggere il titolo dell'ultima circolare dal file
def get_last_saved_circular():
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Funzione per salvare il titolo della circolare nel file
def save_last_circular(title):
    try:
        with open(file_path, 'w') as file:
            file.write(title)
            file.flush()
            os.fsync(file.fileno())
        print(f"Contenuto del file scritto: {title}")
    except Exception as e:
        print(f"Errore durante l'aggiornamento del file: {e}")

# Main
if __name__ == "__main__":
    # Ottieni l'ultima circolare dal sito
    circular_title, circular_link = get_latest_circular()
    
    # Ottieni l'ultimo titolo salvato
    last_saved_title = get_last_saved_circular()
    
    # Confronta i titoli
    if last_saved_title != circular_title:
        # Invia il messaggio su Telegram
        message = f"Nuova circolare pubblicata:\nTitolo: {circular_title}\nLink: {circular_link}"
        send_telegram_message(message)
        
        # Salva il nuovo titolo nel file
        save_last_circular(circular_title)
        print("Nuova circolare trovata e file aggiornato.")
    else:
        print("Non ci sono nuove circolari.")
