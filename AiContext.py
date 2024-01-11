from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from dataset import dataset
import time

# Preprocess the data
messages = [item['message'] for item in dataset]
intents = [item['intent'] for item in dataset]
print("Training Model Please Wait.....")
#time.sleep(5)
X_train, X_test, y_train, y_test = train_test_split(messages, intents, test_size=0.2, random_state=42)

# Train a Random Forest model
model = make_pipeline(TfidfVectorizer(), RandomForestClassifier())
model.fit(X_train, y_train)

# Predict intent for a new message
def recognize_intent2(message):
    predicted_intent = model.predict([message])[0]
    return predicted_intent

