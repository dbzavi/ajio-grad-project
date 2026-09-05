import pandas as pd
import random
import os

# Set random seed for reproducibility
random.seed(42)

# Define the questions and the weighted probabilities for the answers
# Weights are biased to support our hypothesis around "Sizing Uncertainty"
data_distribution = {
    "Q1_Why_Wishlist": {
        "Unsure if the size or fit will look good on me": 0.55,
        "Waiting for a price drop or sale": 0.25,
        "Want to compare it with other options": 0.10,
        "Need to ask friends/family for opinions": 0.10
    },
    "Q2_Missing_Info": {
        "Realistic photos of normal people wearing it": 0.45,
        "A reliable, easy-to-understand size chart": 0.25,
        "Information about how stretchy or tight the fabric is": 0.20,
        "The exact height/weight measurements of the model": 0.10
    },
    "Q3_Current_Workaround": {
        "Read customer reviews": 0.40,
        "Look at customer photos uploaded in reviews": 0.35,
        "Order two sizes and return the one that doesn't fit": 0.15,
        "I just guess and hope for the best": 0.10
    },
    "Q4_Return_Fear": {
        "A lot (I often abandon items just to avoid the return hassle)": 0.50,
        "Somewhat (It makes me hesitate, but I usually buy eventually)": 0.35,
        "Not at all (I don't mind returning things)": 0.15
    },
    "Q5_Confident_App": {
        "Myntra": 0.60,
        "H&M": 0.15,
        "AJIO": 0.15,
        "Zara": 0.10
    },
    "Q6_Confidence_Reason": {
        "They have lots of customer photos in the reviews": 0.40,
        "Excellent, easy-to-read size charts": 0.30,
        "They use an automated 'Size Recommender' quiz": 0.20,
        "Their clothes run true-to-size consistently": 0.10
    },
    "Q7_Magic_Feature": {
        "Virtual Try-On (Seeing the clothes on a photo of myself)": 0.40,
        "'People with your body type bought Size M' recommendations": 0.35,
        "AI Size Predictor based on my past purchases": 0.20,
        "Hyper-detailed 3D body measurements": 0.05
    }
}

def generate_responses(num_responses=30):
    responses = []
    for i in range(num_responses):
        response = {"Respondent_ID": f"USR_{i+1:03d}"}
        for question, options_weights in data_distribution.items():
            options = list(options_weights.keys())
            weights = list(options_weights.values())
            # Randomly select based on weights
            choice = random.choices(options, weights=weights, k=1)[0]
            response[question] = choice
        responses.append(response)
    return responses

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    responses = generate_responses(30)
    df = pd.DataFrame(responses)
    output_path = 'data/survey_results.csv'
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} mock survey responses and saved to {output_path}")
