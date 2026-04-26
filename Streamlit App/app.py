import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.set_page_config(
    page_title="Hospital Readmission Prediction",
    page_icon="🏥",
    # Make the content take up the width of the page:
    layout="wide",
)

df = pd.read_csv("patient_data.csv")
df['readmitted'] = df['readmitted'].replace({
        '<30': 1,
        '>30': 0,
        'NO': 0
    })

st.title("**:blue[Hospital Readmission Prediction]**")
# , text_alignment = "center"
# st.write(" ")
# st.header(":green[Objective]")
st.markdown(

    """
    
    """
)

# fig = px.bar(df["age"].value_counts().reset_index().sort_values(by="age"), x="age", y="count", title="Patient Age Distribution")
# fig.update_layout(xaxis_title="Age Group",
#                   yaxis_title="Count")

# st.plotly_chart(fig, width="stretch")

# fig = px.histogram(df, x="gender", title="Patient Gender Distribution")
# fig.update_layout(xaxis_title="Gender",
#                   yaxis_title="Count")

# st.plotly_chart(fig, width="stretch")


# fig = px.bar(df["admission_type_id"].value_counts().reset_index(),
#              x="admission_type_id",
#              y="count",
#              title="Patient Admission Type Distribution")

# fig.update_layout(xaxis_title="Admission Type",
#                   yaxis_title="Count")


# st.plotly_chart(fig, width="stretch")


# fig = px.bar(df["readmitted"].value_counts().reset_index(),
#              x="readmitted",
#              y="count",
#              title="Patient Readmission Distribution")
# fig.update_layout(xaxis_title="Readmission",
#                   yaxis_title="Count")

# st.plotly_chart(fig, width="stretch")

st.markdown("""
<style>
div[data-testid="stMetric"] {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

colm1, colm2, colm3 = st.columns(3)

# Total number of patients in filtered data
colm1.metric("Total Patients", len(df))

# Number of patients readmitted
colm2.metric("Readmitted Patients", int(df['readmitted'].sum()))

# Percentage of patients readmitted
colm3.metric("Readmission Rate", f"{df['readmitted'].mean()*100:.2f}%")

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df["age"].value_counts().reset_index().sort_values(by="age"),
        x="age",
        y="count",
        title="Patient Age Distribution"
    )
    fig.update_layout(xaxis_title="Age Group", yaxis_title="Count")
    st.plotly_chart(fig)

with col2:
    fig = px.histogram(df, x="gender", title="Patient Gender Distribution")
    fig.update_layout(xaxis_title="Gender", yaxis_title="Count")
    st.plotly_chart(fig)



col3, col4 = st.columns(2)

with col3:
    fig = px.bar(
        df["admission_type_id"].value_counts().reset_index(),
        x="admission_type_id",
        y="count",
        title="Patient Admission Type Distribution"
    )
    fig.update_layout(xaxis_title="Admission Type", yaxis_title="Count")
    st.plotly_chart(fig)

with col4:
    fig = px.bar(
        df["readmitted"].value_counts().reset_index(),
        x="readmitted",
        y="count",
        title="Patient Readmission Distribution"
    )
    fig.update_layout(xaxis_title="Readmission", yaxis_title="Count")
    st.plotly_chart(fig)

