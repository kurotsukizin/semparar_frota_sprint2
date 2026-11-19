import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "entrada"
ENTRADA.mkdir(parents=True, exist_ok=True)

VEICULOS = [
    {"id_veiculo": "V001", "placa": "ABC1D23", "tipo": "caminhao", "porte": "pesado", "categoria_operacional": "pesado_rodoviario"},
    {"id_veiculo": "V002", "placa": "DEF2E34", "tipo": "caminhao", "porte": "pesado", "categoria_operacional": "pesado_rodoviario"},
    {"id_veiculo": "V003", "placa": "GHI3F45", "tipo": "furgao", "porte": "medio", "categoria_operacional": "misto"},
    {"id_veiculo": "V004", "placa": "JKL4G56", "tipo": "furgao", "porte": "medio", "categoria_operacional": "misto"},
    {"id_veiculo": "V005", "placa": "MNO5H67", "tipo": "van", "porte": "leve", "categoria_operacional": "leve_urbano"},
    {"id_veiculo": "V006", "placa": "PQR6I78", "tipo": "van", "porte": "leve", "categoria_operacional": "leve_urbano"},
]


def main():
    random.seed(42)
    inicio = date(2026, 8, 1)

    with (ENTRADA / "cadastro_frota.csv").open("w", encoding="utf-8", newline="") as arquivo:
        campos = ["id_veiculo", "placa", "tipo", "porte", "categoria_operacional"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(VEICULOS)

    custos = []
    for veiculo in VEICULOS:
        for mes in range(3):
            km = random.randint(2500, 9000)
            litros = round(km / random.uniform(2.5, 5.5), 2)
            combustivel = round(litros * random.uniform(5.5, 6.8), 2)
            manutencao = round(random.uniform(300, 3200), 2)
            pedagio = round(random.uniform(50, 900), 2)
            multas = round(random.choice([0, 0, 100, 250, 480]), 2)
            impostos = round(random.uniform(180, 750), 2)

            custos.append({
                "id_veiculo": veiculo["id_veiculo"],
                "periodo": (inicio + timedelta(days=30 * mes)).strftime("%Y-%m"),
                "quilometragem": km,
                "litros_combustivel": litros,
                "custo_combustivel": combustivel,
                "custo_manutencao": manutencao,
                "custo_pedagio": pedagio,
                "custo_multas": multas,
                "custo_impostos": impostos
            })

    custos[7]["custo_manutencao"] = -250.00

    custos.append({
        "id_veiculo": "V999",
        "periodo": "2026-08",
        "quilometragem": 1000,
        "litros_combustivel": 200,
        "custo_combustivel": 1200,
        "custo_manutencao": 300,
        "custo_pedagio": 50,
        "custo_multas": 0,
        "custo_impostos": 200
    })

    with (ENTRADA / "custos_frota.csv").open("w", encoding="utf-8", newline="") as arquivo:
        campos = list(custos[0].keys())
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(custos)

    telemetria = []
    for veiculo in VEICULOS[:3]:
        for i in range(20):
            velocidade = round(random.uniform(20, 95), 1)
            rotacao = round(random.uniform(700, 2600), 0)
            temperatura = round(random.uniform(75, 112), 1)
            combustivel = round(random.uniform(8, 98), 1)

            anomalia = (
                temperatura > 105
                or rotacao > 2500
                or combustivel < 10
            )

            telemetria.append({
                "id_veiculo": veiculo["id_veiculo"],
                "timestamp": f"2026-11-01 {i:02d}:00:00",
                "velocidade_km_h": velocidade,
                "rotacao_rpm": rotacao,
                "temperatura_motor_c": temperatura,
                "nivel_combustivel_pct": combustivel,
                "anomalia": int(anomalia),
                "origem": "wokwi_simulado"
            })

    with (ENTRADA / "telemetria.csv").open("w", encoding="utf-8", newline="") as arquivo:
        campos = list(telemetria[0].keys())
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(telemetria)

    resumo = {
        "fonte": "dados simulados gerados pelo projeto",
        "periodo": "2026-08 a 2026-10",
        "quantidade_veiculos": len(VEICULOS),
        "quantidade_registros_custo": len(custos),
        "quantidade_registros_telemetria": len(telemetria),
        "inconsistencias_propositas": [
            "custo_manutencao negativo no registro 8",
            "id_veiculo V999 inexistente no cadastro"
        ]
    }

    (ENTRADA / "resumo_fontes.json").write_text(
        json.dumps(resumo, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("Arquivos gerados em data/entrada/")


if __name__ == "__main__":
    main()
