#include "Arduino_RouterBridge.h"

const int servoPin = 9;

void setup() {
  pinMode(servoPin, OUTPUT);
}

void loop() {
  moveServo(0);      // 0 degrees
  delay(1000);

  moveServo(90);     // 90 degrees
  delay(1000);

  moveServo(180);    // 180 degrees
  delay(1000);
}

void moveServo(int angle) {

  // Convert angle (0-180) to pulse width (1000-2000 µs)
  int pulseWidth = map(angle, 0, 180, 1000, 2000);

  // Send pulses for about 1 second (50 pulses)
  for (int i = 0; i < 50; i++) {
    digitalWrite(servoPin, HIGH);
    delayMicroseconds(pulseWidth);

    digitalWrite(servoPin, LOW);
    delayMicroseconds(20000 - pulseWidth);
  }
}