from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load model yang sudah dilatih
model = load_model('model_cancer.h5')  # pastikan Anda punya model .h5 yang sudah dilatih

def predict_image(filepath):
    img = image.load_img(filepath, target_size=(224, 224))  # Sesuaikan dengan ukuran input model Anda
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Ubah menjadi batch size 1

    # Normalisasi gambar jika diperlukan
    img_array = img_array / 255.0

    # Prediksi
    prediction = model.predict(img_array)

    # Tentukan hasil prediksi (misalnya: 0 = Non-cancer, 1 = Cancer)
    if prediction[0] > 0.5:
        return {"result": "Cancer", "suggestion": "Segera periksa ke dokter!"}
    else:
        return {"result": "Non-cancer", "suggestion": "Penyakit kanker tidak terdeteksi."}
