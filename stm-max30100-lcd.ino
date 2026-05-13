#include <Wire.h>
#include <LiquidCrystal.h>
#include "MAX30100_PulseOximeter.h"

const uint32_t REPORTING_PERIOD_MS = 1000;  // Chu kỳ cập nhật LCD và Serial, đơn vị ms.

const int LCD_RS = PB12;
const int LCD_EN = PB14;
const int LCD_D4 = PB15;
const int LCD_D5 = PA8;
const int LCD_D6 = PA9;
const int LCD_D7 = PA10;

LiquidCrystal lcd(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7);
PulseOximeter pox;

uint32_t tsLastReport = 0;

void onBeatDetected()
{
  Serial1.println("Phat hien nhip tim");
}

void setup()
{
  Serial1.begin(115200);
  Serial1.println("Khoi dong mach do nhip tim va SpO2");

  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Do nhip tim");
  lcd.setCursor(0, 1);
  lcd.print("Dang khoi dong");

  if (!pox.begin()) {
    Serial1.println("FAILED: kiem tra I2C, nguon va module MAX30100/MAX30102");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Cam bien loi");
    lcd.setCursor(0, 1);
    lcd.print("Kiem tra I2C");

    for (;;) {
      delay(1000);
    }
  }

  Serial1.println("SUCCESS: cam bien san sang");
  pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);

  pox.setOnBeatDetectedCallback(onBeatDetected);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("San sang do");
}

void loop()
{
  pox.update();

  if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
    const float heartRate = pox.getHeartRate();
    const uint8_t spo2 = pox.getSpO2();

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("BPM : ");
    lcd.print(heartRate, 0);

    lcd.setCursor(0, 1);
    lcd.print("SpO2: ");
    lcd.print(spo2);
    lcd.print("%");

    Serial1.print("BPM=");
    Serial1.print(heartRate, 1);
    Serial1.print(" | SpO2=");
    Serial1.print(spo2);
    Serial1.println("%");

    tsLastReport = millis();
  }
}
