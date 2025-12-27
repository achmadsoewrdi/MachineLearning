# 🐵 Meme Detector

Aplikasi web interaktif yang mendeteksi gesture tangan menggunakan AI dan menampilkan meme reaksi yang sesuai.

## 📁 Struktur Projekt

```
Meme_detector/
├── backend/          # Express.js API server
├── frontend/         # React + Tailwind UI
└── main.py          # Python ML model (gesture detection)
```

## 🚀 Quick Start

### Backend Setup

```bash
cd backend
npm install
npm start
```

Server akan berjalan di `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

## 🛠️ Tech Stack

### Backend
- **Express.js** - Web framework
- **Multer** - File upload handling
- **CORS** - Cross-origin resource sharing

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **react-webcam** - Webcam integration
- **Axios** - HTTP client

### Machine Learning
- **MediaPipe** - Gesture detection
- **OpenCV** - Image processing
- **Python** - ML model

## 📝 Features

- 📸 Real-time webcam capture
- 🤖 AI-powered gesture detection
- 🎨 Modern, responsive UI
- 🐵 Meme reactions based on detected gestures

## 🎯 Supported Gestures

- 👍 Thumbs Up
- 👉 Pointing
- 🤔 Touching Head

## 📖 Documentation

Lihat README di masing-masing folder untuk detail lebih lanjut:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## 🔧 Development

1. Jalankan backend server terlebih dahulu
2. Jalankan frontend development server
3. Buka browser di `http://localhost:5173`
4. Izinkan akses webcam
5. Ambil foto dan deteksi gesture!

## 📦 Portfolio Ready

Proyek ini siap untuk digunakan sebagai portfolio dengan:
- Clean code structure
- Modern tech stack
- Professional UI/UX
- Full-stack implementation
