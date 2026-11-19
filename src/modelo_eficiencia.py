from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

RAIZ = Path(__file__).resolve().parents[1]
DIAGNOSTICO = RAIZ / "data" / "processados" / "diagnostico_regras.csv"
RESULTADO = RAIZ / "evidencias" / "resultado_modelo.txt"


def main():
    df = pd.read_csv(DIAGNOSTICO)

    atributos = [
        "custo_por_km",
        "consumo_km_l",
        "quilometragem_total",
        "custo_total",
        "custo_combustivel",
        "custo_manutencao",
        "custo_pedagio",
        "custo_multas",
        "custo_impostos"
    ]

    X = df[atributos]
    y = df["diagnostico_regras"]

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    modelo = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    modelo.fit(X_treino, y_treino)
    previsoes = modelo.predict(X_teste)

    comparacao = pd.DataFrame({
        "id_veiculo": df.loc[X_teste.index, "id_veiculo"],
        "diagnostico_regras": y_teste,
        "previsao_modelo": previsoes
    })

    comparacao["coincide"] = (
        comparacao["diagnostico_regras"] == comparacao["previsao_modelo"]
    )

    relatorio = f"""MODELO INTRODUTORIO DE EFICIENCIA

Algoritmo: RandomForestClassifier
Atributos: {', '.join(atributos)}
Rotulo: diagnostico_regras
Divisao: 70% treino e 30% teste, estratificada

Acuracia: {accuracy_score(y_teste, previsoes):.4f}

Relatorio de classificacao:
{classification_report(y_teste, previsoes)}

Matriz de confusao:
{confusion_matrix(y_teste, previsoes)}

Comparacao entre regras e modelo:
{comparacao.to_string(index=False)}

Interpretacao:
O modelo aprende a partir dos rotulos criados pelas regras de negocio.
Coincidencias indicam que o modelo reproduz a mesma logica de classificacao.
Divergencias devem ser analisadas, pois podem ocorrer pela baixa quantidade de dados.
"""

    RESULTADO.write_text(relatorio, encoding="utf-8")
    print(relatorio)


if __name__ == "__main__":
    main()
