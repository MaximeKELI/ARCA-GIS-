/**
 * ARCA-GIS — Firmware ESP32 capteur humidité sol
 * Envoie les lectures à POST /api/iot/ingest/
 */
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "VOTRE_WIFI";
const char* WIFI_PASS = "VOTRE_MOT_DE_PASSE";
const char* API_URL = "http://192.168.1.100:8003/api/iot/ingest/";
const char* DEVICE_ID = "ESP32-SOIL-001";
const int SOIL_PIN = 34;

void setup() {
  Serial.begin(115200);
  pinMode(SOIL_PIN, INPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connecté");
}

void loop() {
  int raw = analogRead(SOIL_PIN);
  float moisture = map(raw, 4095, 0, 0, 100);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<256> doc;
    doc["device_id"] = DEVICE_ID;
    doc["value"] = moisture;
    doc["unit"] = "%";
    doc["sensor_type"] = "soil_moisture";

    String body;
    serializeJson(doc, body);
    int code = http.POST(body);
    Serial.printf("Envoi: %.1f%% — HTTP %d\n", moisture, code);
    http.end();
  }

  delay(300000); // 5 minutes
}
