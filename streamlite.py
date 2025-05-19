import streamlit as st
import pandas as pd
from qdrant_client import QdrantClient

client = QdrantClient(
    url="https://388b072d-469a-4562-ba61-201e1ec27fd0.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.vXaJ5sSyA1gsOfoKYEIOsDV2pn2kERPtFMK-t7VNy3c",
)

# Scroll all reviews with features
points, _ = client.scroll("mbank.csv", with_payload=True, limit=10000)

# Convert to DataFrame
df = pd.DataFrame([{"id": p.id, **p.payload} for p in points])
df = df.explode("features")

# Bar chart of feature frequency
feature_counts = df["features"].value_counts()
st.bar_chart(feature_counts)

# Filter and view reviews
selected_feature = st.selectbox("Select feature", feature_counts.index)
st.dataframe(df[df["features"] == selected_feature][["text", "score"]])