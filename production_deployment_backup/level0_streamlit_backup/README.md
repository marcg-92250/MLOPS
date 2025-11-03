# Level 0: Streamlit App

Interactive web application for house price prediction using Streamlit.

## 📋 Steps

### 1. Download Files

Files already provided:
- ✅ `train_model.py` - Model training script
- ✅ `data/houses.csv` - Dataset

### 2. Train the Model

```bash
cd /home/gma/MLOPS/production_deployment
python train_model.py
```

This generates `models/regression.joblib`.

### 3. Create Streamlit App

✅ Created `model_app.py` with:
- Streamlit and joblib imports
- Model loading with `joblib.load()`
- Three input fields using `st.number_input()` and `st.selectbox()`
- Prediction using `model.predict()`
- Results display with `st.write()`

### 4. Run the App

```bash
cd level0_streamlit
streamlit run model_app.py
```

Access at: http://localhost:8501

## 🎯 Features

- **Interactive Form**: Easy input for house details
- **Real-time Prediction**: Instant price estimation
- **Model Insights**: Shows feature importance
- **Clean UI**: Professional Streamlit interface

## 📸 Usage

1. Enter house size (m²)
2. Enter number of bedrooms
3. Select if house has a garden
4. Click "Predict Price"
5. View estimated price

## 🔧 Customization

Edit `model_app.py` to:
- Change input ranges
- Add more features
- Modify the UI layout
- Add visualizations

## 📊 Example Predictions

| Size | Bedrooms | Garden | Predicted Price |
|------|----------|--------|-----------------|
| 100  | 3        | Yes    | ~$250,000       |
| 150  | 4        | Yes    | ~$380,000       |
| 50   | 1        | No     | ~$150,000       |

## 🚀 Next Level

Proceed to **Level 1** to create a FastAPI REST API for the same model.

## 💡 Tips

- The model loads once and is cached
- Input validation prevents invalid entries
- Sidebar provides additional information
- Responsive design works on mobile

## 🐛 Troubleshooting

**Model not found?**
```bash
# Make sure you're in the right directory
cd /home/gma/MLOPS/production_deployment
python train_model.py
```

**Streamlit not installed?**
```bash
pip install streamlit
```

**Port already in use?**
```bash
streamlit run model_app.py --server.port 8502
```

