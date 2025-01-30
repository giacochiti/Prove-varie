import os

def leggi_numero(file_path):
    """Legge il numero dal file, se esiste, altrimenti restituisce 0."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            contenuto = file.read().strip()
            return int(contenuto) if contenuto.isdigit() else 0
    return 0

def aggiorna_numero(file_path):
    numero = leggi_numero(file_path)
    numero += 1    """Legge il numero, lo incrementa di 1 e lo scrive nel file."""

    with open(file_path, 'w') as file:
        file.write(str(numero))

if __name__ == "__main__":
    file_path = "somma.txt"
    aggiorna_numero(file_path)
    print(f"Il numero aggiornato è: {leggi_numero(file_path)}")
