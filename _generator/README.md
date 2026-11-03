# Generatorul site-ului

Paginile HTML din rădăcină sunt generate. Pentru modificări se editează fișierele din acest folder, apoi se rulează din rădăcina repository-ului:

    python3 _generator/build.py .

- `build.py`: datele firmei (nume, telefon, domeniu), produse, orașe, galerie și paginile
- `materiale_date.py`: paginile de materiale
- `sub_date.py`: paginile de variante (bucătării pe colț, dulapuri încastrate etc.) și textele cardurilor
- `style.css`: aspectul site-ului; se copiază în rădăcină la generare
- `lucrari/`: pozele lucrărilor (fără date GPS), copiate în rădăcină la generare

Când există domeniul, se completează `domeniu` în `build.py` și se regenerează: apar automat linkurile canonice și `sitemap.xml`.
