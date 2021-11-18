import requests

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

# V souboru air_polution_ukol.csv najdeš data o množství jemných částic změřených v ovzduší v jedné plzeňské
# meteorologické stanici a který jsme již používali v úkolu z druhého týdne.
#
# Pokud máš úkol hotový, můžeš si z něj zkopírovat následující krok:
#
# Načti dataset a převeď sloupec date (datum měření) na typ datetime.
# Dále pokračuj následujícími kroky:
#
# Z dat vyber data za leden roku 2019 a 2020.
# Porovnej průměrné množství jemných částic ve vzduchu v těchto dvou měsících pomocí Mann–Whitney U testu.
# Formuluj hypotézy pro oboustranný test (nulovou i alternativní) a napiš je do komentářů v programu.
# Měl(a) bys dospět k výsledku, že p-hodnota testu je 1.1 %. Rozhodni, zda bys na hladině významnosti 5 % zamítla
# nulovou hypotézu. Své rozhodnutí napiš do programu