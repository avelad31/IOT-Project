#ifdef ESP8266
#include <ESP8266WiFi.h>
#else // ESP32
#include <WiFi.h>
#endif
#include <ModbusIP_ESP8266.h>

// Configuración WiFi
const char *ssid = "WIN HOUSE";
const char *password = "10302060";

// Configuración Modbus
const int LED_COIL = 0;
const int LED = 13;

ModbusIP mb;

void setup() {
  Serial.begin(115200);
  
  // Configurar conexión WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Dirección IP:");
  Serial.println(WiFi.localIP());

  // Configurar Modbus
  mb.server();
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  mb.addCoil(LED_COIL);
}

void loop() {
  // Actualizar el servidor Modbus
  mb.task();

  // Leer el estado del coil Modbus para el LED
  int LED_state = mb.Coil(LED_COIL);

  // Actualizar el estado del LED
  //Serial.println(LED_state);

  if(LED_state==0){
   //Serial.println("Puerta cerrada");
    digitalWrite(LED, HIGH);
  }
  if(LED_state==1){
   //Serial.println("Abriendo puerta...");
    digitalWrite(LED, LOW); 
    delay(3000); //Se abre la puerta durante 4s
    //Serial.println("Puerta cerrada");
    digitalWrite(LED, HIGH);
    delay(1000);
  }
  delay(10);
}
