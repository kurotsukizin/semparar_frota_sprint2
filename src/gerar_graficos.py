from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RAIZ = Path(__file__).resolve().parents[1]
PROCESSADOS = RAIZ / "data" / "processados"
IMAGENS = RAIZ / "images"
IMAGENS.mkdir(exist_ok=True)


def main():
    indicadores = pd.read_csv(PROCESSADOS / "indicadores_veiculo.csv")
    gaps = pd.read_csv(PROCESSADOS / "gaps_eficiencia.csv")

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=indicadores,
        x="id_veiculo",
        y="custo_por_km",
        hue="categoria_operacional",
        palette="viridis"
    )
    plt.title("Custo por quilometro por veiculo")
    plt.xlabel("Veiculo")
    plt.ylabel("Custo por km (R$)")
    plt.tight_layout()
    plt.savefig(IMAGENS / "01_custo_por_km.png", dpi=150)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=indicadores,
        x="id_veiculo",
        y="consumo_km_l",
        hue="categoria_operacional",
        palette="crest"
    )
    plt.title("Consumo medio por veiculo")
    plt.xlabel("Veiculo")
    plt.ylabel("km/l")
    plt.tight_layout()
    plt.savefig(IMAGENS / "02_consumo_km_l.png", dpi=150)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=gaps,
        x="id_veiculo",
        y="gap_percentual_custo_km",
        hue="categoria_operacional",
        palette="flare"
    )
    plt.axhline(0, color="black", linestyle="--")
    plt.title("Gap percentual de custo por km em relacao ao grupo")
    plt.xlabel("Veiculo")
    plt.ylabel("Gap (%)")
    plt.tight_layout()
    plt.savefig(IMAGENS / "03_gap_eficiencia.png", dpi=150)
    plt.show()

    print("Graficos gerados em images/")


if __name__ == "__main__":
    main()
