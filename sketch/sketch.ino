#include "Arduino_RouterBridge.h"
#include <CNCShield.h>
#include <AccelStepper.h>

// ============================================================
// CNC SHIELD
// ============================================================

CNCShield cnc_shield;

StepperMotor *motorX;
StepperMotor *motorY;
StepperMotor *motorZ;

// ============================================================
// FIXED MOTOR SPEEDS
// ============================================================

const float X_SPEED = 50.0;
const float Y_SPEED = 50.0;
const float Z_SPEED = 50.0;

// ============================================================
// CURRENT MOTOR STATE (-1, 0, 1)
// ============================================================

int directionX = 0;
int directionY = 0;
int directionZ = 0;

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

// ============================================================
// SETUP
// ============================================================

void setup() {
  cnc_shield.begin();

  motorX = cnc_shield.get_motor(0);
  motorY = cnc_shield.get_motor(1);
  motorZ = cnc_shield.get_motor(2);

  stepperX.setMaxSpeed(X_SPEED);
  stepperY.setMaxSpeed(Y_SPEED);
  stepperZ.setMaxSpeed(Z_SPEED);

  stepperX.setSpeed(0);
  stepperY.setSpeed(0);
  stepperZ.setSpeed(0);

  Bridge.begin();

  Bridge.provide("set_motor_x", set_motor_x);
  Bridge.provide("set_motor_y", set_motor_y);
  Bridge.provide("set_motor_z", set_motor_z);

  Bridge.provide("stop_motor_x", stop_motor_x);
  Bridge.provide("stop_motor_y", stop_motor_y);
  Bridge.provide("stop_motor_z", stop_motor_z);

  Bridge.provide("stop_all", stop_all);

  Bridge.provide("get_motor_x", get_motor_x);
  Bridge.provide("get_motor_y", get_motor_y);
  Bridge.provide("get_motor_z", get_motor_z);
}

// ============================================================
// MAIN LOOP — must run continuously to pulse steps
// ============================================================

void loop() {
  stepperX.runSpeed();
  stepperY.runSpeed();
  stepperZ.runSpeed();
}

// ============================================================
// SET MOTOR (direction: -1, 0, 1)
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

void set_motor_z(int direction) {
  direction = clampDirection(direction);
  directionZ = direction;
  stepperZ.setSpeed(directionZ * Z_SPEED);
}

// ============================================================
// STOP INDIVIDUAL MOTORS
// ============================================================

void stop_motor_x() {
  directionX = 0;
  stepperX.setSpeed(0);
}

void stop_motor_y() {
  directionY = 0;
  stepperY.setSpeed(0);
}

void stop_motor_z() {
  directionZ = 0;
  stepperZ.setSpeed(0);
}

// ============================================================
// STOP ALL
// ============================================================

void stop_all() {
  stop_motor_x();
  stop_motor_y();
  stop_motor_z();
}

// ============================================================
// GET STATE
// ============================================================

int get_motor_x() { return directionX; }
int get_motor_y() { return directionY; }
int get_motor_z() { return directionZ; }

// ============================================================
// HELPER
// ============================================================

int clampDirection(int direction) {
  if (direction > 0) return 1;
  if (direction < 0) return -1;
  return 0;
}