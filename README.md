# Đồ án Điện tử Y sinh - STM32 MAX30100 LCD

Repo này lưu mã nguồn, mô phỏng Proteus, slide thuyết trình và video demo cho đồ án Điện tử Y sinh: thiết kế mạch đo nhịp tim và nồng độ oxy trong máu SpO2. Hệ thống dùng vi điều khiển STM32F103C8T6, cảm biến nhịp tim/oxy MAX30100 và màn hình LCD 1602 để hiển thị trực tiếp giá trị BPM và SpO2.

## Tài liệu và demo

- [Slide thuyết trình PowerPoint](./22207056_DoAnDienTuYSinh_22DTV_CLC1.pptx)
- [Video demo mạch hoạt động](./22207056_DoAnYSinh_LuongHaiLong.mp4)
- [Mô phỏng Proteus](./STM32F103C8T6%20MAX30100%20LCD%202025.pdsprj)
- [Mã nguồn Arduino/STM32](./stm-max30100-lcd.ino)

## Mục tiêu

- Thiết kế thiết bị đo sinh hiệu nhỏ gọn, chi phí thấp và dễ tiếp cận.
- Đo nhịp tim theo BPM bằng cảm biến MAX30100.
- Đo nồng độ oxy trong máu SpO2.
- Hiển thị kết quả trực tiếp trên LCD 16x2.
- Mô phỏng mạch bằng Proteus trước khi triển khai phần cứng.
- Viết chương trình điều khiển trên nền Arduino IDE/STM32duino.

## Phần cứng sử dụng

- STM32F103C8T6 Blue Pill
- Cảm biến MAX30100 hoặc module tương thích MAX30102
- LCD 1602
- Dây nối, nguồn 3.3V/5V phù hợp
- Mạch mô phỏng Proteus trong file `.pdsprj`

## Sơ đồ kết nối chính

### LCD 1602

| LCD | STM32F103C8T6 |
| --- | --- |
| RS | PB12 |
| EN | PB14 |
| D4 | PB15 |
| D5 | PA8 |
| D6 | PA9 |
| D7 | PA10 |

### MAX30100/MAX30102

| Cảm biến | STM32F103C8T6 |
| --- | --- |
| SDA | SDA của I2C |
| SCL | SCL của I2C |
| VCC | 3.3V |
| GND | GND |

Lưu ý: cảm biến nên dùng mức nguồn 3.3V để tránh hỏng module. LCD 1602 thường cần chỉnh biến trở tương phản nếu chỉ hiện ô vuông đen.

## Cách hoạt động

1. Chương trình khởi tạo Serial1, LCD 1602 và cảm biến MAX30100.
2. Cảm biến được cấu hình dòng LED hồng ngoại `MAX30100_LED_CURR_7_6MA` để giảm nhiễu và tiết kiệm năng lượng.
3. Trong vòng lặp chính, `pox.update()` được gọi liên tục để cập nhật dữ liệu thô.
4. Mỗi 1000 ms, chương trình đọc `pox.getHeartRate()` và `pox.getSpO2()`.
5. LCD xóa dữ liệu cũ và hiển thị:
   - Dòng 1: `BPM`
   - Dòng 2: `SpO2`

## Thư viện cần cài

Trong Arduino IDE, cần có:

- `Wire`
- `LiquidCrystal`
- `MAX30100_PulseOximeter`
- Board package STM32duino hoặc cấu hình tương thích STM32F103C8T6

## Cách chạy code

1. Mở file `stm-max30100-lcd.ino` trong Arduino IDE.
2. Chọn board STM32F103C8T6/Blue Pill phù hợp.
3. Cài thư viện MAX30100 Pulse Oximeter nếu máy chưa có.
4. Kiểm tra lại chân LCD và I2C theo phần sơ đồ kết nối.
5. Compile và upload chương trình lên STM32.
6. Mở Serial nếu cần kiểm tra trạng thái khởi tạo cảm biến.

## Cách mở mô phỏng Proteus

1. Mở Proteus.
2. Chọn file `STM32F103C8T6 MAX30100 LCD 2025.pdsprj`.
3. Kiểm tra lại đường dẫn firmware nếu Proteus yêu cầu file `.hex`.
4. Build code trong Arduino IDE để sinh firmware, sau đó gán lại vào vi điều khiển trong Proteus nếu cần.
5. Chạy mô phỏng và quan sát LCD.

## Kinh nghiệm khi đo

- Giữ ngón tay ổn định trên cảm biến để hạn chế số đo nhảy.
- Cố định cảm biến bằng băng dính hoặc gá đỡ khi demo.
- Nếu LCD không hiện chữ, chỉnh biến trở tương phản và kiểm tra thứ tự chân dữ liệu.
- Nếu cảm biến khởi tạo thất bại, kiểm tra lại I2C, nguồn 3.3V và chân SDA/SCL.

## Hướng phát triển

- Thêm ESP8266 hoặc module WiFi để gửi dữ liệu lên điện thoại.
- Kết nối Blynk hoặc dashboard web để theo dõi từ xa.
- Thiết kế vỏ hộp in 3D để cố định ngón tay và tăng tính hoàn thiện.
- Lọc tín hiệu tốt hơn để giảm nhiễu khi người dùng cử động.

## Thông tin

- Môn học: Điện tử Y sinh
- Sinh viên thực hiện: Lương Hải Long - 22207056
- Lớp: 22DTV_CLC
- Nền tảng: STM32 + MAX30100/MAX30102 + LCD 1602
