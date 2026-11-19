from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "entrada"
PROCESSADOS = RAIZ / "data" / "processados"
PROCESSADOS.mkdir(parents=True, exist_ok=True)


def main():
    cadastro = pd.read_csv(ENTRADA / "cadastro_frota.csv")
    custos = pd.read_csv(ENTRADA / "custos_frota.csv")
    telemetria = pd.read_csv(ENTRADA / "telemetria.csv")

    custos["periodo"] = pd.to_datetime(custos["periodo"]).dt.to_period("M").astype(str)
    telemetria["timestamp"] = pd.to_datetime(telemetria["timestamp"])
    telemetria["periodo"] = telemetria["timestamp"].dt.to_period("M").astype(str)

    colunas_custo = [
        "custo_combustivel", "custo_manutencao",
        "custo_pedagio", "custo_multas", "custo_impostos"
    ]

    custos["custo_total"] = custos[colunas_custo].sum(axis=1)

    base = custos.merge(
        cadastro,
        on="id_veiculo",
        how="left",
        indicator=True
    )

    base.to_csv(PROCESSADOS / "base_integrada.csv", index=False)
    telemetria.to_csv(PROCESSADOS / "telemetria_normalizada.csv", index=False)

    print(f"Base integrada: {len(base)} registros")
    print(f"Telemetria normalizada: {len(telemetria)} registros")
    print(f"Veiculos sem cadastro: {(base['_merge'] == 'left_only').sum()}")


if __name__ == "__main__":
    main()
