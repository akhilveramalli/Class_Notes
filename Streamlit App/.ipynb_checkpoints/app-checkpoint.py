import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Patient Readmission App",
    page_icon="🏥",
    layout="wide"
)

# =============================================================================
# LOAD AND PREPARE DATA  (cached so it only runs once)
# =============================================================================

@st.cache_data
def load_and_prepare_data():

    df = pd.read_csv("patient_data.csv")

    # ── drop high-missing columns ─────────────────────────────────────────────
    df = df.drop(columns=["A1Cresult", "max_glu_serum"])

    # ── drop admin id columns ────────────────────────────────────────────────
    df = df.drop(columns=["admission_type_id",
                           "discharge_disposition_id",
                           "admission_source_id"])

    # ── fill race nulls ───────────────────────────────────────────────────────
    df["race"] = df["race"].fillna(df["race"].mode()[0])

    # ── remove unknown gender ────────────────────────────────────────────────
    df = df[df["gender"] != "Unknown/Invalid"]

    # ── encode age ───────────────────────────────────────────────────────────
    age_map = {
        "[0-10)": 0, "[10-20)": 10, "[20-30)": 20, "[30-40)": 30,
        "[40-50)": 40, "[50-60)": 50, "[60-70)": 60, "[70-80)": 70,
        "[80-90)": 80, "[90-100)": 90
    }
    df["age_numeric"] = df["age"].map(age_map)

    # ── encode insulin ───────────────────────────────────────────────────────
    df["insulin_numeric"] = df["insulin"].map(
        {"No": 0, "Down": 1, "Steady": 2, "Up": 3}
    )

    # ── binary encode yes/no columns ─────────────────────────────────────────
    df["diabetesMed"] = df["diabetesMed"].map({"Yes": 1, "No": 0})
    df["change"]      = df["change"].map({"Ch": 1, "No": 0})
    df["gender_num"]  = df["gender"].map({"Male": 1, "Female": 0})

    # ── medication count ─────────────────────────────────────────────────────
    med_cols = ["metformin", "glipizide", "glyburide",
                "pioglitazone", "rosiglitazone"]
    df["total_meds_active"] = 0
    for col in med_cols:
        df["total_meds_active"] += (df[col] != "No").astype(int)
    df = df.drop(columns=med_cols)

    # ── service intensity ────────────────────────────────────────────────────
    df["service_intensity"] = (df["time_in_hospital"] +
                                df["number_inpatient"]  +
                                df["number_outpatient"] +
                                df["number_emergency"])

    # ── one-hot race ──────────────────────────────────────────────────────────
    df = pd.get_dummies(df, columns=["race"], drop_first=True)

    # ── binary target ─────────────────────────────────────────────────────────
    df["readmitted_binary"] = (df["readmitted"] == "<30").astype(int)

    return df


@st.cache_resource
def train_model(df):

    feature_cols = [
        "time_in_hospital", "num_lab_procedures", "num_procedures",
        "num_medications", "number_outpatient", "number_emergency",
        "number_inpatient", "number_diagnoses", "gender_num",
        "diabetesMed", "change", "age_numeric", "total_meds_active",
        "insulin_numeric", "service_intensity"
    ]
    # add race dummies that exist in df
    race_cols = [c for c in df.columns if c.startswith("race_")]
    feature_cols += race_cols

    X = df[feature_cols]
    y = df["readmitted_binary"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_sc, y_train)

    return model, scaler, feature_cols


# =============================================================================
# LOAD DATA AND MODEL
# =============================================================================

df = load_and_prepare_data()
model, scaler, feature_cols = train_model(df)

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================

# st.sidebar.image(
#     "https://img.icons8.com/ios-filled/100/4A90D9/hospital.png",
#     width=60
# )
st.sidebar.title("Patient Readmission")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Go to",
    ["Data Dashboard", "Predict Readmission"]
)

st.sidebar.markdown("---")
# st.sidebar.markdown(
#     f"**Dataset:** {len(df):,} patients  \n"
#     f"**Features:** {len(feature_cols)}  \n"
#     f"**Model:** Random Forest  \n"
#     f"**Positive class:** {df['readmitted_binary'].mean()*100:.1f}%"
# )


# =============================================================================
# PAGE 1 : DATA DASHBOARD
# =============================================================================

if page == "Data Dashboard":

    st.title("🏥 Patient Readmission — Data Dashboard")
    st.markdown("Explore the diabetic patient dataset used to train the readmission prediction model.")
    st.markdown("---")

    # ── Row 1 : KPI cards ────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Patients",    f"{len(df):,}")
    col2.metric("Readmitted < 30d",  f"{df['readmitted_binary'].sum():,}")
    col3.metric("Not Readmitted",    f"{(df['readmitted_binary']==0).sum():,}")
    col4.metric("Positive Rate",     f"{df['readmitted_binary'].mean()*100:.1f}%")

    st.markdown("---")

    # ── Row 2 : Target distribution + Gender breakdown ────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Readmission class distribution")

        target_counts = df["readmitted"].value_counts().reset_index()
        target_counts.columns = ["Class", "Count"]

        fig1 = px.pie(
            target_counts,
            names="Class",
            values="Count",
            color_discrete_sequence=["#4CAF50", "#FF9800", "#F44336"],
            hole=0.45
        )
        fig1.update_traces(textposition="outside", textinfo="percent+label")
        fig1.update_layout(
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            height=340
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        # st.subheader("Readmission by gender")

        # gender_read = df.groupby("gender")["readmitted_binary"].mean().reset_index()
        # gender_read.columns = ["Gender", "Readmission Rate"]
        # gender_read["Gender"] = gender_read["Gender"].map({1: "Male", 0: "Female"})
        # gender_read["Readmission Rate %"] = (gender_read["Readmission Rate"] * 100).round(2)

        # fig2 = px.bar(
        #     gender_read,
        #     x="Gender",
        #     y="Readmission Rate %",
        #     color="Gender",
        #     color_discrete_sequence=["#378ADD", "#D4537E"],
        #     text="Readmission Rate %"
        # )
        # fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        # fig2.update_layout(
        #     showlegend=False,
        #     yaxis_title="Readmission Rate (%)",
        #     margin=dict(t=20, b=20, l=20, r=20),
        #     height=340
        # )
        # st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Readmission rate by race")

        # reconstruct race from dummy columns
        race_dummies = [c for c in df.columns if c.startswith("race_")]
        race_map_df = df[race_dummies + ["readmitted_binary"]].copy()

        race_rates = {}
        for col in race_dummies:
            race_name = col.replace("race_", "")
            mask = race_map_df[col] == 1
            if mask.sum() > 0:
                race_rates[race_name] = race_map_df.loc[mask, "readmitted_binary"].mean() * 100

        # the baseline race (dropped in get_dummies) is AfricanAmerican
        base_mask = (race_map_df[race_dummies] == 0).all(axis=1)
        race_rates["AfricanAmerican"] = race_map_df.loc[base_mask, "readmitted_binary"].mean() * 100

        race_df = pd.DataFrame(list(race_rates.items()), columns=["Race", "Rate %"])
        race_df = race_df.sort_values("Rate %", ascending=True)

        fig5 = px.bar(
            race_df,
            x="Rate %",
            y="Race",
            orientation="h",
            color="Rate %",
            color_continuous_scale="Teal",
            text="Rate %"
        )
        fig5.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig5.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Readmission Rate (%)",
            margin=dict(t=20, b=20, l=20, r=20),
            height=340
        )
        st.plotly_chart(fig5, use_container_width=True)

        

    # ── Row 3 : Age distribution + Time in hospital ───────────────────────────
    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Readmission rate by age group")

        age_labels = {
            0: "0-10", 10: "10-20", 20: "20-30", 30: "30-40",
            40: "40-50", 50: "50-60", 60: "60-70", 70: "70-80",
            80: "80-90", 90: "90-100"
        }
        age_df = df.copy()
        age_df["Age Group"] = age_df["age_numeric"].map(age_labels)
        age_read = age_df.groupby("Age Group")["readmitted_binary"].mean().reset_index()
        age_read.columns = ["Age Group", "Rate"]
        age_read["Rate %"] = (age_read["Rate"] * 100).round(2)

        age_order = ["0-10","10-20","20-30","30-40","40-50",
                     "50-60","60-70","70-80","80-90","90-100"]
        age_read["Age Group"] = pd.Categorical(age_read["Age Group"],
                                               categories=age_order, ordered=True)
        age_read = age_read.sort_values("Age Group")

        fig3 = px.bar(
            age_read,
            x="Age Group",
            y="Rate %",
            color="Rate %",
            color_continuous_scale="Blues",
            text="Rate %"
        )
        fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig3.update_layout(
            coloraxis_showscale=False,
            yaxis_title="Readmission Rate (%)",
            margin=dict(t=20, b=20, l=20, r=20),
            height=340
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        # st.subheader("Time in hospital distribution")

        # fig4 = px.histogram(
        #     df,
        #     x="time_in_hospital",
        #     color="readmitted_binary",
        #     barmode="overlay",
        #     nbins=14,
        #     labels={"readmitted_binary": "Readmitted < 30d",
        #             "time_in_hospital": "Days in Hospital"},
        #     color_discrete_map={0: "#4CAF50", 1: "#F44336"}
        # )
        # fig4.update_layout(
        #     yaxis_title="Number of Patients",
        #     margin=dict(t=20, b=20, l=20, r=20),
        #     height=340,
        #     legend=dict(title="Readmitted <30d", x=0.75, y=0.95)
        # )
        # st.plotly_chart(fig4, use_container_width=True)
        st.subheader("Number of medications vs readmission")

        med_read = df.groupby("num_medications")["readmitted_binary"].mean().reset_index()
        med_read.columns = ["Num Medications", "Rate"]
        med_read["Rate %"] = (med_read["Rate"] * 100).round(2)

        fig6 = px.scatter(
            med_read,
            x="Num Medications",
            y="Rate %",
            size="Rate %",
            color="Rate %",
            color_continuous_scale="Reds",
            labels={"Rate %": "Readmission Rate (%)"}
        )
        fig6.update_layout(
            coloraxis_showscale=False,
            yaxis_title="Readmission Rate (%)",
            margin=dict(t=20, b=20, l=20, r=20),
            height=340
        )
        st.plotly_chart(fig6, use_container_width=True)

    # ── Row 4 : Race breakdown + Medications ─────────────────────────────────
    # col_e, col_f = st.columns(2)

    # with col_e:
    #     st.subheader("Readmission rate by race")

    #     # reconstruct race from dummy columns
    #     race_dummies = [c for c in df.columns if c.startswith("race_")]
    #     race_map_df = df[race_dummies + ["readmitted_binary"]].copy()

    #     race_rates = {}
    #     for col in race_dummies:
    #         race_name = col.replace("race_", "")
    #         mask = race_map_df[col] == 1
    #         if mask.sum() > 0:
    #             race_rates[race_name] = race_map_df.loc[mask, "readmitted_binary"].mean() * 100

    #     # the baseline race (dropped in get_dummies) is AfricanAmerican
    #     base_mask = (race_map_df[race_dummies] == 0).all(axis=1)
    #     race_rates["AfricanAmerican"] = race_map_df.loc[base_mask, "readmitted_binary"].mean() * 100

    #     race_df = pd.DataFrame(list(race_rates.items()), columns=["Race", "Rate %"])
    #     race_df = race_df.sort_values("Rate %", ascending=True)

    #     fig5 = px.bar(
    #         race_df,
    #         x="Rate %",
    #         y="Race",
    #         orientation="h",
    #         color="Rate %",
    #         color_continuous_scale="Teal",
    #         text="Rate %"
    #     )
    #     fig5.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    #     fig5.update_layout(
    #         coloraxis_showscale=False,
    #         xaxis_title="Readmission Rate (%)",
    #         margin=dict(t=20, b=20, l=20, r=20),
    #         height=340
    #     )
    #     st.plotly_chart(fig5, use_container_width=True)

    # with col_f:
    #     st.subheader("Number of medications vs readmission")

    #     med_read = df.groupby("num_medications")["readmitted_binary"].mean().reset_index()
    #     med_read.columns = ["Num Medications", "Rate"]
    #     med_read["Rate %"] = (med_read["Rate"] * 100).round(2)

    #     fig6 = px.scatter(
    #         med_read,
    #         x="Num Medications",
    #         y="Rate %",
    #         size="Rate %",
    #         color="Rate %",
    #         color_continuous_scale="Reds",
    #         labels={"Rate %": "Readmission Rate (%)"}
    #     )
    #     fig6.update_layout(
    #         coloraxis_showscale=False,
    #         yaxis_title="Readmission Rate (%)",
    #         margin=dict(t=20, b=20, l=20, r=20),
    #         height=340
    #     )
    #     st.plotly_chart(fig6, use_container_width=True)

    # ── Row 5 : Feature importance ────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Top 15 feature importances (Random Forest)")

    importance_df = pd.DataFrame({
        "Feature":    feature_cols,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False).head(15)

    fig7 = px.bar(
        importance_df.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale="Blues"
    )
    fig7.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Importance Score",
        margin=dict(t=10, b=20, l=20, r=20),
        height=450
    )
    st.plotly_chart(fig7, use_container_width=True)


# =============================================================================
# PAGE 2 : PREDICTION
# =============================================================================

elif page == "Predict Readmission":

    st.title("Predict Patient Readmission")
    st.markdown("Fill in the patient details below and click **Predict** to see whether the patient is likely to be readmitted within 30 days.")
    st.markdown("---")

    # ── Input form ────────────────────────────────────────────────────────────
    with st.form("prediction_form"):

        st.subheader("Patient demographics")
        col1, col2, col3 = st.columns(3)

        with col1:
            age_input = st.selectbox(
                "Age group",
                options=["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)",
                         "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"],
                index=6
            )

        with col2:
            gender_input = st.selectbox("Gender", ["Female", "Male"])

        with col3:
            race_input = st.selectbox(
                "Race",
                ["Caucasian", "AfricanAmerican", "Hispanic", "Asian", "Other"]
            )

        st.markdown("---")
        st.subheader("Hospital visit details")
        col4, col5, col6, col7 = st.columns(4)

        with col4:
            time_in_hospital = st.slider("Days in hospital", 1, 14, 4)

        with col5:
            num_lab_procedures = st.slider("Lab procedures", 1, 132, 43)

        with col6:
            num_procedures = st.slider("Medical procedures", 0, 6, 1)

        with col7:
            num_medications = st.slider("Number of medications", 1, 81, 15)

        col8, col9, col10, col11 = st.columns(4)

        with col8:
            number_outpatient = st.slider("Outpatient visits", 0, 42, 0)

        with col9:
            number_emergency = st.slider("Emergency visits", 0, 76, 0)

        with col10:
            number_inpatient = st.slider("Inpatient visits", 0, 21, 0)

        with col11:
            number_diagnoses = st.slider("Number of diagnoses", 1, 16, 7)

        st.markdown("---")
        st.subheader("Medication details")
        col12, col13, col14 = st.columns(3)

        with col12:
            insulin_input = st.selectbox(
                "Insulin usage",
                ["No", "Down", "Steady", "Up"]
            )

        with col13:
            diabetes_med = st.selectbox("On diabetes medication?", ["Yes", "No"])

        with col14:
            change_med = st.selectbox("Medication changed this visit?", ["Yes", "No"])

        st.markdown("**Which oral medications is the patient taking?**")
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        met  = mc1.selectbox("Metformin",     ["No", "Steady", "Up", "Down"])
        glip = mc2.selectbox("Glipizide",     ["No", "Steady", "Up", "Down"])
        glyb = mc3.selectbox("Glyburide",     ["No", "Steady", "Up", "Down"])
        pio  = mc4.selectbox("Pioglitazone",  ["No", "Steady", "Up", "Down"])
        rosi = mc5.selectbox("Rosiglitazone", ["No", "Steady", "Up", "Down"])

        st.markdown("---")
        submitted = st.form_submit_button("Predict", use_container_width=True)

    # ── On submit: build feature vector and predict ───────────────────────────
    if submitted:

        # convert inputs to model format
        age_map = {
            "[0-10)": 0, "[10-20)": 10, "[20-30)": 20, "[30-40)": 30,
            "[40-50)": 40, "[50-60)": 50, "[60-70)": 60, "[70-80)": 70,
            "[80-90)": 80, "[90-100)": 90
        }
        age_numeric     = age_map[age_input]
        gender_num      = 1 if gender_input == "Male" else 0
        insulin_numeric = {"No": 0, "Down": 1, "Steady": 2, "Up": 3}[insulin_input]
        diabetes_num    = 1 if diabetes_med == "Yes" else 0
        change_num      = 1 if change_med  == "Yes" else 0

        meds_active = sum([
            met  != "No",
            glip != "No",
            glyb != "No",
            pio  != "No",
            rosi != "No"
        ])

        service_intensity = (time_in_hospital + number_inpatient +
                             number_outpatient + number_emergency)

        # race dummies  (base category = AfricanAmerican, which is dropped)
        race_Asian      = 1 if race_input == "Asian"          else 0
        race_Caucasian  = 1 if race_input == "Caucasian"      else 0
        race_Hispanic   = 1 if race_input == "Hispanic"       else 0
        race_Other      = 1 if race_input == "Other"          else 0

        # build input row in the exact column order the model was trained on
        input_data = {
            "time_in_hospital"  : time_in_hospital,
            "num_lab_procedures": num_lab_procedures,
            "num_procedures"    : num_procedures,
            "num_medications"   : num_medications,
            "number_outpatient" : number_outpatient,
            "number_emergency"  : number_emergency,
            "number_inpatient"  : number_inpatient,
            "number_diagnoses"  : number_diagnoses,
            "gender_num"        : gender_num,
            "diabetesMed"       : diabetes_num,
            "change"            : change_num,
            "age_numeric"       : age_numeric,
            "total_meds_active" : meds_active,
            "insulin_numeric"   : insulin_numeric,
            "service_intensity" : service_intensity,
            "race_Asian"        : race_Asian,
            "race_Caucasian"    : race_Caucasian,
            "race_Hispanic"     : race_Hispanic,
            "race_Other"        : race_Other,
        }

        input_df = pd.DataFrame([input_data])[feature_cols]

        input_scaled  = scaler.transform(input_df)
        prediction    = model.predict(input_scaled)[0]
        probability   = model.predict_proba(input_scaled)[0]

        prob_positive = probability[1] * 100   # probability of readmission <30d
        prob_negative = probability[0] * 100

        st.markdown("---")
        st.subheader("Prediction result")

        # ── Result banner ─────────────────────────────────────────────────────
        if prediction == 1:
            st.error(
                f"⚠️  **High Risk — Patient is likely to be readmitted within 30 days**  \n"
                f"Readmission probability: **{prob_positive:.1f}%**"
            )
        else:
            st.success(
                f"✅  **Low Risk — Patient is NOT likely to be readmitted within 30 days**  \n"
                f"Readmission probability: **{prob_positive:.1f}%**"
            )

        # ── Probability gauge ─────────────────────────────────────────────────
        col_left, col_right = st.columns(2)

        with col_left:
            gauge = go.Figure(go.Indicator(
                mode  = "gauge+number+delta",
                value = round(prob_positive, 1),
                title = {"text": "Readmission Risk (%)", "font": {"size": 16}},
                # delta = {"reference": 11.2, "increasing": {"color": "#F44336"},
                #          "decreasing": {"color": "#4CAF50"}},
                gauge = {
                    "axis"  : {"range": [0, 100]},
                    "bar"   : {"color": "#F44336" if prediction == 1 else "#4CAF50"},
                    "steps" : [
                        {"range": [0,  30], "color": "#E8F5E9"},
                        {"range": [30, 60], "color": "#FFF9C4"},
                        {"range": [60, 100], "color": "#FFEBEE"},
                    ],
                    "threshold": {
                        "line" : {"color": "#333", "width": 3},
                        "thickness": 0.8,
                        "value": 50
                    }
                }
            ))
            gauge.update_layout(height=280, margin=dict(t=30, b=10, l=30, r=30))
            st.plotly_chart(gauge, use_container_width=True)

        with col_right:
            # probability breakdown bar
            prob_fig = go.Figure()
            prob_fig.add_trace(go.Bar(
                x=[prob_negative],
                y=[""],
                orientation="h",
                name="Not readmitted",
                marker_color="#4CAF50",
                text=f"{prob_negative:.1f}%",
                textposition="inside"
            ))
            prob_fig.add_trace(go.Bar(
                x=[prob_positive],
                y=[""],
                orientation="h",
                name="Readmitted <30d",
                marker_color="#F44336",
                text=f"{prob_positive:.1f}%",
                textposition="inside"
            ))
            prob_fig.update_layout(
                barmode="stack",
                height=280,
                title="Probability breakdown",
                xaxis=dict(range=[0, 100], title="Probability (%)"),
                margin=dict(t=50, b=30, l=10, r=10),
                legend=dict(orientation="h", y=-0.2)
            )
            st.plotly_chart(prob_fig, use_container_width=True)

        # ── Summary of what was entered ───────────────────────────────────────
        st.markdown("---")
        st.subheader("Patient summary")

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:
            st.markdown("**Demographics**")
            st.write(f"Age group: {age_input}")
            st.write(f"Gender: {gender_input}")
            st.write(f"Race: {race_input}")

        with summary_col2:
            st.markdown("**Hospital visit**")
            st.write(f"Days in hospital: {time_in_hospital}")
            st.write(f"Lab procedures: {num_lab_procedures}")
            st.write(f"Medications: {num_medications}")
            st.write(f"Diagnoses: {number_diagnoses}")
            st.write(f"Service intensity score: {service_intensity}")

        with summary_col3:
            st.markdown("**Medication**")
            st.write(f"Insulin: {insulin_input}")
            st.write(f"On diabetes med: {diabetes_med}")
            st.write(f"Medication changed: {change_med}")
            st.write(f"Oral drugs active: {meds_active} / 5")
