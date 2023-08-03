import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

st.title('Interactive KMeans Clustering')

# Load data
@st.cache
def load_data():
    dataset = pd.read_csv('DATASETS/Mall_Customers.csv')
    return dataset

dataset = load_data()

# Select features
X = dataset.iloc[:, [2, 3, 4]].values

# Select number of clusters
num_clusters = st.sidebar.slider('Select number of clusters', 2, 10, 5)

# Build Model
kmeansmodel = KMeans(n_clusters=num_clusters, init='k-means++', random_state=0, n_init=10)
y_kmeans = kmeansmodel.fit_predict(X)

# Visualization
st.subheader('Cluster Visualization')

df = pd.DataFrame(X, columns=['Age', 'Annual_Income', 'Spending_Score'])
df['cluster'] = y_kmeans

# Input for test data
st.subheader('Test Data')
age = st.number_input('Age', min_value=1)
annual_income = st.number_input('Annual Income', min_value=1)
spending_score = st.number_input('Spending Score', min_value=1)

# Button to add test data
if st.button('Add Test Data'):
    test_data = np.array([age, annual_income, spending_score])
    X_test = np.append(X, [test_data], axis=0)
    y_kmeans = kmeansmodel.fit_predict(X_test)

    # Add the test data to the dataframe for visualization
    test_df = pd.DataFrame([test_data], columns=['Age', 'Annual_Income', 'Spending_Score'])
    test_df['cluster'] = y_kmeans[-1]  # assign the predicted cluster of the test data
    df = pd.concat([df, test_df])

    # Use a color scale that provides more colors
    fig = px.scatter_3d(df, x='Age', y='Annual_Income', z='Spending_Score', color='cluster', color_continuous_scale=px.colors.sequential.Plasma, color_discrete_map={y_kmeans[-1]: 'red'})

    fig.update_layout(height=1000, width=1000)

    # Show plot in streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    # Show the initial plot without the test data
    fig = px.scatter_3d(df, x='Age', y='Annual_Income', z='Spending_Score', color='cluster', color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(height=1000, width=1000)
    st.plotly_chart(fig, use_container_width=True)
