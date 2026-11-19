#define PINO_LED 26

unsigned long ultimoCiclo = 0;
int contador = 0;

void setup() {
  Serial.begin(115200);
  pinMode(PINO_LED, OUTPUT);
  Serial.println("id_veiculo,temp_motor_c,rotacao_rpm,velocidade_km_h,combustivel_pct,anomalia");
}

void loop() {
  unsigned long agora = millis();

  if (agora - ultimoCiclo < 2000) {
    return;
  }

  ultimoCiclo = agora;
  contador++;

  float temperatura = random(75, 113);
  int rotacao = random(700, 2700);
  float velocidade = random(20, 96);
  float combustivel = random(5, 99);

  bool anomalia = temperatura > 105 || rotacao > 2500 || combustivel < 10;

  digitalWrite(PINO_LED, anomalia ? HIGH : LOW);

  Serial.printf("V001,%.1f,%d,%.1f,%.1f,%d\n",
                temperatura, rotacao, velocidade, combustivel, anomalia ? 1 : 0);
}
