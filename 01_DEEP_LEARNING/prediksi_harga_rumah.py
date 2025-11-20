import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.datasets import fetch_california_housing 


# FUNGSI UTAMA DAN UNTUK PELATIHAN EKSEKUSI
def run_deep_learning_model():
    print("--- 2. Memuat dan Memeriksa Dataset California Housing ---")
    
    try:
        housing = fetch_california_housing(as_frame=True)
        df = housing.frame
        df['PRICE'] = housing.target * 100000 
    except Exception as e:
        print(f"Error saat memuat dataset California Housing: {e}")
        return # Hentikan eksekusi jika gagal memuat data
    
    # menammpilkan 5 baris pertama dari dataset 
    print(df.head())
    print(f"\nJumlah Baris Data: {len(df)}")
    
    # preprocessing data
    # pemisahan fitu (X) dengan target (Y)
    X = df.drop('PRICE', axis=1)
    y = df['PRICE']
    
    # Scaling data (Standarisasi)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print(f"\nFitur Berhasil di Standarisasi")
    
    # Splitting Data (Learning 80%, Testing 20%)
    X_train,X_test, y_train_val , y_test = train_test_split(X_scaled,y, test_size=0.2, random_state=42)
    
    # bagi train dan validation menjadi 75% dan 25%
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train_val, test_size=0.25, random_state=42)
    
    print(f"Data Training: {len(X_train)}, Validation: {len(X_val)}, Testing: {len(X_test)}")
    
    # membuat model Jaringan saraf tiruan
    print(f"======== MEMBUAT MODEL JARINGAN SARAF TIRUAN ========")
    model = Sequential([
        # layer input: Jumlah neuron disesuaikan otomatis dengan jumlah fitur baru
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        # layer tersembunyi (Hiden layer)
        Dense(32, activation='relu'),
        # layer output
        Dense(1)
    ])
    
    
    # Kompilasi Model: Menentukan fungsi kerugian dan optimizer
    # 'mean_squared_error' (MSE) adalah fungsi kerugian umum untuk regresi
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    model.summary()
    
    
    # early stopping
    # Ini adalah kunci untuk menghentikan epoch secara otomatis
    # pantau 'val_loss' (Loss pada data Validasi)
    # 'patience=10' berarti jika val_loss tidak membaik setelah 10 epoch, pelatihan akan dihentikan   
    early_stoping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    ) 
    
    # Pelatihan model 
    print(f"\n--- Pelatihan dimulai dengan EarlyStoping ---")
    history = model.fit(
        X_train,
        y_train,
        epochs = 300,
        batch_size=32,
        validation_data=(X_val, y_val),
        callbacks=[early_stoping],
        verbose=1
    )
    
    # Evaluasi model Akhir
    print(f"\n--- Evaluasi model pada data testing ---")
    loss, mae = model.evaluate(X_test,y_test, verbose=1)
    print(f"Mean Squared Error (MSE) pada Test Set: {loss:.2f}")
    print(f"Mean Absolute Error (MAE) pada Test Set: {mae:.2f} USD")
    
    # 8. VISUALISASI HASIL EPOCH
    plt.figure(figsize=(12, 6))
    plt.plot(history.history['loss'], label='Training Loss (Kerugian Pelatihan)')
    plt.plot(history.history['val_loss'], label='Validation Loss (Kerugian Validasi)')
    plt.title('Kurva Kerugian (Loss) Model Deep Learning')
    plt.xlabel('Epochs')
    plt.ylabel('Loss (MSE)')
    plt.legend()
    plt.show()
    
    # 9. PENGUJIAN PREDIKSI BARU
    print("\n--- 9. Contoh Prediksi Rumah Baru ---")
    # Ambil 5 data pertama dari X_test (sudah di-scale)
    contoh_data_baru_scaled = X_test[:5]
    y_aktual = y_test[:5]
    
    # Lakukan prediksi
    y_pred_new = model.predict(contoh_data_baru_scaled).flatten()
    
    # Tampilkan hasilnya
    hasil_prediksi = pd.DataFrame({
        'Harga Aktual': y_aktual,
        'Harga Prediksi': y_pred_new.round(2)
    })
    
    print(hasil_prediksi)
    
run_deep_learning_model()