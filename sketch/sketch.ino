#include <Arduino_RouterBridge.h>
#include <CNCShield.h>
#include <AccelStepper.h>


// ============================================================
// CNC SHIELD
// ============================================================

CNCShield cnc_shield;


// ============================================================
// MOTOR OBJECTS
// ============================================================

StepperMotor *motorX;
StepperMotor *motorY;
StepperMotor *motorZ;


// ============================================================
// FIXED MOTOR SPEEDS
// ============================================================

const float X_SPEED = 100.0;
const float Y_SPEED = 50.0;
const float Z_SPEED = 50.0;


// ============================================================
// CURRENT DIRECTIONS
//
//  1 = clockwise
// -1 = counter-clockwise
//  0 = stopped
// ============================================================

int directionX = 0;
int directionY = 0;
int directionZ = 0;


// ============================================================
// ACCELSTEPPER CALLBACKS
// ============================================================

// X
void xForward()
{
  motorX->step(CLOCKWISE);
}

void xBackward()
{
  motorX->step(COUNTER);
}


// Y
void yForward()
{
  motorY->step(CLOCKWISE);
}

void yBackward()
{
  motorY->step(COUNTER);
}


// Z
void zForward()
{
  motorZ->step(CLOCKWISE);
}

void zBackward()
{
  motorZ->step(COUNTER);
}


// ============================================================
// ACCELSTEPPER OBJECTS
// ============================================================

AccelStepper stepperX(xForward, xBackward);
AccelStepper stepperY(yForward, yBackward);
AccelStepper stepperZ(zForward, zBackward);


// ============================================================
// SET X MOTOR
//
// direction:
//   1  = clockwise
//  -1  = counter-clockwise
//   0  = stop
// ============================================================

void setX(int direction)
{
  if (direction > 0)
    direction = 1;

  else if (direction < 0)
    direction = -1;

  else
    direction = 0;


  directionX = direction;

  stepperX.setSpeed(directionX * X_SPEED);
}


// ============================================================
// SET Y MOTOR
// ============================================================

void setY(int direction)
{
  if (direction > 0)
    direction = 1;

  else if (direction < 0)
    direction = -1;

  else
    direction = 0;


  directionY = direction;

  stepperY.setSpeed(directionY * Y_SPEED);
}


// ============================================================
// SET Z MOTOR
// ============================================================

void setZ(int direction)
{
  if (direction > 0)
    direction = 1;

  else if (direction < 0)
    direction = -1;

  else
    direction = 0;


  directionZ = direction;

  stepperZ.setSpeed(directionZ * Z_SPEED);
}


// ============================================================
// STOP ALL MOTORS
// ============================================================

void stopAll()
{
  directionX = 0;
  directionY = 0;
  directionZ = 0;

  stepperX.setSpeed(0);
  stepperY.setSpeed(0);
  stepperZ.setSpeed(0);
}


// ============================================================
// SETUP
// ============================================================

void setup()
{
  // Start RouterBridge
  Bridge.begin();

  // Start CNC shield
  cnc_shield.begin();


  // Get motors
  motorX = cnc_shield.get_motor(0);
  motorY = cnc_shield.get_motor(1);
  motorZ = cnc_shield.get_motor(2);


  // Set maximum speeds
  stepperX.setMaxSpeed(X_SPEED);
  stepperY.setMaxSpeed(Y_SPEED);
  stepperZ.setMaxSpeed(Z_SPEED);


  // Initially stopped
  stepperX.setSpeed(0);
  stepperY.setSpeed(0);
  stepperZ.setSpeed(0);


  // ==========================================================
  // EXPOSE FUNCTIONS TO LINUX / PYTHON
  // ==========================================================

  Bridge.provide_safe("set_x", setX);
  Bridge.provide_safe("set_y", setY);
  Bridge.provide_safe("set_z", setZ);

  Bridge.provide_safe("stop_all", stopAll);
}


// ============================================================
// LOOP
// ============================================================

void loop()
{
  // Run all motors continuously

  stepperX.runSpeed();
  stepperY.runSpeed();
  stepperZ.runSpeed();
}