#include "Arduino_RouterBridge.h"
#include <CNCShield.h>
#include <AccelStepper.h>
#include <Servo.h>

// ============================================================
// CNC SHIELD
// ============================================================

CNCShield cnc_shield;

StepperMotor *motorX;
StepperMotor *motorY;
StepperMotor *motorZ;

// ============================================================
// A AXIS — driven directly, bypassing CNCShield (library only
// supports 3 motors). Standard CNC Shield V3 A-axis pins.
// ============================================================

#define A_STEP_PIN 12
#define A_DIR_PIN  13

// ============================================================
// SERVO (360° continuous rotation, metal gear) — runs for a
// fixed 3s window then auto-stops. Non-blocking via millis().
// ============================================================

#define SERVO_PIN 9

const int SERVO_STOP = 90;   // no rotation
const int SERVO_CW   = 180;  // full speed one way
const int SERVO_CCW  = 0;    // full speed other way
const unsigned long SERVO_RUN_MS = 3000;  // 3 seconds

Servo gripperServo;
int servoDirection = 0;          // -1, 0, 1 — for UI state
bool servoRunning = false;
unsigned long servoStopAt = 0;

// ============================================================
// FIXED MOTOR SPEEDS
// ============================================================

const float X_SPEED = 50.0;
const float Y_SPEED = 50.0;
const float Z_SPEED = 50.0;
const float A_SPEED = 50.0;

// ============================================================
// CURRENT MOTOR STATE (-1, 0, 1)
// ============================================================

int directionX = 0;
int directionY = 0;
int directionZ = 0;
int directionA = 0;

// ============================================================
// ACCELSTEPPER CALLBACKS
// ============================================================

void xForward()  { motorX->step(CLOCKWISE); }
void xBackward() { motorX->step(COUNTER); }

void yForward()  { motorY->step(CLOCKWISE); }
void yBackward() { motorY->step(COUNTER); }

void zForward()  { motorZ->step(CLOCKWISE); }
void zBackward() { motorZ->step(COUNTER); }

AccelStepper stepperX(xForward, xBackward);
AccelStepper stepperY(yForward, yBackward);
AccelStepper stepperZ(zForward, zBackward);
AccelStepper stepperA(AccelStepper::DRIVER, A_STEP_PIN, A_DIR_PIN);

// ============================================================
// SETUP
// ============================================================

void setup() {
  Bridge.begin();   // must come first, before any Bridge.provide()

  pinMode(A_STEP_PIN, OUTPUT);
  pinMode(A_DIR_PIN, OUTPUT);

  cnc_shield.begin();

  motorX = cnc_shield.get_motor(0);
  motorY = cnc_shield.get_motor(1);
  motorZ = cnc_shield.get_motor(2);

  stepperX.setMaxSpeed(X_SPEED);
  stepperY.setMaxSpeed(Y_SPEED);
  stepperZ.setMaxSpeed(Z_SPEED);
  stepperA.setMaxSpeed(A_SPEED);

  stepperX.setSpeed(0);
  stepperY.setSpeed(0);
  stepperZ.setSpeed(0);
  stepperA.setSpeed(0);

  gripperServo.attach(SERVO_PIN);
  gripperServo.write(SERVO_STOP);

  Bridge.provide("set_motor_x", set_motor_x);
  Bridge.provide("set_motor_y", set_motor_y);

  Bridge.provide("set_joint_za", set_joint_za);
  Bridge.provide("stop_joint_za", stop_joint_za);
  Bridge.provide("get_joint_za", get_joint_za);

  Bridge.provide("stop_motor_x", stop_motor_x);
  Bridge.provide("stop_motor_y", stop_motor_y);

  Bridge.provide("stop_all", stop_all);

  Bridge.provide("get_motor_x", get_motor_x);
  Bridge.provide("get_motor_y", get_motor_y);

  Bridge.provide("set_servo_dir", set_servo_dir);
  Bridge.provide("stop_servo", stop_servo);
  Bridge.provide("get_servo_dir", get_servo_dir);
}

// ============================================================
// MAIN LOOP — must run continuously to pulse steps
// ============================================================

void loop() {
  stepperX.runSpeed();
  stepperY.runSpeed();
  stepperZ.runSpeed();
  stepperA.runSpeed();

  if (servoRunning && millis() >= servoStopAt) {
    gripperServo.write(SERVO_STOP);
    servoRunning = false;
    servoDirection = 0;
  }
}

// ============================================================
// SET MOTOR (direction: -1, 0, 1) — X and Y, independent
// ============================================================

void set_motor_x(int direction) {
  direction = clampDirection(direction);
  directionX = direction;
  stepperX.setSpeed(directionX * X_SPEED);
}

void set_motor_y(int direction) {
  direction = clampDirection(direction);
  directionY = direction;
  stepperY.setSpeed(directionY * Y_SPEED);
}

// ============================================================
// JOINT CONTROL — Z and A face each other and must counter-
// rotate to move the shared link in one direction.
// ============================================================

void set_joint_za(int direction) {
  direction = clampDirection(direction);

  directionZ = direction;
  directionA = -direction;   // A always spins opposite to Z

  stepperZ.setSpeed(directionZ * Z_SPEED);
  stepperA.setSpeed(directionA * A_SPEED);
}

void stop_joint_za() {
  directionZ = 0;
  directionA = 0;
  stepperZ.setSpeed(0);
  stepperA.setSpeed(0);
}

int get_joint_za() {
  return directionZ;
}

// ============================================================
// STOP INDIVIDUAL MOTORS (X, Y only — Z/A stop via joint)
// ============================================================

void stop_motor_x() {
  directionX = 0;
  stepperX.setSpeed(0);
}

void stop_motor_y() {
  directionY = 0;
  stepperY.setSpeed(0);
}

// ============================================================
// STOP ALL
// ============================================================

void stop_all() {
  stop_motor_x();
  stop_motor_y();
  stop_joint_za();
  stop_servo();
}

// ============================================================
// GET STATE
// ============================================================

int get_motor_x() { return directionX; }
int get_motor_y() { return directionY; }

// ============================================================
// SERVO CONTROL (360° continuous rotation, 3s auto-stop)
// ============================================================

void set_servo_dir(int direction) {
  direction = clampDirection(direction);

  if (direction > 0) {
    gripperServo.write(SERVO_CW);
  } else if (direction < 0) {
    gripperServo.write(SERVO_CCW);
  } else {
    gripperServo.write(SERVO_STOP);
  }

  servoDirection = direction;

  if (direction == 0) {
    servoRunning = false;
  } else {
    servoRunning = true;
    servoStopAt = millis() + SERVO_RUN_MS;
  }
}

void stop_servo() {
  gripperServo.write(SERVO_STOP);
  servoDirection = 0;
  servoRunning = false;
}

int get_servo_dir() {
  return servoDirection;
}

// ============================================================
// HELPER
// ============================================================

int clampDirection(int direction) {
  if (direction > 0) return 1;
  if (direction < 0) return -1;
  return 0;
}