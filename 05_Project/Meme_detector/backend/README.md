# Meme Detector Backend

Backend API untuk aplikasi Meme Detector menggunakan Express.js dan Python ML model.

## Setup

### 1. Install Node.js dependencies:
```bash
npm install
```

### 2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

**Python dependencies:**
- opencv-python (untuk image processing)
- mediapipe (untuk gesture detection)
- numpy (untuk array operations)

### 3. Jalankan server:
```bash
npm start
```

Atau untuk development mode dengan auto-reload:
```bash
npm run dev
```

Server akan berjalan di `http://localhost:5000`

## API Endpoints

### GET /
Health check endpoint

### POST /api/detect
Upload gambar untuk deteksi gesture menggunakan MediaPipe ML model
- Method: POST
- Body: FormData dengan field 'image'
- Response: JSON dengan informasi gesture yang terdeteksi

**Supported Gestures:**
- 👍 Thumbs Up
- 👉 Pointing
- 🤔 Touching Head

**Response format:**
```json
{
  "success": true,
  "gesture": "thumbs_up",
  "confidence": 0.95,
  "meme": "reaction_thumb.jpg"
}
```

### GET /api/memes
Mendapatkan daftar meme yang tersedia
- Method: GET
- Response: JSON array dengan daftar meme

## Dependencies

### Node.js
- express: Web framework
- cors: Enable CORS
- multer: File upload handling

### Python
- opencv-python: Image processing
- mediapipe: Hand and face detection
- numpy: Array operations

