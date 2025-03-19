import pandas as pd

# Load your CSV file
df = pd.read_csv('dogs_manual_score.csv')

# Assuming the images are stored in a folder named 'images' on your local machine
image_folder = 'dog_pics'

# Add a new column with the full path to the image
df['Image Path'] = df['Photo'].apply(lambda x: f"{image_folder}{x}")

# Save the updated CSV with the new 'Image Path' column
df.to_csv('dogs_manual_score.csv', index=False)
