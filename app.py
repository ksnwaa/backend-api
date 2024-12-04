from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from model import predict_image
from utils import allowed_file

app = Flask(__name__)

# Inisialisasi Firestore client
db = firestore.Client()

# Fungsi untuk mengambil riwayat prediksi dari Firestore
def get_prediction_histories():
    histories_ref = db.collection('predictions')  # Nama koleksi yang menyimpan data prediksi
    docs = histories_ref.stream()

    histories = []
    for doc in docs:
        data = doc.to_dict()
        histories.append({
            "id": doc.id,
            "history": {
                "result": data['result'],
                "createdAt": data['createdAt'],
                "suggestion": data['suggestion'],
                "id": doc.id
            }
        })

    return histories

# Tambahkan endpoint untuk mengambil riwayat prediksi
@app.route('/predict/histories', methods=['GET'])
def predict_histories():
    try:
        histories = get_prediction_histories()

        return jsonify({
            "status": "success",
            "data": histories
        })
    except Exception as e:
        return jsonify({
            "status": "fail",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500

# Konfigurasi file upload
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB
def save_prediction_to_firestore(result, suggestion):
    prediction_ref = db.collection('predictions').document()
    prediction_ref.set({
        'result': result,
        'suggestion': suggestion,
        'createdAt': datetime.utcnow().isoformat() + "Z"
    })


@app.route('/predict', methods=['POST'])
def predict():
    # Pastikan file gambar ada dalam request
    if 'image' not in request.files:
        return jsonify({
            "status": "fail",
            "message": "No image file in request"
        }), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({
            "status": "fail",
            "message": "No image file selected"
        }), 400

    # Cek apakah file sesuai dengan ekstensi yang diizinkan
    if not allowed_file(file.filename):
        return jsonify({
            "status": "fail",
            "message": "Invalid file type"
        }), 400

    try:
        # Simpan file gambar
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Lakukan prediksi dengan model
        prediction = predict_image(filepath)

        # Hasil prediksi
        result = {
            "id": str(uuid.uuid4()),
            "result": prediction['result'],
            "suggestion": prediction['suggestion'],
            "createdAt": datetime.utcnow().isoformat() + "Z"
        }

        return jsonify({
            "status": "success",
            "message": "Model is predicted successfully",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "fail",
            "message": "Terjadi kesalahan dalam melakukan prediksi"
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
