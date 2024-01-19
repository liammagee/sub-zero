import pandas as pd
import re

def extract_scores(text):
    scores = re.findall(r'([\w\s]+): (\d+\.?\d*)', text)
    return {theme.strip(): float(score) for theme, score in scores}

def transform_data(file_path, output_file_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Assuming the text is in a column named 'Text'
    data['Scores'] = data['Text'].apply(extract_scores)

    # Normalize the scores into separate columns
    transformed_data = data.join(pd.json_normalize(data.pop('Scores')))

    # Save the transformed data to a new file
    transformed_data.to_csv(output_file_path, index=False)

# Replace 'your_input_file.csv' with the path to your CSV file and 'your_output_file.csv' with your desired output file name
file_path = 'output_data_llama2_2024.csv'
output_file_path = 'your_output_file.csv'
transform_data(file_path, output_file_path)
