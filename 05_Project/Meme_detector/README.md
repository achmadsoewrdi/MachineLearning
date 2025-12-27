# 🐒 Gesture-to-Meme Reaction Detector

Aplikasi interaktif berbasis AI yang mendeteksi gerakan tangan dan wajah menggunakan **MediaPipe** dan **OpenCV**. Ketika Anda melakukan gestur tertentu (jempol, menunjuk, atau memegang kepala), aplikasi akan menampilkan gambar reaksi meme monyet yang sesuai!

![Python](https://img.shields.io/badge/Python-3.12-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Latest-red)

---

## 🎯 Fitur

- **Deteksi Jempol Up 👍**: Tampilkan meme monyet memberikan jempol
- **Deteksi Menunjuk ☝️**: Tampilkan meme monyet menunjuk
- **Deteksi Pegang Kepala 🤦‍♂️**: Tampilkan meme monyet bingung/facepalm
- **Real-time Detection**: Deteksi gestur secara langsung melalui webcam
- **Pop-up Reaction**: Meme muncul di jendela terpisah selama 2 detik

---

## 📋 Prasyarat

- **Python 3.12** (⚠️ Python 3.13 belum didukung MediaPipe)
- **Webcam** yang berfungsi
- **Windows OS** (untuk command yang digunakan)

---

## 🛠️ Instalasi

### 1. Clone atau Download Repository
```bash
git clone <repository-url>
cd Meme_detector
```

### 2. Install Dependencies
Pastikan Anda menggunakan **Python 3.12**:

```powershell
py -3.12 -m pip install mediapipe==0.10.14 opencv-python numpy
```

> **⚠️ Penting**: Gunakan MediaPipe versi **0.10.14** karena versi terbaru (0.10.31) tidak memiliki API `solutions` yang dibutuhkan.

### 3. Verifikasi Instalasi
```powershell
py -3.12 -c "import mediapipe as mp; print('MediaPipe version:', mp.__version__)"
```

Output yang diharapkan: `MediaPipe version: 0.10.14`

---

## 🚀 Cara Menjalankan

```powershell
py -3.12 main.py
```

### Cara Keluar
- Tekan **`Esc`** pada keyboard untuk menutup aplikasi
- Atau tekan **`Ctrl + C`** di terminal

---

## 🎮 Cara Menggunakan

1. **Jalankan aplikasi** dengan command di atas
2. **Posisikan diri** di depan webcam dengan pencahayaan yang cukup
3. **Lakukan gestur** berikut:

| Gestur | Cara Melakukan | Reaksi Meme |
|--------|----------------|-------------|
| **Jempol Up 👍** | Angkat jempol ke atas, jari lain tertutup | Monyet memberikan jempol |
| **Menunjuk ☝️** | Angkat telunjuk ke atas, jari lain tertutup | Monyet menunjuk |
| **Pegang Kepala 🤦** | Tangan menyentuh dahi/kepala | Monyet bingung/facepalm |

4. **Meme akan muncul** di jendela terpisah selama 2 detik
5. Tekan **Esc** untuk keluar

---

## 📁 Struktur Proyek

```
Meme_detector/
├── main.py                    # Program utama
├── assets/                    # Folder gambar reaksi
│   ├── reaction_thumb.jpg     # Meme jempol
│   ├── reaction_point.jpg     # Meme menunjuk
│   └── reaction_head.jpg      # Meme pegang kepala
└── README.md                  # Dokumentasi ini
```

---

## ⚙️ Cara Kerja (Technical)

### Deteksi Gestur dengan MediaPipe

Aplikasi menggunakan **MediaPipe Hands** dan **MediaPipe Face Mesh** untuk mendeteksi landmark (titik kunci) pada tangan dan wajah.

#### 1. Jempol Up
```python
# Logika: Ujung jempol (landmark 4) lebih tinggi dari sendi (landmark 3)
# DAN jari lainnya tertutup
if thumb_tip.y < thumb_ip.y and all_fingers_closed:
    show_meme("reaction_thumb.jpg")
```

#### 2. Menunjuk
```python
# Logika: Ujung telunjuk (landmark 8) lebih tinggi dari sendi (landmark 6)
# DAN jari lainnya tertutup
if index_tip.y < index_pip.y and other_fingers_closed:
    show_meme("reaction_point.jpg")
```

#### 3. Pegang Kepala
```python
# Logika: Koordinat Y tangan <= koordinat Y dahi (face landmark 10)
if hand_y <= forehead_y:
    show_meme("reaction_head.jpg")
```

---

## ❓ Troubleshooting

### Error: `AttributeError: module 'mediapipe' has no attribute 'solutions'`
**Penyebab**: MediaPipe versi terbaru (0.10.31) tidak memiliki API `solutions`.

**Solusi**:
```powershell
py -3.12 -m pip uninstall mediapipe -y
py -3.12 -m pip install mediapipe==0.10.14
```

### Error: `python: command not found` atau masih error
**Penyebab**: Menggunakan Python 3.13 atau versi default yang salah.

**Solusi**: Pastikan menggunakan `py -3.12` bukan `python`:
```powershell
py -3.12 main.py
```

### Gestur tidak terdeteksi
- ✅ Pastikan ruangan **cukup terang**
- ✅ Posisikan tangan **jelas terlihat** di depan kamera
- ✅ Jangan terlalu dekat atau jauh dari kamera
- ✅ Lakukan gestur dengan **jelas dan stabil**

### Webcam tidak terbuka
- ✅ Pastikan webcam tidak digunakan aplikasi lain
- ✅ Cek izin akses kamera di Windows Settings
- ✅ Restart aplikasi

---

## 🔧 Kustomisasi

### Mengganti Gambar Meme
Ganti file di folder `assets/` dengan gambar Anda sendiri (format `.jpg` atau `.png`):
- `reaction_thumb.jpg` - Meme untuk jempol
- `reaction_point.jpg` - Meme untuk menunjuk
- `reaction_head.jpg` - Meme untuk pegang kepala

### Mengubah Durasi Tampilan Meme
Edit variabel `REACTION_DURATION` di `main.py`:
```python
REACTION_DURATION = 2.0  # Ubah angka ini (dalam detik)
```

---

## 🧪 Requirements

```
mediapipe==0.10.14
opencv-python>=4.8.0
numpy>=1.24.0
```

---

## 📝 Lisensi

Proyek ini dibuat untuk tujuan edukasi dan pembelajaran AI/Computer Vision.

---

## 👨‍💻 Kontributor

Dibuat dengan ❤️ menggunakan MediaPipe dan OpenCV

---

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) - Framework untuk ML solutions
- [OpenCV](https://opencv.org/) - Library Computer Vision
- [NumPy](https://numpy.org/) - Scientific computing

---

**Selamat mencoba! 🎉**
