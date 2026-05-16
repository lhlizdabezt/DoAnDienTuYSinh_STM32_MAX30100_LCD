# v1.2.0 - Nâng cấp portfolio Điện tử Y sinh STM32

Ngày phát hành: 2026-05-17

## Mục tiêu

Phiên bản này làm rõ hơn giá trị review của đồ án **STM32F103C8T6 + MAX30100/MAX30102 + LCD1602** theo hướng portfolio kỹ thuật: người xem có thể kiểm tra nhanh bài toán, phần cứng, firmware, mô phỏng, demo và giới hạn học thuật của hệ thống.

## Điểm mới

- Bổ sung cấu trúc README theo hướng HR và kỹ sư review: ma trận kiểm chứng, luồng đo, checklist demo, lỗi thường gặp và giới hạn kỹ thuật.
- Thêm script `scripts/render_pulse_wave.py` để tạo lại GIF chuyển động `assets/pulse-wave.gif` và ảnh preview khi cần chỉnh spacing hoặc text.
- Đóng gói release kèm source snapshot, slide, video demo, project Proteus, SVG hero và GIF motion để người xem không phải dò file thủ công.
- Giữ nguyên nguyên tắc hiển thị: Markdown và bảng biểu dùng tiếng Việt có dấu; chữ trong SVG giữ ASCII/English để tránh lỗi render Unicode.

## Phạm vi kỹ thuật

- Board: STM32F103C8T6 Blue Pill.
- Cảm biến: MAX30100 hoặc MAX30102.
- Hiển thị: LCD1602 chế độ 4-bit.
- Giao tiếp chính: I2C, GPIO, Serial1.
- Công cụ: Arduino IDE, STM32duino, Proteus.

## Giới hạn

Đây là đồ án học thuật và portfolio kỹ thuật. Repo không tuyên bố thiết bị đạt chuẩn y tế, không thay thế thiết bị chẩn đoán và chưa có kiểm định lâm sàng.
