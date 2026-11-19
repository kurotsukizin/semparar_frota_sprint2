from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "entrada"
PROCESSADOS = RAIZ / "data" / "processados"
EVIDENCIAS = RAIZ / "evidencias"
EVIDENCIAS.mkdir(parents=True, exist_ok=True)


def main():
    custos = pd.read_csv(ENTRADA / "custos_frota.csv")
    base = pd.read_csv(PROCESSADOS / "base_integrada.csv")

    problemas = []

    nulos = custos.isna().sum()
    for coluna, quantidade in nulos.items():
        if quantidade > 0:
            problemas.append(f"Valores nulos na coluna {coluna}: {quantidade}")

    duplicados = custos.duplicated(subset=["id_veiculo", "periodo"]).sum()
    if duplicados > 0:
        problemas.append(f"Registros duplicados de veiculo/periodo: {duplicados}")

    colunas_monetarias = [
        "custo_combustivel", "custo_manutencao",
        "custo_pedagio", "custo_multas", "custo_impostos"
    ]

    for coluna in colunas_monetarias:
        negativos = (custos[coluna] < 0).sum()
        if negativos > 0:
            problemas.append(f"Valores negativos na coluna {coluna}: {negativos}")

    sem_cadastro = base[base["_merge"] == "left_only"]
    if len(sem_cadastro) > 0:
        veiculos = ", ".join(sem_cadastro["id_veiculo"].unique())
        problemas.append(f"Veiculos sem cadastro: {veiculos}")

    km_invalido = (custos["quilometragem"] <= 0).sum()
    if km_invalido > 0:
        problemas.append(f"Quilometragem invalida: {km_invalido}")

    litros_invalido = (custos["litros_combustivel"] <= 0).sum()
    if litros_invalido > 0:
        problemas.append(f"Litros invalidos: {litros_invalido}")

    relatorio = "RELATORIO DE QUALIDADE DOS DADOS\n\n"

    if problemas:
        relatorio += "Inconsistencias identificadas:\n"
        for problema in problemas:
            relatorio += f"- {problema}\n"
    else:
        relatorio += "Nenhuma inconsistencia identificada.\n"

    relatorio += "\nTratamento aplicado:\n"
    relatorio += "- Registros com veiculo inexistente foram sinalizados e excluidos do calculo de benchmark.\n"
    relatorio += "- Valores negativos de custo foram sinalizados como inconsistentes.\n"
    relatorio += "- O arquivo original foi preservado em data/entrada/.\n"

    (EVIDENCIAS / "relatorio_qualidade.txt").write_text(relatorio, encoding="utf-8")
    print(relatorio)


if __name__ == "__main__":
    main()
