import os

def leggi_numero(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            contenuto = file.read().strip()
            return int(contenuto) if contenuto.isdigit() else 0
    return 0

def aggiorna_numero(file_path):
    numero = leggi_numero(file_path)
    numero += 1

    with open(file_path, 'w') as file:
        file.write(str(numero))

    print(f"Nuovo valore scritto su {file_path}: {numero}")  # Debug

if __name__ == "__main__":
    file_path = "somma.txt"
    aggiorna_numero(file_path)
    print(f"Il numero aggiornato è: {leggi_numero(file_path)}")
