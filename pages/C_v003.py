import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Set page configuration
st.set_page_config(page_title="Customer Turnover Forecasting", page_icon="📊", layout="wide")

# Load sample data (replace this with your actual data loading logic)
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'customer_id': range(1000),
        'age': np.random.randint(18, 80, 1000),
        'tenure': np.random.randint(0, 10, 1000),
        'balance': np.random.uniform(0, 250000, 1000),
        'num_products': np.random.randint(1, 5, 1000),
        'credit_score': np.random.randint(300, 850, 1000),
        'is_active_member': np.random.choice([0, 1], 1000),
        'estimated_salary': np.random.uniform(30000, 200000, 1000),
        'churn': np.random.choice([0, 1], 1000, p=[0.8, 0.2])  # 20% churn rate
    })
    data['age_group'] = pd.cut(data['age'], bins=[0, 30, 40, 50, 60, 100], labels=['18-30', '31-40', '41-50', '51-60', '60+'])
    return data

# Train model function
@st.cache_resource
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model, X_test, y_test

# Main function
def main():
    st.title("📊 Customer Turnover Forecasting")
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Prediction Model", "Customer Analysis"])

    # Load data
    data = load_data()

    if page == "Dashboard":
        st.header("Customer Turnover Dashboard")
        
        # Key Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Customers", len(data))
        col2.metric("Churn Rate", f"{data['churn'].mean():.2%}")
        col3.metric("Avg. Customer Tenure", f"{data['tenure'].mean():.1f} years")

        # Churn by Age Group
        st.subheader("Churn by Age Group")
        data['age_group'] = pd.cut(data['age'], bins=[0, 30, 40, 50, 60, 100], labels=['18-30', '31-40', '41-50', '51-60', '60+'])
        churn_by_age = data.groupby('age_group')['churn'].mean().reset_index()
        fig = px.bar(churn_by_age, x='age_group', y='churn', title='Churn Rate by Age Group')
        st.plotly_chart(fig)

        # Correlation Heatmap
        st.subheader("Feature Correlation")
        corr = data.drop(['customer_id', 'churn', 'age_group'], axis=1).corr()
        fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap")
        st.plotly_chart(fig)

    elif page == "Prediction Model":
        st.header("Customer Churn Prediction Model")
        
        # Train model
        st.write("Columns in data:", data.columns.tolist())
        #X = data.drop(['customer_id', 'churn', 'age_group'], axis=1)
        X = data.drop(['customer_id', 'churn', 'age_group'], axis=1, errors='ignore')
        y = data['churn']
        model, X_test, y_test = train_model(X, y)

        # Model Performance
        st.subheader("Model Performance")
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        st.write(f"Model Accuracy: {accuracy:.2%}")

        # Feature Importance
        st.subheader("Feature Importance")
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        fig = px.bar(feature_importance, x='feature', y='importance', title='Feature Importance')
        st.plotly_chart(fig)

        # Prediction Interface
        st.subheader("Churn Prediction")
        st.write("Enter customer details to predict churn probability:")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            tenure = st.number_input("Tenure (years)", min_value=0, max_value=50, value=5)
            balance = st.number_input("Account Balance", min_value=0, max_value=1000000, value=50000)
            num_products = st.number_input("Number of Products", min_value=1, max_value=4, value=1)
        with col2:
            credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=700)
            is_active_member = st.selectbox("Active Member", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            estimated_salary = st.number_input("Estimated Salary", min_value=10000, max_value=1000000, value=50000)

        if st.button("Predict Churn"):
            input_data = np.array([[age, tenure, balance, num_products, credit_score, is_active_member, estimated_salary]])
            prediction = model.predict_proba(input_data)[0]
            st.write(f"Churn Probability: {prediction[1]:.2%}")
            if prediction[1] > 0.5:
                st.warning("This customer is at high risk of churning. Consider intervention strategies.")
            else:
                st.success("This customer is likely to remain. Continue providing excellent service.")

    elif page == "Customer Analysis":
        st.header("Customer Analysis")

        # Customer Segmentation
        st.subheader("Customer Segmentation")
        segment = pd.cut(data['estimated_salary'], bins=3, labels=['Low', 'Medium', 'High'])
        fig = px.scatter(data, x='tenure', y='balance', color=segment, hover_data=['age', 'credit_score'],
                         title='Customer Segmentation by Tenure and Balance')
        st.plotly_chart(fig)

        # Churn Reasons Analysis (hypothetical)
        st.subheader("Top Reasons for Churn")
        churn_reasons = pd.DataFrame({
            'Reason': ['Poor Customer Service', 'High Fees', 'Competitor Offers', 'Life Changes', 'Product Dissatisfaction'],
            'Percentage': [30, 25, 20, 15, 10]
        })
        fig = px.pie(churn_reasons, values='Percentage', names='Reason', title='Top Reasons for Customer Churn')
        st.plotly_chart(fig)

        # Customer Lifetime Value
        st.subheader("Customer Lifetime Value (CLV) Distribution")
        data['clv'] = data['balance'] * data['tenure'] * (1 - data['churn'])  # Simplified CLV calculation
        fig = px.histogram(data, x='clv', nbins=50, title='Distribution of Customer Lifetime Value')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
