#include "Arduino_RouterBridge.h"
#include <CNCShield.h>
#include <AccelStepper.h>

CNCShield cnc_shield;
StepperMotor *motorX;

const float X_SPEED = 100.0;
int directionX = 0;

void xForward() { motorX->step(CLOCKWISE); }
void xBackward() { motorX->step(COUNTER); }

AccelStepper stepperX(xForward, xBackward);

void setup() {
  cnc_shield.begin();
  motorX = cnc_shield.get_motor(0);

  stepperX.setMaxSpeed(X_SPEED);
  stepperX.setSpeed(0);

  Bridge.begin();
  Bridge.provide("set_motor_x", set_motor_x);
  Bridge.provide("get_motor_x", get_motor_x);
}

void loop() {
  stepperX.runSpeed();  // must run every cycle — this is what pulses steps
}

// Callable from Python: direction is -1, 0, or 1
void set_motor_x(int direction) {
  if (direction > 0) direction = 1;
  else if (direction < 0) direction = -1;
  else direction = 0;

  directionX = direction;
  stepperX.setSpeed(directionX * X_SPEED);
}

// Callable from Python: returns current direction
int get_motor_x() {
  return directionX;
}