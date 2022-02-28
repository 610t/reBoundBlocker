/*
   Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleScan.cpp
   Ported to Arduino ESP32 by pcbreflux

   Based on AmbientDataInc work for Arduino: https://github.com/AmbientDataInc/EnvSensorBleGw/blob/master/src/envSensor_esp32/BLE_BME280_bcast/BLE_BME280_bcast.ino
*/

#include <M5StickC.h>
#include "BLEDevice.h"
#include "BLEServer.h"
#include "BLEUtils.h"
//#include "esp_sleep.h"
//#include <Wire.h>

static uint8_t seq; // sequence number for advertisement

// Variables for step counter
int step = 0;
float total = 0;
int count = 0;
float avg = 1.1;
float width = avg / 10;
boolean state = false;
boolean old_state = false;
int old_time = 0;

void setAdvData(BLEAdvertising *pAdvertising) {
  BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();

  oAdvertisementData.setFlags(0x06); // BR_EDR_NOT_SUPPORTED | LE General Discoverable Mode

  std::string strServiceData = "";
  strServiceData += (char)0x06;   // Length of data
  strServiceData += (char)0xff;   // AD Type 0xFF: Manufacturer specific data
  strServiceData += (char)0xff;   // Test manufacture ID low byte
  strServiceData += (char)0xff;   // Test manufacture ID high byte
  strServiceData += (char)seq;                  // Sequence number
  strServiceData += (char)(step & 0xff);        // step low byte
  strServiceData += (char)((step >> 8) & 0xff); // step high byte

  oAdvertisementData.addData(strServiceData);
  pAdvertising->setAdvertisementData(oAdvertisementData);
}

void setup() {
  M5.begin();

  // Improve battery life.
  M5.Axp.ScreenBreath(8);
  //setCpuFrequencyMhz(10);

  // Display setting
  M5.Lcd.setRotation(1);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextSize(5);

  // IMU & LED
  M5.IMU.Init();
  pinMode(M5_LED, OUTPUT);

  Serial.begin(115200);
}

void loop() {
  // Accelerometer value for x,y,z axis.
  float accX = 0;
  float accY = 0;
  float accZ = 0;

  // Get accel.
  M5.IMU.getAccelData(&accX, &accY, &accZ);
  float accel = sqrt(accX * accX + accY * accY + accZ * accZ);

  // Calibration for average acceleration.
  if (count < 100) {
    total += accel;
    count += 1;
  } else {
    avg = total / count;
    width = avg / 10;
    total = avg;
    count = 1;
  }

  // When current accel. is ...
  if (accel > avg + width) {
    state = true;
  } else if (accel < avg - width) {
    state = false;
  }

  // Count up step.
  if (!old_state && state) {
    step += 1;
    digitalWrite(M5_LED, LOW);  // led on

    // Display step
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.printf("Step:\n");
    M5.Lcd.printf("%5d\n", step);
    Serial.printf("Step:%5d\n", step);
  } else {
    digitalWrite(M5_LED, HIGH); // led off
  }
  old_state = state;

  delay(100);

  if (millis() - old_time > 5 * 1000 || old_time > millis()) {
    BLEDevice::init("reBoundBlocker");
    BLEServer *pServer = BLEDevice::createServer();

    BLEAdvertising *pAdvertising = pServer->getAdvertising();
    setAdvData(pAdvertising);

    pAdvertising->start();
    // Serial.println("Advertizing started...");
    delay(0.1 * 1000);
    pAdvertising->stop();

    seq++;
    delay(0.1 * 1000);

    old_time = millis();
  }
}
