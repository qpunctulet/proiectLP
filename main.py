import PIL
from PIL import Image
import os
import shutil

# Directorul sursă si destinație
folder_sursa = "poze"
folder_destinatie = "expedtie"


def date_si_rezolutie(cale_fisier):
    # Obtinem proprietatiile imagini(date si rezolutie)
    try:
        imagine = PIL.Image.open(cale_fisier, "r")
        # Extragem data
        date = imagine.getexif()
        # Extragem rezolutia
        wid, hgt = imagine.size
        rezolutie = str(wid) + "x" + str(hgt)
        imagine.close()
        return date, rezolutie
    except Exception as e:
        print(f"Eroare la procesarea imaginii {cale_fisier}: {e}")
        return None, None


def redenumeste_imagine(cale_veche, nr_imagine, date, rezolutie, folder_destinatie1):
    nume = f"{date}_img_{nr_imagine}_{rezolutie}.jpeg"
    cale_noua = os.path.join(folder_destinatie1, nume)
    try:
        shutil.copy2(cale_veche, cale_noua)
        print(f"Fișierul {os.path.basename(cale_veche)} a fost redenumit și mutat cu succes.")
        return True
    except Exception as e:
        print(f"Eroare la mutarea fișierului {os.path.basename(cale_veche)}: {e}")
        return False


def redenumire_imaginii(folder_sursa1, folder_destinatie1):
    # Verificam daca folderul destinatie exista, astfel il cream
    if not os.path.exists(folder_destinatie1):
        os.makedirs(folder_destinatie1)

    # Listam toate fisierele din directorul sursa
    imagini = os.listdir(folder_sursa1)

    # Contor pentru numarul de imagini
    nr_imagine = 1

    # Parcurgem fiecare fisier din directorul sursa
    for imagine in imagini:
        # Verificam daca fisierul este de tip "jpg"
        if imagine.lower().endswith(".jpg") or imagine.lower().endswith(".jpeg"):
            # Obtinem calea completa catre fisierul curent
            cale_fisier = os.path.join(folder_sursa, imagine)

            # Obtinem data si rezolutia imaginii
            date, rezolutie = date_si_rezolutie(cale_fisier)
            # Redenumim si mutam fisierul daca am extras datele si rezolutia
            if date or rezolutie:
                redenumeste_imagine(cale_fisier, nr_imagine, date, rezolutie, folder_destinatie1)
                # Revenim la 1 daca numarul depaseste de 99
                nr_imagine = (nr_imagine % 100) + 1

    print("Procesul de redenumire și mutare a fișierelor a fost finalizat.")


redenumire_imaginii(folder_sursa, folder_destinatie)
