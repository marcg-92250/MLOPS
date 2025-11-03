#!/usr/bin/env python3
"""
Level 0: Streamlit App for House Price Prediction
"""

import streamlit as st
import joblib
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

# Load model
@st.cache_resource
def load_model():
    """Load the trained model"""
    model_path = '../models/regression.joblib'
    if not os.path.exists(model_path):
        st.error(f"Model not found at {model_path}")
        st.info("Please run train_model.py first to generate the model")
        st.stop()
    return joblib.load(model_path)

# Main app
def main():
    st.title("🏠 House Price Prediction App")
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to the House Price Predictor!
    
    This app uses a machine learning model to predict house prices based on:
    - **Size** (in m²)
    - **Number of bedrooms**
    - **Garden** (yes/no)
    """)
    
    st.markdown("---")
    
    # Load the model
    try:
        model = load_model()
        st.success("✓ Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return
    
    st.markdown("### Enter House Details")
    
    # Create input form
    col1, col2 = st.columns(2)
    
    with col1:
        size = st.number_input(
            "Size (m²)",
            min_value=20,
            max_value=500,
            value=100,
            step=5,
            help="Enter the size of the house in square meters"
        )
        
        bedrooms = st.number_input(
            "Number of Bedrooms",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Enter the number of bedrooms"
        )
    
    with col2:
        garden = st.selectbox(
            "Has Garden?",
            options=[("No", 0), ("Yes", 1)],
            format_func=lambda x: x[0],
            help="Does the house have a garden?"
        )
        garden_value = garden[1]
        
        # Show input summary
        st.markdown("#### Input Summary")
        st.info(f"""
        - Size: **{size} m²**
        - Bedrooms: **{bedrooms}**
        - Garden: **{garden[0]}**
        """)
    
    st.markdown("---")
    
    # Prediction button
    if st.button("🔮 Predict Price", type="primary", use_container_width=True):
        # Prepare input
        features = np.array([[size, bedrooms, garden_value]])
        
        # Make prediction
        try:
            prediction = model.predict(features)[0]
            
            # Display result
            st.markdown("### Prediction Result")
            st.success(f"### Estimated Price: **${prediction:,.2f}**")
            
            # Show feature importance (coefficients)
            st.markdown("---")
            st.markdown("#### Model Insights")
            
            col1, col2, col3 = st.columns(3)
            
            coefs = model.coef_
            with col1:
                st.metric("Size Impact", f"${coefs[0]:.2f}/m²")
            with col2:
                st.metric("Bedroom Impact", f"${coefs[1]:,.2f}")
            with col3:
                st.metric("Garden Impact", f"${coefs[2]:,.2f}")
            
            st.caption(f"Baseline price: ${model.intercept_:,.2f}")
            
        except Exception as e:
            st.error(f"Prediction error: {e}")
    
    # Sidebar information
    with st.sidebar:
        st.markdown("## About")
        st.info("""
        This is a demo application for Level 0 of the 
        Model Deployment project.
        
        **Model**: Linear Regression  
        **Dataset**: House Prices
        
        **Next Steps:**
        - Level 1: FastAPI REST API
        - Level 2: Docker Container
        - Level 3: Cloud Deployment
        - Level 4: CI/CD Pipeline
        """)
        
        st.markdown("---")
        st.markdown("### How it works")
        st.markdown("""
        1. Enter house details
        2. Click 'Predict Price'
        3. Get instant prediction
        
        The model uses linear regression to estimate 
        the price based on the input features.
        """)

if __name__ == "__main__":
    main()

