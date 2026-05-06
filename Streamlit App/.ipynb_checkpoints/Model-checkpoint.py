import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns




df = pd.read_csv("patient_data.csv")

print("Shape of dataset:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumn names:")
print(df.columns.tolist())




print("\nData types:")
print(df.dtypes)

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nTarget column value counts:")
print(df["readmitted"].value_counts())



# DROP COLUMNS WITH TOO MANY MISSING VALUES


# A1Cresult has 83% missing values
# max_glu_serum has 95% missing values
# These columns are mostly empty so we just remove them

df = df.drop(columns=["A1Cresult", "max_glu_serum"])

print("\nAfter dropping high-missing columns:", df.shape)


# These are just ID codes and don't carry useful information for prediction
df = df.drop(columns=["admission_type_id", "discharge_disposition_id", "admission_source_id"])

print("After dropping admin columns:", df.shape)



# Race has only 2273 missing values (about 2%)
# We fill it with the most common value (mode)

most_common_race = df["race"].mode()[0]
df["race"] = df["race"].fillna(most_common_race)

print("\nMissing values in race after filling:", df["race"].isnull().sum())



# There are only 3 rows with "Unknown/Invalid" gender
# We just remove those rows

df = df[df["gender"] != "Unknown/Invalid"]

print("After removing unknown gender rows:", df.shape)



# Age is stored as a bracket like "[70-80)"
# We map each bracket to the lower number so the model can use it

age_mapping = {
    "[0-10)"  : 0,
    "[10-20)" : 10,
    "[20-30)" : 20,
    "[30-40)" : 30,
    "[40-50)" : 40,
    "[50-60)" : 50,
    "[60-70)" : 60,
    "[70-80)" : 70,
    "[80-90)" : 80,
    "[90-100)": 90
}

df["age"] = df["age"].map(age_mapping)

print("\nAge column after mapping:")
print(df["age"].value_counts().sort_index())



# Insulin has 4 categories that represent how much insulin the patient uses
# We convert them to numbers: No=0, Down=1, Steady=2, Up=3

insulin_mapping = {
    "No"    : 0,
    "Down"  : 1,
    "Steady": 2,
    "Up"    : 3
}

df["insulin"] = df["insulin"].map(insulin_mapping)

print("\nInsulin column after mapping:")
print(df["insulin"].value_counts())



# diabetesMed and change columns only have Yes or No
# We convert Yes to 1 and No to 0

df["diabetesMed"] = df["diabetesMed"].map({"Yes": 1, "No": 0})
df["change"]      = df["change"].map({"Ch": 1, "No": 0})

print("\ndiabetesMed value counts:")
print(df["diabetesMed"].value_counts())



df["gender"] = df["gender"].map({"Male": 1, "Female": 0})

print("\nGender after encoding:")
print(df["gender"].value_counts())


# Instead of keeping 5 separate drug columns we just count
# how many drugs each patient is actively taking

med_columns = ["metformin", "glipizide", "glyburide", "pioglitazone", "rosiglitazone"]

# Any value other than "No" means the patient is taking that drug
df["total_meds_active"] = 0

for col in med_columns:
    df["total_meds_active"] = df["total_meds_active"] + (df[col] != "No").astype(int)

# Now we can drop the original 5 columns
df = df.drop(columns=med_columns)

print("\ntotal_meds_active value counts:")
print(df["total_meds_active"].value_counts().sort_index())



# Patients who stay longer and visit more often are generally sicker
# We add up 4 related columns into one score

df["service_intensity"] = (df["time_in_hospital"] +
                           df["number_inpatient"]  +
                           df["number_outpatient"] +
                           df["number_emergency"])

print("\nservice_intensity sample values:")
print(df["service_intensity"].describe())



# Race has 5 different categories so we create a separate column for each
# drop_first=True removes one column to avoid redundancy

df = pd.get_dummies(df, columns=["race"], drop_first=True)

print("\nColumns after encoding race:")
print(df.columns.tolist())



# Original target had 3 values: NO, >30, <30
# We want to predict: was the patient readmitted in less than 30 days?
# So we make it binary:
#   1 = readmitted in less than 30 days (this is what we want to detect)
#   0 = not readmitted within 30 days (includes NO and >30)

df["readmitted"] = (df["readmitted"] == "<30").astype(int)

print("\nTarget column after binary encoding:")
print(df["readmitted"].value_counts())
print("Percentage of positive class:", round(df["readmitted"].mean() * 100, 2), "%")



X = df.drop(columns=["readmitted"])   # all columns except the target
y = df["readmitted"]                  # only the target column

print("\nFeature matrix shape:", X.shape)
print("Target shape:", y.shape)



# 80% of data goes to training, 20% goes to testing
# stratify=y makes sure both sets have the same % of positive class

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size   = 0.20,
    random_state= 42,
    stratify    = y
)

print("\nTraining set size:", X_train.shape)
print("Test set size    :", X_test.shape)



# StandardScaler makes all numbers have similar range
# This helps the model treat all features equally

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)   # fit on train, then transform
X_test  = scaler.transform(X_test)        # only transform test (no fitting)

print("\nFeatures scaled successfully")



# n_estimators = 100       --> use 100 trees
# max_depth = 10           --> each tree can go 10 levels deep
# class_weight = balanced  --> handle imbalanced data (only 11% are class 1)
# random_state = 42        --> so results are same every time we run
# n_jobs = -1              --> use all CPU cores to train faster

rf_model = RandomForestClassifier(
    n_estimators = 100,
    max_depth    = 10,
    class_weight = "balanced",
    random_state = 42,
    n_jobs       = -1
)

# Train the model
rf_model.fit(X_train, y_train)

print("\nModel training complete!")



y_pred      = rf_model.predict(X_test)          # predicted class labels
y_pred_prob = rf_model.predict_proba(X_test)[:, 1]  # probability of class 1

print("\nFirst 10 predictions:", y_pred[:10])



accuracy  = accuracy_score(y_test, y_pred)
f1        = f1_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall    = recall_score(y_test, y_pred)
auc       = roc_auc_score(y_test, y_pred_prob)

print("\n========== MODEL EVALUATION ==========")
print(f"Accuracy  : {accuracy:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"ROC-AUC   : {auc:.4f}")

print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred,
                             target_names=["Not Readmitted (0)", "Readmitted <30d (1)"]))



cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Not Readmitted", "Readmitted <30d"],
            yticklabels=["Not Readmitted", "Readmitted <30d"])
plt.title("Confusion Matrix - Random Forest")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()
print("Confusion matrix saved!")



feature_names        = df.drop(columns=["readmitted"]).columns.tolist()
feature_importances  = rf_model.feature_importances_

importance_df = pd.DataFrame({
    "Feature"   : feature_names,
    "Importance": feature_importances
})

importance_df = importance_df.sort_values("Importance", ascending=False).head(15)

plt.figure(figsize=(9, 6))
plt.barh(importance_df["Feature"], importance_df["Importance"], color="steelblue")
plt.gca().invert_yaxis()
plt.title("Top 15 Feature Importances - Random Forest")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()
print("Feature importance chart saved!")
