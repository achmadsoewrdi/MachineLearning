const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
const corsOptions = {
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true
};
app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage: storage });

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Meme Detector API is running!' });
});

// Endpoint untuk deteksi gesture
app.post('/api/detect', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No image provided' });
    }

    // Call Python script untuk deteksi gesture
    const { spawn } = require('child_process');
    const pythonProcess = spawn('py', ['-3.12', 'detect_gesture.py', req.file.path]);

    let dataString = '';
    let errorString = '';

    pythonProcess.stdout.on('data', (data) => {
      dataString += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      errorString += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error('Python error:', errorString);
        return res.status(500).json({
          error: 'Error processing image',
          details: errorString
        });
      }

      try {
        const result = JSON.parse(dataString);
        res.json(result);
      } catch (parseError) {
        console.error('JSON parse error:', parseError);
        res.status(500).json({ error: 'Error parsing detection result' });
      }
    });
  } catch (error) {
    console.error('Error processing image:', error);
    res.status(500).json({ error: 'Error processing image' });
  }
});

// Endpoint untuk mendapatkan daftar meme
app.get('/api/memes', (req, res) => {
  // TODO: Return list of available memes
  res.json({
    memes: [
      { id: 1, name: 'thumbs_up', file: 'reaction_thumb.jpg' },
      { id: 2, name: 'pointing', file: 'reaction_point.jpg' },
      { id: 3, name: 'touching_head', file: 'reaction_head.jpg' }
    ]
  });
});

// Create uploads directory if it doesn't exist
const fs = require('fs');
const uploadsDir = './uploads';
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir);
}

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
