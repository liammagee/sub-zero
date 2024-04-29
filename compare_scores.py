# First, let's load the Excel file to see what's inside it.
import pandas as pd

# Load the Excel file
# file_path = 'data/Low temp Hackathon 1135.xlsx'
file_path = 'data/Low temp Hackathon 2024.xlsx'

# Check the sheet names in the Excel file
sheet_names = pd.ExcelFile(file_path).sheet_names
print(sheet_names)

# Let's load the content of each sheet to get an overview of the data it contains.
data_overview = {}

for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    data_overview[sheet] = df.head()  # Displaying first few rows for an overview



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
gpt4_4_totals = column_totals['GPT-4-04'].values
llama2_totals = column_totals['Llama2'].values
llama3_totals = column_totals['Llama3'].values
claude3_totals = column_totals['Claude'].values

# Remove any labels not present across all sheets
common_labels = set(labels).intersection(set(column_totals['GPT-4'].index), set(column_totals['Llama2'].index))
# common_labels = sorted(list(common_labels))

# print(common_labels)
common_labels = labels

humans_totals = [column_totals['Humans'][label] for label in common_labels]
gpt4_totals = [column_totals['GPT-4'][label] for label in common_labels]
gpt4_4_totals = [column_totals['GPT-4-04'][label] for label in common_labels]
llama2_totals = [column_totals['Llama2'][label] for label in common_labels]
llama3_totals = [column_totals['Llama3'][label] for label in common_labels]
claude3_totals = [column_totals['Claude'][label] for label in common_labels]

print(column_totals['Humans'])
print(humans_totals)

# Define the bar positions
x = np.arange(len(common_labels))

# Create the plot
fig, ax = plt.subplots(figsize=(15, 8))


# Define bar widths and positions
width = 0.1
colors = ['#000000', '#FF4500', '#FCD603', '#888888', '#0077B6', '#00A896']  # Blue, Orange, Green, Red
# colors = ['#000000', '#FF4500', '#FCD603', '#888888', '#FF6B35', '#FF8C00']  # Blue, Orange, Green, Red


rects1 = ax.bar(x - width * 4, humans_totals, width, label='Humans', color = colors[0])

rects2 = ax.bar(x - width * 2.5, gpt4_4_totals, width, label='GPT-4 (2024)', color = colors[1])
rects4 = ax.bar(x - width * 1.5, llama3_totals, width, label='Llama3 (2024)', color = colors[4])
rects6 = ax.bar(x - width * 0.5, claude3_totals, width, label='Claude3 (2024)', color = colors[5])

rects3 = ax.bar(x + width * 1.0, gpt4_totals, width, label='GPT-4 (2023)', color = colors[2])
rects5 = ax.bar(x + width * 2.0, llama2_totals, width, label='Llama2 (2023)', color = colors[3])

# Add labels, title, and legend
ax.set_ylabel('Total Values')
ax.set_title('Total Values of Numerical Columns Across Sheets')
# ax.set_xticks(ticks=range(len(labels)), labels=labels, rotation=45, ha='right', fontsize=12)
ax.set_xticks(range(len(common_labels)))
ax.set_xticklabels(common_labels, rotation=45, ha="right")
ax.legend()

# Show the plot
plt.tight_layout()
# Saving the bar graph to a file
output_file_path = 'data/comparison_graph_04_2024.png'
fig.savefig(output_file_path)

# Re-creating the line graph using a different approach

# Creating a DataFrame for the bar graph
data_for_line_graph = pd.DataFrame({
    'Labels': labels,
    'Humans': humans_totals,
    'GPT-4 (2024)': gpt4_4_totals,
    'Llama3 (2024)': llama3_totals,
    'Claude3 (2024)': claude3_totals,
    'GPT-4 (2023)': gpt4_totals,
    'Llama2 (2023)': llama2_totals,
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
output_file_path = 'data/comparison_line_graph_04_2024.png'
line_fig.savefig(output_file_path)


from sklearn.preprocessing import MinMaxScaler

# Normalizing the data
scaler = MinMaxScaler()

# Combining the data for normalization
combined_data = np.vstack([humans_totals, gpt4_totals, llama2_totals, gpt4_4_totals, llama3_totals, claude3_totals]).T

# Normalizing the data
normalized_data = scaler.fit_transform(combined_data)

offset = 0.1
normalized_data = normalized_data + offset

# Splitting the normalized data back into separate arrays
normalized_humans = normalized_data[:, 0]
normalized_gpt4 = normalized_data[:, 1]
normalized_llama2 = normalized_data[:, 2]
normalized_gpt4_4 = normalized_data[:, 3]
normalized_llama3 = normalized_data[:, 4]
normalized_claude3 = normalized_data[:, 5]

# Creating a line graph for the normalized data
normalized_fig, normalized_ax = plt.subplots(figsize=(15, 8))

# Plotting the normalized data
normalized_ax.plot(labels, normalized_humans, label='Humans (Normalized)', marker='o', color = colors[0])

normalized_ax.plot(labels, normalized_gpt4_4, label='GPT-4 (2024)', marker='s', color = colors[1])
normalized_ax.plot(labels, normalized_llama3, label='Llama3 (2024)', marker='^', color = colors[4])
normalized_ax.plot(labels, normalized_claude3, label='Claude3 (2024)', marker='^', color = colors[5])

normalized_ax.plot(labels, normalized_gpt4, label='GPT-4 (2023)', marker='s', color = colors[2])
normalized_ax.plot(labels, normalized_llama2, label='Llama2 (2023)', marker='^', color = colors[3])


# Add labels, title, and legend
normalized_ax.set_ylabel('Normalized Total Values')
normalized_ax.set_title('Normalized Line Graph of Total Values Across Sheets')
normalized_ax.set_xticks(x)
normalized_ax.set_xticklabels(labels, rotation=45, ha="right")
normalized_ax.legend()

plt.tight_layout()

output_file_path = 'data/comparison_line_graph_normed_04_2024.png'
normalized_fig.savefig(output_file_path)


# Create the plot
fig, ax = plt.subplots(figsize=(15, 8))

# Define bar widths and positions
y_min = -0.1
width = 0.1
rects1 = ax.bar(x - width * 4, normalized_humans, width, label='Humans', color = colors[0])

negative_mask = normalized_humans < 0
rects_neg = ax.bar(x[negative_mask] - width * 4, normalized_humans[negative_mask], width, color=colors[0])


rects2 = ax.bar(x - width * 2.5, normalized_gpt4_4, width, label='GPT-4 (2024)', color = colors[1])
rects4 = ax.bar(x - width * 1.5, normalized_llama3, width, label='Llama3 (2024)', color = colors[4])
rects6 = ax.bar(x - width * 0.5, normalized_claude3, width, label='Claude3 (2024)', color = colors[5])

rects3 = ax.bar(x + width * 1.0, normalized_gpt4, width, label='GPT-4 (2023)', color = colors[2])
rects5 = ax.bar(x + width * 2.0, normalized_llama2, width, label='Llama2 (2023)', color = colors[3])

# Fill in the negative areas
for rect in rects_neg:
    height = rect.get_height()
    ax.fill_between([rect.get_x(), rect.get_x() + rect.get_width()], [height, height], 0, color=colors[0], alpha=0.5)

# Add labels, title, and legend
ax.set_ylabel('Total Values')
ax.set_title('Total Values of Numerical Columns Across Sheets')
# ax.set_xticks(ticks=range(len(labels)), labels=labels, rotation=45, ha='right', fontsize=12)
ax.set_ylim(bottom=y_min)
ax.axhline(0, color='black', linewidth=0.8)  # Add a horizontal line at y=0
ax.set_xticks(range(len(common_labels)))
ax.set_xticklabels(common_labels, rotation=45, ha="right")
ax.legend()

# Show the plot
plt.tight_layout()
# Saving the bar graph to a file
output_file_path = 'data/comparison_graph_normalised_04_2024.png'
fig.savefig(output_file_path)
