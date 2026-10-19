# Analisi di vendite in una catena di negozi — Epicode

Progetto dimostrativo realizzato con **Python**, **Pandas**, **NumPy** e **Matplotlib**.
I dati sono **sintetici**: 70 transazioni distribuite su 14 giorni, 4 negozi e 7 prodotti. Non rappresentano incassi reali.

## Come eseguirlo

Apri il terminale nella cartella del progetto e digita:

```bash
python -m pip install -r requirements.txt
python analisi_vendite.py
```

Su alcuni PC Windows occorre usare `py` al posto di `python`.

Il programma legge `vendite.csv`, stampa risultati delle analisi e crea:
- `vendite_analizzate.csv` con le colonne **Incasso** e **Categoria**;
- quattro grafici PNG nella cartella `grafici/`.

## Cosa viene analizzato

1. Importazione e ispezione (`head`, `shape`, `info`).
2. Incasso totale della catena, incasso medio per negozio **per transazione**, top 3 per quantità, media per coppia negozio-prodotto.
3. Statistiche NumPy sulla quantità e verifica numerica degli incassi calcolati tramite matrice 2D.
4. Grafici a barre, torta, linee e combinato con due assi.
5. Raggruppamento in categorie, esportazione del file analizzato e funzione `top_n_prodotti(n)`.

## Scelte metodologiche

- **Incasso** = Quantità × Prezzo_unitario; importi in euro.
- La **media per negozio** è la media dell'incasso per riga/transazione, non l'incasso totale del negozio né una media giornaliera.
- La **percentuale sopra la media** conta le righe con Quantità superiore alla media di tutte le righe.
- `np.std` calcola la deviazione standard della popolazione (`ddof=0`).
- Il confronto NumPy–Pandas usa `np.allclose` per tollerare minimi errori floating-point.

## Struttura

```text
progetto_analisi_vendite/
├── analisi_vendite.py
├── vendite.csv
├── vendite_analizzate.csv
├── requirements.txt
├── README.md
└── grafici/
    ├── 01_incasso_per_negozio.png
    ├── 02_quota_incasso_prodotto.png
    ├── 03_andamento_giornaliero.png
    └── 04_confronto_categorie.png
```

Per consegnare su GitHub, carica tutti i file della cartella in un repository e invia il link secondo le indicazioni della piattaforma.
