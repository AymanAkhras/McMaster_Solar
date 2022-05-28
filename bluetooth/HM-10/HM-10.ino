#define sd
#define test

#include <SoftwareSerial.h>
#ifdef sd
#include <SPI.h>
#include <SD.h>
char filename[] = "buslog.csv";
#endif

SoftwareSerial HM10(2, 3); // RX = 2, TX = 3
unsigned long timer = millis();
const byte dataOutLength = 80;

String dataIn = "";
char dataOut[dataOutLength];

int counter = 0;

void setup() {
  Serial.begin(115200);
  HM10.begin(9600);
  HM10.listen();
  HM10.print("AT"); delay(500); HM10.print("AT"); delay(500);
  while (HM10.available() > 0) {
    dataIn = HM10.readString();
  }
  if (dataIn.equals("OK") || dataIn == "OKOK") {
    Serial.println(F("✓ HM10 9600"));
  } else {
    Serial.println(F("× HM10"));
  }

  #ifdef sd
  while (!SD.begin(10)) { //default SPI bus SS line
    Serial.println(F("× SD"));
    delay(1000);
  }
  Serial.println(F("✓ SD"));

  if (SD.exists(filename)) {
    Serial.println((String)"Overwriting " + (String)filename);
    SD.remove(filename);

    File dataFile = SD.open(filename, FILE_WRITE);
    if (dataFile) {
      dataFile.println("battery,temperature,speed");
      dataFile.close();
    } else {
      Serial.println((String)"× " + (String)filename);
    }
  }
  #endif
}

void loop() {
  float battery = 98.0;
  float speed = random(690) / 10.0;
  float temperature = random(420) / 10.0;
  float data[3] = {battery, speed, temperature};

  while (HM10.available() > 0) {
    dataIn = HM10.readString();
    Serial.println((String) "[BLE @" + millis() + "] " + dataIn);
  }

  #ifdef sd //----------------------------------------
  uint8_t msgLength = 21;
  char msg[msgLength] = {'\0'};
  File dataFile = SD.open(filename, FILE_WRITE);
  if (dataFile) {
    for (int i = 0; i < 3; i++) {
      float d = data[i];
      char floatBuffer[6]; // includes '-' and '.'
      
      dataFile.print(d, 2);
      dtostrf(d, 6, 1, floatBuffer);
      strcat(msg, floatBuffer);
      
      if (i % 3 != 2) {
        dataFile.print(',');
        strcat(msg, " ");
      }
    }
    dataFile.print('\n');
    dataFile.close();
  } else {
    Serial.println((String)"× " + (String)filename);
  }
  
  msg[msgLength - 1] = 0;
  Serial.println((String) '@' + millis() + "> " + msg);
  BLEsend(msg, 21);
  #endif //----------------------------------------

  #ifdef test //----------------------------------------
  while (Serial.available() > 0) {
    int cursorAt = Serial.readBytes(dataOut, dataOutLength);
    dataOut[cursorAt] = 0;
    Serial.println((String) '@' + millis() + "> " + dataOut);
    
    BLEsend(dataOut, dataOutLength);
    delay(500); // delay to prevent next msg sending in same packet
  }

  if (millis() - timer >= 1000) {
    HM10.print(counter++);
    timer = millis();
  }

  dataOut[0] = 0;
  #endif //----------------------------------------
}

void BLEsend(char* msg, int length) {
  for (int i = 0; i < length; i++) {
    char c = msg[i];
    if (c == 0) {
      break;
    } else if (c != 10 && c != 13) {
      if (i % 19 == 0 && i != 0) {
        HM10.write(1);
      }
      HM10.write(c);
    }
  }
}
