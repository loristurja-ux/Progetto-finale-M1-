"""Progetto Epicode - Analisi vendite in una catena di negozi.
Esecuzione: python analisi_vendite.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
GRAFICI = BASE / "grafici"
GRAFICI.mkdir(exist_ok=True)

# PARTE 2 - Importazione
# Il CSV contiene una vendita per riga; Data è convertita in datetime.
df = pd.read_csv(BASE / "vendite.csv", parse_dates=["Data"])
print("\n=== PRIME 5 RIGHE ===")
print(df.head())
print("\n=== DIMENSIONI (righe, colonne) ===")
print(df.shape)
print("\n=== INFO GENERALI ===")
df.info()

# PARTE 3 - Analisi con Pandas
df["Incasso"] = (df["Quantità"] * df["Prezzo_unitario"]).round(2)
incasso_totale = df["Incasso"].sum()
# Media degli incassi delle singole operazioni per ciascun negozio.
incasso_medio_per_negozio = df.groupby("Negozio")["Incasso"].mean().sort_values(ascending=False)
prodotti_piu_venduti = df.groupby("Prodotto")["Quantità"].sum().nlargest(3)
incasso_medio_negozio_prodotto = df.groupby(["Negozio", "Prodotto"])["Incasso"].mean()

print(f"\n=== INCASSO TOTALE CATENA ===\n€ {incasso_totale:,.2f}")
print("\n=== INCASSO MEDIO PER NEGOZIO (per operazione) ===")
print(incasso_medio_per_negozio.round(2))
print("\n=== TOP 3 PRODOTTI PER QUANTITÀ ===")
print(prodotti_piu_venduti)
print("\n=== INCASSO MEDIO PER NEGOZIO E PRODOTTO ===")
print(incasso_medio_negozio_prodotto.round(2))

# PARTE 4 - Elaborazioni NumPy
q = df["Quantità"].to_numpy()
media, minimo, massimo, deviazione = np.mean(q), np.min(q), np.max(q), np.std(q)
percentuale_sopra_media = np.mean(q > media) * 100
print("\n=== STATISTICHE NUMPY: QUANTITÀ ===")
print(f"Media: {media:.2f}; minimo: {minimo}; massimo: {massimo}; deviazione std.: {deviazione:.2f}")
print(f"Percentuale di righe con quantità sopra la media: {percentuale_sopra_media:.2f}%")

matrice = df[["Quantità", "Prezzo_unitario"]].to_numpy()
incassi_numpy = matrice[:, 0] * matrice[:, 1]
# Confronto robusto per numeri in virgola mobile.
assert np.allclose(incassi_numpy, df["Incasso"].to_numpy(), atol=0.005), "Gli incassi non coincidono!"
print("Verifica NumPy vs Pandas: OK (tutti gli incassi coincidono)")

# PARTE 5 - Visualizzazioni Matplotlib
plt.style.use("ggplot")

per_negozio = df.groupby("Negozio")["Incasso"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9, 5))
per_negozio.plot(kind="bar", ax=ax, color="#3758A8")
ax.set(title="Incasso totale per negozio", xlabel="Negozio", ylabel="Incasso (€)")
ax.tick_params(axis="x", rotation=0)
fig.tight_layout()
fig.savefig(GRAFICI / "01_incasso_per_negozio.png", dpi=160)
plt.close(fig)

per_prodotto = df.groupby("Prodotto")["Incasso"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 7))
ax.pie(per_prodotto, labels=per_prodotto.index, autopct="%1.1f%%", startangle=90)
ax.set_title("Quota dell'incasso per prodotto")
fig.tight_layout()
fig.savefig(GRAFICI / "02_quota_incasso_prodotto.png", dpi=160)
plt.close(fig)

per_giorno = df.groupby("Data")["Incasso"].sum().sort_index()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(per_giorno.index, per_giorno.values, marker="o", color="#3758A8")
ax.set(title="Andamento giornaliero degli incassi", xlabel="Data", ylabel="Incasso (€)")
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(GRAFICI / "03_andamento_giornaliero.png", dpi=160)
plt.close(fig)

# PARTE 6 - Categorie
categorie = {
    "Smartphone": "Informatica", "Laptop": "Informatica", "Tablet": "Informatica",
    "TV": "Elettrodomestici", "Frigorifero": "Elettrodomestici",
    "Cuffie": "Audio", "Speaker": "Audio",
}
df["Categoria"] = df["Prodotto"].map(categorie).fillna("Altro")
riepilogo_categorie = df.groupby("Categoria").agg(
    Incasso_totale=("Incasso", "sum"),
    Quantità_media=("Quantità", "mean"),
)
print("\n=== RIEPILOGO CATEGORIE ===")
print(riepilogo_categorie.round(2))
df.to_csv(BASE / "vendite_analizzate.csv", index=False, date_format="%Y-%m-%d", float_format="%.2f")
print("\nCSV analizzato salvato: vendite_analizzate.csv")

# PARTE 7 - Estensioni
# Incasso medio = media dell'incasso per operazione in ciascuna categoria.
confronto = df.groupby("Categoria").agg(Incasso_medio=("Incasso", "mean"), Quantità_media=("Quantità", "mean"))
fig, ax1 = plt.subplots(figsize=(9, 5))
confronto["Incasso_medio"].plot(kind="bar", ax=ax1, color="#3758A8", width=0.6)
ax1.set(xlabel="Categoria", ylabel="Incasso medio per operazione (€)", title="Incasso medio e quantità media per categoria")
ax1.tick_params(axis="x", rotation=0)
ax2 = ax1.twinx()
ax2.plot(range(len(confronto)), confronto["Quantità_media"], color="#E67A27", marker="o", linewidth=2)
ax2.set_ylabel("Quantità media (unità)")
fig.tight_layout()
fig.savefig(GRAFICI / "04_confronto_categorie.png", dpi=160)
plt.close(fig)

def top_n_prodotti(n: int) -> pd.Series:
    """Restituisce gli n prodotti con maggior incasso totale (serie ordinata)."""
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("n deve essere un intero positivo")
    return df.groupby("Prodotto")["Incasso"].sum().nlargest(n)

print("\n=== TOP 3 PRODOTTI PER INCASSO (funzione) ===")
print(top_n_prodotti(3).round(2))
print(f"\nGrafici creati nella cartella: {GRAFICI}")
