import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

DATA_PATH = Path("data/raw/admission.csv")
PROCESSED_DIR = Path("data/processed")

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

target = "Chance of Admit"
X = df.drop(columns=["Serial No.", target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

X_train.to_csv(PROCESSED_DIR / "X_train.csv", index=False)
X_test.to_csv(PROCESSED_DIR / "X_test.csv", index=False)
y_train.to_csv(PROCESSED_DIR / "y_train.csv", index=False)
y_test.to_csv(PROCESSED_DIR / "y_test.csv", index=False)

print("Data prepared successfully.")
print(f"X_train: {X_train.shape}")
print(f"X_test: {X_test.shape}")
print(f"y_train: {y_train.shape}")
print(f"y_test: {y_test.shape}")