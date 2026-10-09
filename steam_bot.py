
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from pathlib import Path

opcje = Options()
opcje.add_experimental_option("detach", True)

print("Uruchamiam prawdziwą przeglądarkę Chrome...")
driver = webdriver.Chrome(options=opcje)

print("Wchodzę na stronę z promocjami Steam...")
driver.get("https://steampowered.com/search/?specials=1")

# Czekamy 3 sekundy na załadowanie strony
time.sleep(3)

# =========================================================================
# NOWA LOGIKA NIESKOŃCZONEGO PRZEWIJANIA (Pętla algorytmiczna)
# =========================================================================
print("Rozpoczynam masowe przewijanie strony do samego końca...")

# Sprawdzamy początkową wysokość strony
ostatnia_wysokosc = driver.execute_script("return document.body.scrollHeight")

licznik_przewinien = 1
while True:
    # Zjeżdżamy na sam dół
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(f"Przewinięcie strony nr {licznik_przewinien}...")
    
    # Czekamy 2.5 sekundy, aż Steam dociągnie kolejną paczkę z serwera
    time.sleep(2.5)
    
    # Obliczamy nową wysokość strony po załadowaniu kolejnych gier
    nowa_wysokosc = driver.execute_script("return document.body.scrollHeight")
    
    # WARUNEK KOŃCA: Jeśli nowa wysokość jest taka sama jak stara, oznacza to, 
    # że dotarliśmy do samego dna i nie ma już więcej gier do załadowania.
    if nowa_wysokosc == ostatnia_wysokosc:
        print("Dotarłem do końca bazy danych Steam! Brak kolejnych ofert.")
        break
        
    ostatnia_wysokosc = nowa_wysokosc
    licznik_przewinien += 1
# =========================================================================

print("\nRozpoczynam analizę i filtrowanie ogromnej listy gier (Zniżki >= 50%)...")

try:
    promocje = driver.find_elements(By.XPATH, "//a[contains(@class, 'search_result_row')]")
    plik_wynikowy = Path("wszystkie_promocje_steam.txt")
    
    with open(plik_wynikowy, "w", encoding="utf-8") as plik:
        plik.write(f"=== WSZYSTKIE NAJLEPSZE PROMOCJE STEAM >= 50% ({time.strftime('%Y-%m-%d')}) ===\n\n")
        
        licznik = 0
        for gra in promocje:
            try:
                tytul = gra.find_element(By.XPATH, ".//span[@class='title']").text
                znizka = gra.find_element(By.XPATH, ".//div[contains(@class, 'discount_pct')]").text
                
                if znizka and tytul:
                    znizka_liczba = int(znizka.replace("-", "").replace("%", ""))
                    
                    if znizka_liczba >= 50:
                        wynik = f"Gra: {tytul} | Zniżka: {znizka}\n"
                        plik.write(wynik)
                        licznik += 1
            except Exception:
                pass
                
    print(f"\nSukces! Bot przejrzał całą platformę i zapisał {licznik} gier w pliku: {plik_wynikowy.absolute()}")

except Exception as e:
    print(f"Wystąpił problem podczas wyciągania danych: {e}")
