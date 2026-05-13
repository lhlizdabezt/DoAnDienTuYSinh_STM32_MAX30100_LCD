#include <Wire.h>
#include <LiquidCrystal.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS     1000// thời gian cập nhật xung nhịp tim

const int rs = PB12, en = PB14, d4 = PB15, d5 = PA8, d6 = PA9, d7 = PA10;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
PulseOximeter pox;
uint32_t tsLastReport = 0;
void onBeatDetected()
{
    Serial1.println("Beat!");
}
void setup() {

  Serial1.begin(115200);
  Serial1.print("Initializing pulse oximeter..");
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Do Nh_tim + Oxi");
  // Initialize the PulseOximeter instance
  // Failures are generally due to an improper I2C wiring, missing power supply
  // or wrong target chip
  if (!pox.begin()) {
    Serial1.println("FAILED");
    for(;;);
  } else {
    Serial1.println("SUCCESS");
  }
  pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);

  // Register a callback for the beat detection
  pox.setOnBeatDetectedCallback(onBeatDetected);
}
void loop() {
  pox.update();
  if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
      lcd.clear();//xóa màn hình
      lcd.setCursor(0,0);//hiển thị nhịp tim ở hàng 1 LCD
      lcd.print("BPM: ");
      lcd.print(pox.getHeartRate());//nhịp tim đo được

      lcd.setCursor(0,1);//hiển thị mức oxi ở hàng 2 LCD
      lcd.print("SpO2: ");
      lcd.print(pox.getSpO2());//mức oxi đo được
      lcd.print("%");//dấu phần trăm của mức oxi vd: 80%
      tsLastReport = millis();//thời gian cập nhật lên màn hình
  }
}
