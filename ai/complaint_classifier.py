from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# =========================================================
# TRAINING DATA
# =========================================================

training_texts = [
    # Plumbing
    "tap leaking water pipe broken bathroom water problem",
    "washroom water leakage shower not working",
    "water tap broken sink leakage",
    "toilet water problem bathroom leakage",
    "no water in bathroom",
    "water pipe leaking hostel",

    # Electrical
    "electricity power cut fan light switch socket not working",
    "bulb fused fan broken electricity problem",
    "light not working room",
    "fan not working",
    "switch socket damaged",
    "power problem in room",
    "electrical wiring problem",

    # Cleaning
    "room dirty bathroom cleaning garbage dust",
    "washroom cleaning required floor dirty",
    "dirty room needs cleaning",
    "garbage not collected",
    "bathroom is dirty",
    "dust everywhere in room",
    "hostel cleaning problem",

    # Internet
    "wifi internet not working network slow connection",
    "hostel wifi disconnected internet problem",
    "wifi is slow",
    "internet connection not working",
    "wifi keeps disconnecting",
    "no internet in room",
    "hostel network problem",

    # Furniture
    "chair broken table damaged bed furniture",
    "cupboard door broken chair table repair",
    "bed is broken",
    "chair is damaged",
    "table broken",
    "cupboard not working",
    "furniture needs repair",

    # Other
    "food problem mess food quality",
    "mess food is bad",
    "hostel food problem",
    "other hostel problem issue"
]

training_labels = [
    "Plumbing",
    "Plumbing",
    "Plumbing",
    "Plumbing",
    "Plumbing",
    "Plumbing",

    "Electrical",
    "Electrical",
    "Electrical",
    "Electrical",
    "Electrical",
    "Electrical",
    "Electrical",

    "Cleaning",
    "Cleaning",
    "Cleaning",
    "Cleaning",
    "Cleaning",
    "Cleaning",
    "Cleaning",

    "Internet",
    "Internet",
    "Internet",
    "Internet",
    "Internet",
    "Internet",
    "Internet",

    "Furniture",
    "Furniture",
    "Furniture",
    "Furniture",
    "Furniture",
    "Furniture",
    "Furniture",

    "Other",
    "Other",
    "Other",
    "Other"
]


# =========================================================
# TRAIN AI MODEL
# =========================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(training_texts)

model = LogisticRegression(
    max_iter=1000
)

model.fit(X, training_labels)


# =========================================================
# COMPLAINT CLASSIFIER
# =========================================================

def classify_complaint(title, description):

    text = f"{title} {description}".strip()
    text_lower = text.lower()

    # -----------------------------------------------------
    # EMPTY INPUT SAFETY
    # -----------------------------------------------------

    if not text:
        return {
            "category": "Other",
            "confidence": 0.0,
            "priority": "Low"
        }

    # -----------------------------------------------------
    # AI PREDICTION
    # -----------------------------------------------------

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]

    probabilities = model.predict_proba(vector)[0]

    confidence = max(probabilities) * 100


    # -----------------------------------------------------
    # CATEGORY KEYWORD SUPPORT
    # -----------------------------------------------------

    category_keywords = {

        "Plumbing": [
            "water",
            "tap",
            "pipe",
            "leak",
            "leaking",
            "bathroom",
            "washroom",
            "shower",
            "toilet",
            "sink"
        ],

        "Electrical": [
            "electricity",
            "electric",
            "fan",
            "light",
            "bulb",
            "switch",
            "socket",
            "power",
            "wiring",
            "current"
        ],

        "Cleaning": [
            "dirty",
            "cleaning",
            "clean",
            "garbage",
            "dust",
            "waste",
            "messy",
            "dirt"
        ],

        "Internet": [
            "wifi",
            "wi-fi",
            "internet",
            "network",
            "connection",
            "disconnect",
            "disconnected",
            "router"
        ],

        "Furniture": [
            "chair",
            "table",
            "bed",
            "cupboard",
            "furniture",
            "drawer",
            "door"
        ]
    }


    # -----------------------------------------------------
    # USE KEYWORDS FOR CLEAR HOSTEL COMPLAINTS
    # -----------------------------------------------------

    for category, keywords in category_keywords.items():

        if any(keyword in text_lower for keyword in keywords):

            prediction = category
            confidence = max(confidence, 85.0)

            break


    # -----------------------------------------------------
    # PRIORITY DETECTION
    # -----------------------------------------------------

    urgent_words = [
        "fire",
        "smoke",
        "electric shock",
        "sparking",
        "gas leak",
        "flood",
        "explosion",
        "danger",
        "emergency"
    ]

    high_priority_words = [
        "no electricity",
        "no water",
        "not working",
        "broken",
        "leak",
        "leaking",
        "severe",
        "unsafe",
        "cannot use",
        "stopped working"
    ]

    medium_priority_words = [
        "slow",
        "damaged",
        "dirty",
        "disconnected",
        "repair",
        "problem",
        "issue"
    ]


    # -----------------------------------------------------
    # PRIORITY RULES
    # -----------------------------------------------------

    if any(word in text_lower for word in urgent_words):

        priority = "High"

    elif any(word in text_lower for word in high_priority_words):

        priority = "High"

    elif any(word in text_lower for word in medium_priority_words):

        priority = "Medium"

    else:

        priority = "Low"


    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return {
        "category": prediction,
        "confidence": round(confidence, 2),
        "priority": priority
    }