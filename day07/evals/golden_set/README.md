# Golden set piano e razionale

## Perche iniziamo con fatture sintetiche

Iniziamo con fatture sintetiche perche non ho fatture reali a disposizione e perche usando i dataset pubblici troveremmo us/uk format che non sono idonei al mercato italiano. Creeremmo cosi un progetto basato su un input/output diverso da quello reale.

## Come evitiamo il bias 'Claude testa se stesso'

Prima devo testare io e capire come voglio l output e cosi posso testare Claude. 
Tre ruoli separati:

- **Claude**: genera il contenuto della fattura (testo realistico: nome vendor, P.IVA, importi, righe)

- **reportlab**: prende quel contenuto e lo trasforma in un file PDF visivo (formattato come una fattura vera)

- **Io**: apro il PDF generato, lo leggo, e scrivo a mano il JSON atteso (la golden label)

## Piano di sostituzione progressiva

- Settimane 1-2: 5 fatture sintetiche italiane
- Settimane 3-4: caccia attiva a 2-3 fatture reali (chiedere a chi ha P.IVA, recuperare fatture freelance o del commercialista)
- Mese 2-3: ogni edge case reale incontrato entra nel golden set
- Target a 3 mesi: 70% del golden set è composto da fatture reali

L'obiettivo è non costruire un sistema che funziona solo su fatture giocattolo.