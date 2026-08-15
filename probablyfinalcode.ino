#include <ESP32Servo.h>

Servo panServo;
Servo tiltServo;

int panAngle = 90;
int tiltAngle = 90;

void setup() {
  Serial.begin(115200);

  panServo.setPeriodHertz(50);
  tiltServo.setPeriodHertz(50);

  // GPIO pins
  panServo.attach(19, 500, 2400);
  tiltServo.attach(18, 500, 2400);

  // Center servos
  panServo.write(panAngle);
  tiltServo.write(tiltAngle);

  delay(1000);
}

void loop() {

  if (Serial.available()) {

    String data = Serial.readStringUntil('\n');

    int comma = data.indexOf(',');

    if (comma > 0) {

      int centerX = data.substring(0, comma).toInt();
      int centerY = data.substring(comma + 1).toInt();

      // PAN
      if (centerX < 280)
        panAngle++;

      else if (centerX > 360)
        panAngle--;

      // TILT
      if (centerY < 290)
    tiltAngle++;

else if (centerY > 320)
    tiltAngle--;

      // Keep angles safe
      panAngle = constrain(panAngle, 0, 180);
      tiltAngle = constrain(tiltAngle, 0, 180);

      panServo.write(panAngle);
      tiltServo.write(tiltAngle);

      Serial.print("Pan: ");
      Serial.print(panAngle);
      Serial.print("  Tilt: ");
      Serial.println(tiltAngle);
    }
  }
}
