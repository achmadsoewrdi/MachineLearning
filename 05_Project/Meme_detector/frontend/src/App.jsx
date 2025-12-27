import { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

function App() {
  const [capturedImage, setCapturedImage] = useState(null);
  const [detectionResult, setDetectionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showMeme, setShowMeme] = useState(false);
  const webcamRef = useRef(null);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

  const captureImage = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
  };

  const detectGesture = async () => {
    if (!capturedImage) return;

    setLoading(true);
    try {
      const blob = await fetch(capturedImage).then(r => r.blob());
      const formData = new FormData();
      formData.append('image', blob, 'capture.jpg');

      const response = await axios.post(`${API_URL}/api/detect`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.gesture === 'none') {
        alert('Tidak ada gesture yang terdeteksi. Coba lagi dengan gesture yang lebih jelas!');
        setLoading(false);
        return;
      }

      setDetectionResult(response.data);
      setShowMeme(true);
    } catch (error) {
      console.error('Error detecting gesture:', error);
      alert('Error detecting gesture. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setCapturedImage(null);
    setDetectionResult(null);
    setShowMeme(false);
  };

  const gestures = [
    { name: 'Thumbs Up', description: 'Acungkan jempol ke atas' },
    { name: 'Pointing', description: 'Tunjuk dengan jari telunjuk' },
    { name: 'Touching Head', description: 'Sentuh kepala dengan tangan' }
  ];

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#F1F3E0' }}>
      {/* Header */}
      <header className="py-8 px-4 border-b" style={{ borderColor: '#D2DCB6' }}>
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-semibold" style={{ color: '#778873' }}>
            Gesture Detector
          </h1>
          <p className="mt-2" style={{ color: '#636e72' }}>
            Deteksi gesture tangan menggunakan AI
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Webcam Section */}
          <div className="rounded-lg border p-6" style={{ backgroundColor: 'white', borderColor: '#D2DCB6' }}>
            <h2 className="text-xl font-medium mb-4" style={{ color: '#778873' }}>
              Kamera
            </h2>
            <div className="relative aspect-video bg-gray-100 rounded-lg overflow-hidden border" style={{ borderColor: '#D2DCB6' }}>
              {!capturedImage ? (
                <Webcam
                  ref={webcamRef}
                  screenshotFormat="image/jpeg"
                  className="w-full h-full object-cover"
                  mirrored={true}
                />
              ) : (
                <img
                  src={capturedImage}
                  alt="Captured"
                  className="w-full h-full object-cover"
                />
              )}
            </div>

            <div className="mt-4 flex gap-3">
              {!capturedImage ? (
                <button
                  onClick={captureImage}
                  className="flex-1 font-medium py-2.5 px-4 rounded-md transition-colors"
                  style={{
                    backgroundColor: '#A1BC98',
                    color: 'white',
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = '#8aab83'}
                  onMouseLeave={(e) => e.target.style.backgroundColor = '#A1BC98'}
                >
                  Ambil Foto
                </button>
              ) : (
                <>
                  <button
                    onClick={detectGesture}
                    disabled={loading}
                    className="flex-1 font-medium py-2.5 px-4 rounded-md transition-colors disabled:opacity-50"
                    style={{
                      backgroundColor: '#778873',
                      color: 'white',
                    }}
                    onMouseEnter={(e) => !loading && (e.target.style.backgroundColor = '#626f5e')}
                    onMouseLeave={(e) => e.target.style.backgroundColor = '#778873'}
                  >
                    {loading ? 'Mendeteksi...' : 'Deteksi Gesture'}
                  </button>
                  <button
                    onClick={reset}
                    className="flex-1 font-medium py-2.5 px-4 rounded-md border transition-colors"
                    style={{
                      borderColor: '#D2DCB6',
                      color: '#778873',
                      backgroundColor: 'white'
                    }}
                    onMouseEnter={(e) => e.target.style.backgroundColor = '#F1F3E0'}
                    onMouseLeave={(e) => e.target.style.backgroundColor = 'white'}
                  >
                    Reset
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Result Section */}
          <div className="rounded-lg border p-6" style={{ backgroundColor: 'white', borderColor: '#D2DCB6' }}>
            <h2 className="text-xl font-medium mb-4" style={{ color: '#778873' }}>
              Hasil Deteksi
            </h2>

            {!detectionResult ? (
              <div className="flex items-center justify-center h-64" style={{ color: '#636e72' }}>
                <div className="text-center">
                  <p>Ambil foto dan deteksi gesture untuk melihat hasil</p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="rounded-md p-4" style={{ backgroundColor: '#F1F3E0' }}>
                  <p className="text-sm mb-1" style={{ color: '#636e72' }}>Gesture Terdeteksi:</p>
                  <p className="text-2xl font-semibold capitalize" style={{ color: '#778873' }}>
                    {detectionResult.gesture.replace('_', ' ')}
                  </p>
                </div>

                <div className="rounded-md p-4" style={{ backgroundColor: '#F1F3E0' }}>
                  <p className="text-sm mb-2" style={{ color: '#636e72' }}>Confidence:</p>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 rounded-full h-2 overflow-hidden" style={{ backgroundColor: '#D2DCB6' }}>
                      <div
                        className="h-full transition-all duration-500"
                        style={{
                          width: `${detectionResult.confidence * 100}%`,
                          backgroundColor: '#A1BC98'
                        }}
                      />
                    </div>
                    <span className="text-lg font-semibold" style={{ color: '#778873' }}>
                      {(detectionResult.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>

                {showMeme && detectionResult.meme && (
                  <div className="rounded-md p-4" style={{ backgroundColor: '#F1F3E0' }}>
                    <p className="text-sm mb-3" style={{ color: '#636e72' }}>Meme Reaksi:</p>
                    <div className="rounded-md overflow-hidden border" style={{ borderColor: '#D2DCB6' }}>
                      <img
                        src={`/assets/${detectionResult.meme}`}
                        alt={detectionResult.gesture}
                        className="w-full"
                        onError={(e) => {
                          e.target.style.display = 'none';
                        }}
                      />
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Gesture Info */}
        <div className="mt-8 rounded-lg border p-6" style={{ backgroundColor: 'white', borderColor: '#D2DCB6' }}>
          <h3 className="text-xl font-medium mb-4" style={{ color: '#778873' }}>
            Gesture yang Didukung
          </h3>
          <div className="grid md:grid-cols-3 gap-4">
            {gestures.map((gesture, index) => (
              <div
                key={index}
                className="rounded-md p-4 border"
                style={{
                  backgroundColor: '#F1F3E0',
                  borderColor: '#D2DCB6'
                }}
              >
                <h4 className="font-medium mb-1" style={{ color: '#778873' }}>
                  {gesture.name}
                </h4>
                <p className="text-sm" style={{ color: '#636e72' }}>
                  {gesture.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-6 rounded-lg border p-6" style={{ backgroundColor: 'white', borderColor: '#D2DCB6' }}>
          <h3 className="text-xl font-medium mb-4" style={{ color: '#778873' }}>
            Cara Penggunaan
          </h3>
          <ol className="space-y-2" style={{ color: '#636e72' }}>
            <li className="flex gap-3">
              <span className="font-semibold" style={{ color: '#778873' }}>1.</span>
              <span>Klik tombol "Ambil Foto" untuk mengambil gambar dari webcam</span>
            </li>
            <li className="flex gap-3">
              <span className="font-semibold" style={{ color: '#778873' }}>2.</span>
              <span>Klik "Deteksi Gesture" untuk menganalisis gesture tangan Anda</span>
            </li>
            <li className="flex gap-3">
              <span className="font-semibold" style={{ color: '#778873' }}>3.</span>
              <span>Lihat hasil deteksi dan meme reaksi yang sesuai</span>
            </li>
          </ol>
        </div>
      </main>
    </div>
  );
}

export default App;
