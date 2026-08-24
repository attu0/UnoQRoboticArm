#include <TinyGPS.h>

// ---- Motor driver (Rhino MDD20A) ----
#define L_PWM 5
#define L_DIR 6
#define L_SLEEP 7
#define R_PWM 9
#define R_DIR 10
#define R_SLEEP 11

// ---- Encoders ----
#define L_ENC_A 2   // interrupt pin
#define L_ENC_B 4
#define R_ENC_A 3   // interrupt pin
#define R_ENC_B 8

volatile long leftCount = 0;
volatile long rightCount = 0;

// ---- GPS ----
TinyGPSPlus gps;
#define GPS_BAUD 9600

// ---- Serial command buffer ----
const int BUFFER_SIZE = 64;
char serialBuffer[BUFFER_SIZE];
int bufferIndex = 0;

void setup() {
  Serial.begin(115200);   // USB to UNO Q
  Serial1.begin(GPS_BAUD); // GPS

  pinMode(L_PWM, OUTPUT);
  pinMode(L_DIR, OUTPUT);
  pinMode(L_SLEEP, OUTPUT);
  pinMode(R_PWM, OUTPUT);
  pinMode(R_DIR, OUTPUT);
  pinMode(R_SLEEP, OUTPUT);

  digitalWrite(L_SLEEP, HIGH);
  digitalWrite(R_SLEEP, HIGH);

  pinMode(L_ENC_A, INPUT_PULLUP);
  pinMode(L_ENC_B, INPUT_PULLUP);
  pinMode(R_ENC_A, INPUT_PULLUP);
  pinMode(R_ENC_B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(L_ENC_A), leftEncoderISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(R_ENC_A), rightEncoderISR, CHANGE);

  stopAll();
}

void loop() {
  // Feed GPS parser continuously
  while (Serial1.available()) {
    gps.encode(Serial1.read());
  }

  // Handle incoming commands from UNO Q
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (bufferIndex > 0) {
        serialBuffer[bufferIndex] = '\0';
        processCommand(serialBuffer);
        bufferIndex = 0;
      }
    } else if (bufferIndex < BUFFER_SIZE - 1) {
      serialBuffer[bufferIndex++] = c;
    } else {
      bufferIndex = 0;
      Serial.println("ERR BUFFER_OVERFLOW");
    }
  }
}

// ============================================================
// ENCODER ISRs
// ============================================================

void leftEncoderISR() {
  if (digitalRead(L_ENC_A) == digitalRead(L_ENC_B)) leftCount++;
  else leftCount--;
}

void rightEncoderISR() {
  if (digitalRead(R_ENC_A) == digitalRead(R_ENC_B)) rightCount++;
  else rightCount--;
}

// ============================================================
// COMMAND PROCESSING
//
// SET_MOTOR L <-255..255>
// SET_MOTOR R <-255..255>
// STOP_MOTOR L / R
// STOP_ALL
// GET_ENCODERS
// GET_GPS
// PING
// ============================================================

void processCommand(char *command) {
  char op[16], side[4];
  int value;

  if (sscanf(command, "%15s %3s %d", op, side, &value) == 3) {
    if (strcmp(op, "SET_MOTOR") == 0) {
      setMotor(side, value);
      return;
    }
  }

  if (sscanf(command, "%15s %3s", op, side) == 2) {
    if (strcmp(op, "STOP_MOTOR") == 0) {
      stopMotor(side);
      return;
    }
  }

  if (strcmp(command, "STOP_ALL") == 0) {
    stopAll();
    Serial.println("OK STOP_ALL");
    return;
  }

  if (strcmp(command, "GET_ENCODERS") == 0) {
    Serial.print("ENC L=");
    Serial.print(leftCount);
    Serial.print(" R=");
    Serial.println(rightCount);
    return;
  }

  if (strcmp(command, "GET_GPS") == 0) {
    sendGPS();
    return;
  }

  if (strcmp(command, "PING") == 0) {
    Serial.println("PONG");
    return;
  }

  Serial.println("ERR INVALID_COMMAND");
}

// ============================================================
// MOTOR CONTROL (value: -255..255, sign = direction)
// ============================================================

void setMotor(const char *side, int value) {
  value = constrain(value, -255, 255);
  bool forward = value >= 0;
  int pwm = abs(value);

  if (strcmp(side, "L") == 0) {
    digitalWrite(L_DIR, forward ? HIGH : LOW);
    analogWrite(L_PWM, pwm);
    Serial.print("OK SET_MOTOR L ");
    Serial.println(value);
    return;
  }

  if (strcmp(side, "R") == 0) {
    digitalWrite(R_DIR, forward ? HIGH : LOW);
    analogWrite(R_PWM, pwm);
    Serial.print("OK SET_MOTOR R ");
    Serial.println(value);
    return;
  }

  Serial.println("ERR INVALID_MOTOR");
}

void stopMotor(const char *side) {
  if (strcmp(side, "L") == 0) {
    analogWrite(L_PWM, 0);
    Serial.println("OK STOP_MOTOR L");
    return;
  }
  if (strcmp(side, "R") == 0) {
    analogWrite(R_PWM, 0);
    Serial.println("OK STOP_MOTOR R");
    return;
  }
  Serial.println("ERR INVALID_MOTOR");
}

void stopAll() {
  analogWrite(L_PWM, 0);
  analogWrite(R_PWM, 0);
}

// ============================================================
// GPS REPORTING — honest about fix status, no fake coordinates
// ============================================================

void sendGPS() {
  if (gps.location.isValid() && gps.location.isUpdated()) {
    Serial.print("GPS FIX ");
    Serial.print(gps.location.lat(), 6);
    Serial.print(",");
    Serial.print(gps.location.lng(), 6);
    Serial.print(" SAT=");
    Serial.println(gps.satellites.value());
  } else {
    Serial.println("GPS NOFIX");
  }
}
