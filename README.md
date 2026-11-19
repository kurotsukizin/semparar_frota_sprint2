# Calculadora de Redução de Custos de Frota — Sem Parar

## Sprint 2 — Inteligência e Diagnóstico

Projeto desenvolvido para consolidar custos, cadastro de frota e telemetria simulada, calcular indicadores de eficiência, construir benchmark por grupos comparáveis e identificar veículos com possíveis ineficiências.

## Integrantes

- Guilherme Cabral Mendes Mariano | 574221

## Problema

Os custos de frota estão dispersos em diferentes fontes e dificultam a identificação de veículos menos eficientes. A solução integra combustível, manutenção, pedágio, multas e impostos com o cadastro dos veículos e telemetria simulada.

## Objetivo da Sprint 2

Responder com evidências às seguintes perguntas do gestor de frota:

1. Quanto a operação realmente custa?
2. Onde a operação está menos eficiente do que deveria?

## Fluxo da solução

```text
Arquivos de entrada (CSV e JSON)
        |
Ingestão e normalização
        |
Verificações de qualidade
        |
Indicadores e benchmark
        |
Gap de eficiência
        |
Diagnóstico por regras
        |
Classificação supervisionada introdutória
```

## Estrutura do projeto

```text
semparar_frota_sprint2/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── entrada/
│   └── processados/
├── docs/
│   └── estrutura_pdf.txt
├── evidencias/
│   ├── relatorio_qualidade.txt
│   └── resultado_modelo.txt
├── images/
├── src/
│   ├── gerar_dados.py
│   ├── ingestao_normalizacao.py
│   ├── verificacao_qualidade.py
│   ├── indicadores_benchmark.py
│   ├── diagnostico_regras.py
│   ├── modelo_eficiencia.py
│   └── gerar_graficos.py
└── wokwi/
    ├── diagram.json
    └── telemetria_frota.ino
```

## Fontes de dados

Todos os dados utilizados são **fictícios e simulados**. Não há uso de dados reais de clientes da Sem Parar Empresas.

Os arquivos de entrada são gerados pelo script `src/gerar_dados.py`:

| Arquivo | Formato | Conteúdo |
|---|---|---|
| `cadastro_frota.csv` | CSV | Identificação, placa, tipo, porte e categoria operacional dos veículos |
| `custos_frota.csv` | CSV | Custos mensais por veículo, quilometragem, litros e categorias de custo |
| `telemetria.csv` | CSV | Leituras simuladas de velocidade, rotação, temperatura e combustível |
| `resumo_fontes.json` | JSON | Resumo das fontes, período e inconsistências propositalmente inseridas |

## Execução

Abra o terminal na pasta raiz do projeto e execute:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Depois, execute os scripts na seguinte ordem:

```bash
python src/gerar_dados.py
python src/ingestao_normalizacao.py
python src/verificacao_qualidade.py
python src/indicadores_benchmark.py
python src/diagnostico_regras.py
python src/modelo_eficiencia.py
python src/gerar_graficos.py
```

## Descrição dos módulos

| Arquivo | Função |
|---|---|
| `gerar_dados.py` | Gera os arquivos fictícios de cadastro, custos e telemetria |
| `ingestao_normalizacao.py` | Lê os arquivos, padroniza períodos, calcula custo total e integra os dados |
| `verificacao_qualidade.py` | Identifica inconsistências e gera o relatório de qualidade |
| `indicadores_benchmark.py` | Calcula indicadores, benchmark por grupo e gaps de eficiência |
| `diagnostico_regras.py` | Classifica os veículos conforme regras de negócio |
| `modelo_eficiencia.py` | Treina e avalia um modelo supervisionado introdutório |
| `gerar_graficos.py` | Gera gráficos de custo, consumo e gaps |

## Verificações de qualidade

O projeto verifica:

- Valores nulos em campos obrigatórios.
- Registros duplicados por veículo e período.
- Valores negativos em custos.
- Quilometragem inválida.
- Litros de combustível inválidos.
- Referências a veículos inexistentes no cadastro.

Foram inseridas propositalmente duas inconsistências nos dados simulados:

- Um custo de manutenção negativo.
- Um veículo com identificador `V999`, presente nos custos, mas ausente no cadastro.

O relatório completo é gerado em:

```text
evidencias/relatorio_qualidade.txt
```

## Benchmark de custos

Os veículos são agrupados pela coluna `categoria_operacional`:

- `leve_urbano`
- `misto`
- `pesado_rodoviario`

Para cada grupo, são calculados:

- Média de custo por quilômetro.
- Mediana de custo por quilômetro.
- Consumo médio em km/l.
- Custo total médio.

O benchmark garante que veículos de perfis diferentes não sejam comparados diretamente entre si.

## Indicadores calculados

- Custo total por veículo.
- Custo por quilômetro.
- Consumo em km/l.
- Participação de combustível, manutenção, pedágio, multas e impostos no custo total.
- Gap absoluto e percentual em relação à média do grupo.
- Ranking dos maiores gaps de eficiência.

## Regras de diagnóstico

A classificação é baseada no gap percentual do custo por quilômetro em relação à média do grupo:

| Diagnóstico | Critério |
|---|---|
| `eficiente` | Custo por km até 10% acima da média do grupo |
| `atencao` | Custo por km entre 10% e 25% acima da média do grupo |
| `ineficiente` | Custo por km mais de 25% acima da média do grupo |

## Modelo de Machine Learning

O modelo utiliza o algoritmo `RandomForestClassifier`, da biblioteca Scikit-learn.

### Atributos utilizados

- Custo por quilômetro.
- Consumo em km/l.
- Quilometragem total.
- Custo total.
- Custo com combustível.
- Custo com manutenção.
- Custo com pedágio.
- Custo com multas.
- Custo com impostos.

### Rótulo

O rótulo utilizado é o diagnóstico criado pelas regras de negócio:

- `eficiente`
- `atencao`
- `ineficiente`

### Divisão dos dados

- 70% dos dados para treino.
- 30% dos dados para teste.
- Divisão estratificada para preservar a proporção das classes.

### Avaliação

O modelo é avaliado com:

- Acurácia.
- Relatório de classificação.
- Matriz de confusão.
- Comparação entre o diagnóstico por regras e a previsão do modelo.

O resultado é salvo em:

```text
evidencias/resultado_modelo.txt
```

## Telemetria e anomalias

O projeto inclui um firmware para ESP32 simulado no Wokwi.

O sistema gera leituras de:

- Temperatura do motor.
- Rotação.
- Velocidade.
- Nível de combustível.

Uma leitura é considerada anomalia quando:

- A temperatura do motor é superior a 105 °C.
- A rotação é superior a 2.500 rpm.
- O nível de combustível é inferior a 10%.

Quando uma anomalia é detectada, o LED acende e o Monitor Serial registra a ocorrência.

## Gráficos

Os gráficos são gerados em:

```text
images/01_custo_por_km.png
images/02_consumo_km_l.png
images/03_gap_eficiencia.png
```

## Resultados esperados

Após a execução, o projeto gera:

```text
data/processados/base_integrada.csv
data/processados/indicadores_veiculo.csv
data/processados/benchmark_grupo.csv
data/processados/gaps_eficiencia.csv
data/processados/diagnostico_regras.csv
evidencias/relatorio_qualidade.txt
evidencias/resultado_modelo.txt
images/01_custo_por_km.png
images/02_consumo_km_l.png
images/03_gap_eficiencia.png
```

## Evolução do projeto

Na Sprint 1, o grupo planejou a arquitetura da Calculadora de Redução de Custos de Frota, selecionou User Stories e organizou os dados necessários.

Na Sprint 2, o grupo implementou o fluxo de ingestão, normalização, verificação de qualidade, cálculo de indicadores, benchmark, gap de eficiência, diagnóstico por regras e modelo introdutório de classificação.

Na Sprint 3, o projeto deverá evoluir para estimativas de economia em reais e recomendações de ação para o gestor de frota.

## Limitações

- Todos os dados são fictícios e simulados.
- A telemetria do Wokwi não representa um veículo real.
- O modelo é introdutório e não substitui uma análise especializada.
- A amostra é pequena, o que pode limitar a generalização do modelo.
- A estimativa de economia e o motor de recomendações serão desenvolvidos na Sprint 3.

## Vídeo demonstrativo

Link do vídeo:

```text
https://youtu.be/lDYB36U6kTw
```
