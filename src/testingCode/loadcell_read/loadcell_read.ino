// Load cell + HX711 -> Arduino Mega, streams "millis,raw" over serial.
// Wiring: DT -> pin 4, SCK -> pin 3, VCC -> 5V, GND -> GND
#include "HX711.h"

const int DT_PIN  = 5;
const int SCK_PIN = 4;

HX711 scale;

void setup() {
  Serial.begin(115200);
  scale.begin(DT_PIN, SCK_PIN);
  while (!scale.is_ready()) { delay(10); }
  scale.tare(10);                 // zero with current load
  Serial.println("time_ms,raw");  // CSV header
}

void loop() {
  if (scale.is_ready()) {
    // get_value() = raw reading minus tare offset (counts).
    // After calibrating, set_scale(factor) and use get_units() for force/mass.
    long v = scale.get_value(1);
    Serial.print(millis());
    Serial.print(',');
    Serial.println(v);
  }
}
