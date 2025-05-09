# YourHome Backend

YourHome là một dự án IoT để điều khiển nhà thông minh, hỗ trợ các vai trò User và Admin. Backend được xây dựng bằng **FastAPI**, tích hợp với **Supabase**, **MQTT**, và **WebSocket** để xử lý dữ liệu realtime và điều khiển thiết bị qua ESP32.

## Tech Stack
- **Python**: 3.11
- **FastAPI**: Framework chính cho API
- **Supabase**: Database (PostgreSQL)
- **MQTT**: Giao tiếp với ESP32 (Mosquitto broker)
- **WebSocket**: Đẩy dữ liệu realtime cho Flutter UI
- **Docker**: Tùy chọn triển khai (dự phòng)

## Cấu trúc thư mục
```
yourhome_backend/
├── config/         # Cấu hình (database, settings,...)
├── core/          # Logic cốt lõi (interfaces, events)
├── models/        # Pydantic schemas
├── services/      # Logic nghiệp vụ (MQTT, device, log,...)
├── routes/        # API endpoints
├── utils/         # Hàm tiện ích
├── plugins/       # Module mở rộng (dành cho tương lai)
├── tests/         # Test cases
├── main.py        # Điểm vào chính
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 1. Cài đặt môi trường
1. Clone repository:
   ```bash
   git clone <your-repo-url>
   cd yourhome_backend
   ```
2. Tạo virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```
3. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Tạo file `.env` dựa trên `.env.example` và điền thông tin:
   ```
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-key
   MQTT_BROKER=broker.hivemq.com
   MQTT_PORT=1883
   SECRET_KEY=your-jwt-secret
   ```
5. Chạy ứng dụng:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - `--reload`: Tự động reload khi code thay đổi (chỉ dùng khi phát triển).
   - Truy cập API docs tại: `http://localhost:8000/docs`

## API Endpoints
- **Auth**:
  - `POST /login`: Đăng nhập
  - `POST /register`: Đăng ký
- **Devices**:
  - `GET /devices/{home_id}`: Lấy danh sách thiết bị
  - `POST /devices`: Thêm thiết bị mới
  - `PUT /devices/{device_id}`: Sửa thiết bị
  - `DELETE /devices/{device_id}`: Xoá thiết bị
- **Logs**:
  - `GET /logs/{home_id}`: Lấy danh sách log (hỗ trợ lọc theo thời gian)
- **Admin**:
  - `GET /admin/homes`: Xem danh sách nhà và trạng thái

## Tích hợp với ESP32
- ESP32 cần subscribe vào topic `yourhome/{device_id}` để nhận lệnh (enable/disable port).
- Đáp ứng yêu cầu cổng trống qua topic `yourhome/{home_id}/ports/response`.

## Ghi chú
- Dự án sử dụng event-driven architecture để dễ mở rộng.
- Hỗ trợ WebSocket tại `/ws` để đẩy dữ liệu realtime cho Flutter UI.
- Để tối ưu phát triển, dùng `--reload` với `uvicorn` trên local.
