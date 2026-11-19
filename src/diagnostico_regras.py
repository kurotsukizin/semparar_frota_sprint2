from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
GAPS = RAIZ / "data" / "processados" / "gaps_eficiencia.csv"
DIAGNOSTICO = RAIZ / "data" / "processados" / "diagnostico_regras.csv"


def classificar(gap_percentual):
    if gap_percentual <= 10:
        return "eficiente"

    if gap_percentual <= 25:
        return "atencao"

    return "ineficiente"


def main():
    df = pd.read_csv(GAPS)
    df["diagnostico_regras"] = df["gap_percentual_custo_km"].apply(classificar)
    df.to_csv(DIAGNOSTICO, index=False)

    print(df[[
        "id_veiculo",
        "categoria_operacional",
        "custo_por_km",
        "custo_por_km_medio",
        "gap_percentual_custo_km",
        "diagnostico_regras"
    ]])


if __name__ == "__main__":
    main()
