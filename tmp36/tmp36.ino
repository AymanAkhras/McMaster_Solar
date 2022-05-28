#define READ_TMP A5
#define ADC_RESOLUTION_BITS 10

int sensorIn;
float temperature;

void setup() {
  Serial.begin(115200);
}

void loop() {
  sensorIn = analogRead(READ_TMP);
  temperature = ((float)sensorIn / pow(2, ADC_RESOLUTION_BITS) * 5000 - 500) / 10;

  Serial.print("temperature: ");
  Serial.println(temperature);
  delay(1000);
}
