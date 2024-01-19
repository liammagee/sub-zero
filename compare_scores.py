# First, let's load the Excel file to see what's inside it.
import pandas as pd

# Load the Excel file
file_path = 'data/Low temp Hackathon 1135.xlsx'

# Check the sheet names in the Excel file
sheet_names = pd.ExcelFile(file_path).sheet_names
print(sheet_names)

# Let's load the content of each sheet to get an overview of the data it contains.
data_overview = {}

for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    data_overview[sheet] = df.head()  # Displaying first few rows for an overview

print(data_overview)


# Load each sheet and compute the total for each numerical column
column_totals = {}

for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    # Summing up only the numerical columns
    column_totals[sheet] = df.select_dtypes(include=['number']).sum()


print(column_totals)

import matplotlib.pyplot as plt
import numpy as np

# Prepare the data for plotting
labels = list(column_totals['Humans'].index)
humans_totals = column_totals['Humans'].values
gpt4_totals = column_totals['GPT-4'].values
llama2_totals = column_totals['Llama2'].values

# Remove any labels not present across all sheets
common_labels = set(labels).intersection(set(column_totals['GPT-4'].index), set(column_totals['Llama2'].index))
common_labels = sorted(list(common_labels))

humans_totals = [column_totals['Humans'][label] for label in common_labels]
gpt4_totals = [column_totals['GPT-4'][label] for label in common_labels]
llama2_totals = [column_totals['Llama2'][label] for label in common_labels]

# Define the bar positions
x = np.arange(len(common_labels))

# Create the plot
fig, ax = plt.subplots(figsize=(15, 8))

# Define bar widths and positions
width = 0.25
rects1 = ax.bar(x - width, humans_totals, width, label='Humans')
rects2 = ax.bar(x, gpt4_totals, width, label='GPT-4')
rects3 = ax.bar(x + width, llama2_totals, width, label='Llama2')

# Add labels, title, and legend
ax.set_ylabel('Total Values')
ax.set_title('Total Values of Numerical Columns Across Sheets')
ax.set_xticks(x)
ax.set_xticklabels(common_labels, rotation=45, ha="right")
ax.legend()

# Show the plot
plt.tight_layout()
# plt.show()
# Saving the bar graph to a file
output_file_path = 'data/comparison_graph.png'
fig.savefig(output_file_path)

# Re-creating the line graph using a different approach

# Creating a DataFrame for the line graph
data_for_line_graph = pd.DataFrame({
    'Labels': labels,
    'Humans': humans_totals,
    'GPT-4': gpt4_totals,
    'Llama2': llama2_totals
})

# Setting the 'Labels' column as index for plotting
data_for_line_graph.set_index('Labels', inplace=True)

# Plotting the line graph
line_fig, line_ax = plt.subplots(figsize=(15, 8))
data_for_line_graph.plot(kind='line', ax=line_ax, marker='o')

# Adding labels and title
line_ax.set_ylabel('Total Values')
line_ax.set_title('Line Graph of Total Values Across Sheets')
line_ax.set_xticks(x)
line_ax.set_xticklabels(labels, rotation=45, ha="right")

line_ax.legend()

plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
# Saving the bar graph to a file
output_file_path = 'data/comparison_line_graph.png'
line_fig.savefig(output_file_path)


print(labels)


from sklearn.preprocessing import MinMaxScaler

# Normalizing the data
scaler = MinMaxScaler()

# Combining the data for normalization
combined_data = np.vstack([humans_totals, gpt4_totals, llama2_totals]).T

# Normalizing the data
normalized_data = scaler.fit_transform(combined_data)

# Splitting the normalized data back into separate arrays
normalized_humans = normalized_data[:, 0]
normalized_gpt4 = normalized_data[:, 1]
normalized_llama2 = normalized_data[:, 2]

# Creating a line graph for the normalized data
normalized_fig, normalized_ax = plt.subplots(figsize=(15, 8))

# Plotting the normalized data
normalized_ax.plot(labels, normalized_humans, label='Humans (Normalized)', marker='o')
normalized_ax.plot(labels, normalized_gpt4, label='GPT-4 (Normalized)', marker='s')
normalized_ax.plot(labels, normalized_llama2, label='Llama2 (Normalized)', marker='^')

# Add labels, title, and legend
normalized_ax.set_ylabel('Normalized Total Values')
normalized_ax.set_title('Normalized Line Graph of Total Values Across Sheets')
normalized_ax.set_xticks(x)
normalized_ax.set_xticklabels(labels, rotation=45, ha="right")
normalized_ax.legend()

plt.tight_layout()

output_file_path = 'data/comparison_line_graph_normed.png'
normalized_fig.savefig(output_file_path)
