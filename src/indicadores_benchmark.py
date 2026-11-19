from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
PROCESSADOS = RAIZ / "data" / "processados"
BASE = PROCESSADOS / "base_integrada.csv"
INDICADORES = PROCESSADOS / "indicadores_veiculo.csv"
BENCHMARK = PROCESSADOS / "benchmark_grupo.csv"
GAPS = PROCESSADOS / "gaps_eficiencia.csv"


def main():
    df = pd.read_csv(BASE)

    df_valido = df[
        (df["_merge"] == "both")
        & (df["quilometragem"] > 0)
        & (df["litros_combustivel"] > 0)
        & (df["custo_total"] >= 0)
    ].copy()

    df_valido["custo_por_km"] = (
        df_valido["custo_total"] / df_valido["quilometragem"]
    ).round(4)

    df_valido["consumo_km_l"] = (
        df_valido["quilometragem"] / df_valido["litros_combustivel"]
    ).round(4)

    indicadores = df_valido.groupby(
        ["id_veiculo", "categoria_operacional"], as_index=False
    ).agg(
        quilometragem_total=("quilometragem", "sum"),
        litros_total=("litros_combustivel", "sum"),
        custo_total=("custo_total", "sum"),
        custo_combustivel=("custo_combustivel", "sum"),
        custo_manutencao=("custo_manutencao", "sum"),
        custo_pedagio=("custo_pedagio", "sum"),
        custo_multas=("custo_multas", "sum"),
        custo_impostos=("custo_impostos", "sum")
    )

    indicadores["custo_por_km"] = (
        indicadores["custo_total"] / indicadores["quilometragem_total"]
    ).round(4)

    indicadores["consumo_km_l"] = (
        indicadores["quilometragem_total"] / indicadores["litros_total"]
    ).round(4)

    benchmark = indicadores.groupby("categoria_operacional", as_index=False).agg(
        custo_por_km_medio=("custo_por_km", "mean"),
        custo_por_km_mediana=("custo_por_km", "median"),
        consumo_medio=("consumo_km_l", "mean"),
        custo_total_medio=("custo_total", "mean")
    ).round(4)

    gaps = indicadores.merge(
        benchmark,
        on="categoria_operacional",
        how="left"
    )

    gaps["gap_absoluto_custo_km"] = (
        gaps["custo_por_km"] - gaps["custo_por_km_medio"]
    ).round(4)

    gaps["gap_percentual_custo_km"] = (
        100 * gaps["gap_absoluto_custo_km"] / gaps["custo_por_km_medio"]
    ).round(2)

    gaps["gap_absoluto_consumo"] = (
        gaps["consumo_km_l"] - gaps["consumo_medio"]
    ).round(4)

    gaps = gaps.sort_values("gap_percentual_custo_km", ascending=False)

    indicadores.to_csv(INDICADORES, index=False)
    benchmark.to_csv(BENCHMARK, index=False)
    gaps.to_csv(GAPS, index=False)

    print("Indicadores por veiculo:")
    print(indicadores)

    print("\nBenchmark por grupo:")
    print(benchmark)

    print("\nRanking de gaps de custo por km:")
    print(gaps[["id_veiculo", "categoria_operacional", "custo_por_km", "custo_por_km_medio", "gap_percentual_custo_km"]])


if __name__ == "__main__":
    main()
