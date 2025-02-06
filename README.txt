1. Ladda ner korrekt corpus och lägg det i foldern 'data' och döp txt filen till 'coprus_file'. Vi använder ___ som finns tillgänglig på URL: 
2. Se till att alla python filer är i samma directory och kompilerade.
3. Kör 'main.py'.

Filer:
ModelBuilder.py
    Innehåller klassen ModelBuilder som skapar filen 'language_model.txt', som innehåller unigram counts och bigram sannolikheter

Suggestor.py
    Innehåller klassen Suggestor som läser modellen och använder sannolikheter för att föreslår ord. Går att använda i text format eller i GUI.

Interface.py
    Innehåller klass WordSuggestor som tar Suggestor som argument och skapar ett GUI som implementerar ordprediktorn på ett fönster.