import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'data/Low temp Hackathon 2024.xlsx'
data = pd.read_excel(file_path)

# Listing all the sheets in the Excel file
sheet_names = pd.ExcelFile(file_path).sheet_names
sheet_names


# Loading and displaying the first few rows of the "Humans" sheet
humans_data = pd.read_excel(file_path, sheet_name='Humans')
humans_data.head()

# Loading and displaying the first few rows of the "GPT-4" sheet
gpt4_data = pd.read_excel(file_path, sheet_name='GPT-4')
gpt4_data.head()


# Loading and displaying the first few rows of the "GPT-4-04" sheet
gpt4_4_data = pd.read_excel(file_path, sheet_name='GPT-4-04')
gpt4_4_data.head()


# Loading and displaying the first few rows of the "Llama2" sheet
llama2_data = pd.read_excel(file_path, sheet_name='Llama2')
llama2_data.head()


# Loading and displaying the first few rows of the "Llama2" sheet
llama3_data = pd.read_excel(file_path, sheet_name='Llama3')

claude3_data = pd.read_excel(file_path, sheet_name='Claude')



# Excluding the 'statement' column before rounding
gpt4_data_excluding_statement = gpt4_data.drop(['statement', 'author'], axis=1)
gpt4_4_data_excluding_statement = gpt4_data.drop(['statement', 'author'], axis=1)
llama2_data_excluding_statement = llama2_data.drop(['statement', 'author'], axis=1)
llama3_data_excluding_statement = llama3_data.drop(['statement', 'author'], axis=1)
claude3_data_excluding_statement = claude3_data.drop(['statement', 'author'], axis=1)

# Redefining the function to calculate agreement percentage
def calculate_agreement(df1, df2):
    total = df1.shape[0] * df1.shape[1]
    agreement = (df1 == df2).sum().sum()
    return agreement, (agreement / total) * 100

# Rounding the values to 0 or 1
threshold_1 = 50
threshold_2 = 70

# Humans data without the 'statement' and 'author' columns
humans_data_excluding_statement = humans_data.drop(['statement', 'author'], axis=1)
humans_data_excluding_statement = humans_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_1 else 0)
gpt4_data_rounded_1 = gpt4_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_1 else 0)
gpt4_4_data_rounded_1 = gpt4_4_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_1 else 0)
llama2_data_rounded_1 = llama2_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_1 else 0)
llama3_data_rounded_1 = llama3_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_1 else 0)
claude3_data_rounded_1 = claude3_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_1 else 0)
gpt4_data_rounded_2 = gpt4_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_2 else 0)
gpt4_4_data_rounded_2 = gpt4_4_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_2 else 0)
llama2_data_rounded_2 = llama2_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_2 else 0)
llama3_data_rounded_2 = llama3_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_2 else 0)
claude3_data_rounded_2 = claude3_data_excluding_statement.applymap(lambda x: 1 if x >= threshold_2 else 0)


# Recalculate agreement percentages
agreement_gpt4_count_1, agreement_gpt4_1 = calculate_agreement(humans_data_excluding_statement, gpt4_data_rounded_1)
agreement_gpt4_4_count_1, agreement_gpt4_4_1 = calculate_agreement(humans_data_excluding_statement, gpt4_4_data_rounded_1)
agreement_llama2_count_1, agreement_llama2_1 = calculate_agreement(humans_data_excluding_statement, llama2_data_rounded_1)
agreement_llama3_count_1, agreement_llama3_1 = calculate_agreement(humans_data_excluding_statement, llama3_data_rounded_1)
agreement_claude3_count_1, agreement_claude3_1 = calculate_agreement(humans_data_excluding_statement, claude3_data_rounded_1)
agreement_gpt4_count_2, agreement_gpt4_2 = calculate_agreement(humans_data_excluding_statement, gpt4_data_rounded_2)
agreement_gpt4_4_count_2, agreement_gpt4_4_2 = calculate_agreement(humans_data_excluding_statement, gpt4_4_data_rounded_2)
agreement_llama2_count_2, agreement_llama2_2 = calculate_agreement(humans_data_excluding_statement, llama2_data_rounded_2)
agreement_llama3_count_2, agreement_llama3_2 = calculate_agreement(humans_data_excluding_statement, llama3_data_rounded_2)
agreement_claude3_count_2, agreement_claude3_2 = calculate_agreement(humans_data_excluding_statement, claude3_data_rounded_2)



print(f'Human agreement with GPT-4, threshold {threshold_1}:', agreement_gpt4_count_1, agreement_gpt4_1)
print(f'Human agreement with GPT-4-4, threshold {threshold_1}:', agreement_gpt4_4_count_1, agreement_gpt4_4_1)
print(f'Human agreement with Llama2, threshold {threshold_1}:', agreement_llama2_count_1, agreement_llama2_1)
print(f'Human agreement with Llama3, threshold {threshold_1}:', agreement_llama3_count_1, agreement_llama3_1)
print(f'Human agreement with Claude3, threshold {threshold_1}:', agreement_claude3_count_1, agreement_claude3_1)

print(f'Human agreement with GPT-4, threshold {threshold_2}:', agreement_gpt4_count_2, agreement_gpt4_2)
print(f'Human agreement with GPT-4-4, threshold {threshold_2}:', agreement_gpt4_4_count_2, agreement_gpt4_4_2)
print(f'Human agreement with Llama2, threshold {threshold_2}:', agreement_llama2_count_2, agreement_llama2_2)
print(f'Human agreement with Llama3, threshold {threshold_2}:', agreement_llama3_count_2, agreement_llama3_2)
print(f'Human agreement with Claude3, threshold {threshold_2}:', agreement_claude3_count_2, agreement_claude3_2)


# Data for plotting
sheets = ['GPT-4', 'Llama2']
agreements_1 = [agreement_gpt4_1, agreement_llama2_1]
agreements_2 = [agreement_gpt4_2, agreement_llama2_2]

# Counting the number of statements with a "1" for each theme in each sheet
count_humans = humans_data_excluding_statement.sum()
count_gpt4_1 = gpt4_data_rounded_1.sum()
count_gpt4_4_1 = gpt4_4_data_rounded_1.sum()
count_llama2_1 = llama2_data_rounded_1.sum()
count_llama3_1 = llama3_data_rounded_1.sum()
count_claude3_1 = claude3_data_rounded_1.sum()
count_gpt4_2 = gpt4_data_rounded_2.sum()
count_gpt4_4_2 = gpt4_4_data_rounded_2.sum()
count_llama2_2 = llama2_data_rounded_2.sum()
count_llama3_2 = llama3_data_rounded_2.sum()
count_claude3_2 = claude3_data_rounded_2.sum()

# Preparing data for plotting
themes = humans_data_excluding_statement.columns
counts = pd.DataFrame({'Humans': count_humans, 
                       f'GPT-4, {threshold_1}': count_gpt4_1, 
                       f'GPT-4-04, {threshold_1}': count_gpt4_4_1, 
                       f'Llama2, {threshold_1}': count_llama2_1, 
                       f'Llama3, {threshold_1}': count_llama3_1, 
                       f'Claude3, {threshold_1}': count_claude3_1, 
                       f'GPT-4, {threshold_2}': count_gpt4_2, 
                       f'GPT-4-04, {threshold_2}': count_gpt4_4_2, 
                       f'Llama2, {threshold_2}': count_llama2_2, 
                       f'Llama3, {threshold_2}': count_llama3_2,
                       f'Claude3, {threshold_2}': count_claude3_2})
counts_1 = pd.DataFrame({'Humans': count_humans, 'GPT-4': count_gpt4_1, 'Llama2': count_llama2_1, 'Llama3': count_llama3_1, 'Claude3': count_claude3_1})
counts_2 = pd.DataFrame({'Humans': count_humans, 'GPT-4': count_gpt4_2, 'Llama2': count_llama2_2, 'Llama3': count_llama3_2, 'Claude3': count_claude3_2})


# Plotting

# Creating two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))

plt.figure(figsize=(16, 10))
counts.plot(kind='bar', ax=plt.gca())
plt.xlabel('Themes', fontsize=14)
plt.ylabel('Number of Statements', fontsize=14)
plt.xticks(ticks=range(len(themes)), labels=themes, rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='Sheet Name', fontsize=12)
plt.tight_layout()  # Adjust layout to prevent cutting-off


# Save the plot to a file
output_file_path = 'data/comparison_dichotomous.png'
plt.savefig(output_file_path)
plt.close()  # Close the plot

# Calculating the correlation between the counts for each theme across the three sheets
print("Rounded results")
correlation_matrix = counts.corr()
print(correlation_matrix)

print("Full results")
full_0 = humans_data_excluding_statement.to_numpy().flatten().tolist()
full_1 = gpt4_data_excluding_statement.to_numpy().flatten().tolist()
full_2 = gpt4_4_data_excluding_statement.to_numpy().flatten().tolist()
full_3 = llama2_data_excluding_statement.to_numpy().flatten().tolist()
full_4 = llama3_data_excluding_statement.to_numpy().flatten().tolist()
full_5 = claude3_data_excluding_statement.to_numpy().flatten().tolist()
full_counts = pd.DataFrame({'Humans': full_0, f'GPT-4': full_1, f'GPT-4-04': full_2, f'Llama2': full_3, f'Llama3': full_4, f'Claude3': full_5})
print(full_counts.corr())


# Preparing the data for pairwise correlation analysis
# Dropping the 'statement' columns as they are not needed for correlation calculation
humans_data_corr = humans_data_excluding_statement
gpt4_data_corr = gpt4_data_rounded_1
gpt4_4_data_corr = gpt4_4_data_rounded_1
llama2_data_corr = llama2_data_rounded_1
llama3_data_corr = llama3_data_rounded_1
claude3_data_corr = claude3_data_rounded_1

# Calculating pairwise correlations
corr_humans_gpt4 = humans_data_corr.corrwith(gpt4_data_corr, axis=0).mean()
corr_humans_gpt4_4 = humans_data_corr.corrwith(gpt4_4_data_corr, axis=0).mean()
corr_humans_llama2 = humans_data_corr.corrwith(llama2_data_corr, axis=0).mean()
corr_humans_llama3 = humans_data_corr.corrwith(llama3_data_corr, axis=0).mean()
corr_humans_claude3 = humans_data_corr.corrwith(claude3_data_corr, axis=0).mean()


print('Correlations')
print("corr_humans_gpt4: " + str(corr_humans_gpt4))
print("corr_humans_gpt4_4: " + str(corr_humans_gpt4_4))
print("corr_humans_llama2: " + str(corr_humans_llama2))
print("corr_humans_llama3: " + str(corr_humans_llama3))
print("corr_humans_claude3: " + str(corr_humans_claude3))


# Calculating pairwise correlations
corr_humans_gpt4 = humans_data_corr.corrwith(gpt4_data_corr, axis=1).mean()
corr_humans_gpt4_4 = humans_data_corr.corrwith(gpt4_4_data_corr, axis=1).mean()
corr_humans_llama2 = humans_data_corr.corrwith(llama2_data_corr, axis=1).mean()
corr_humans_llama3 = humans_data_corr.corrwith(llama3_data_corr, axis=1).mean()
corr_humans_claude3 = humans_data_corr.corrwith(claude3_data_corr, axis=1).mean()


print("")
print("Correlations")
print(corr_humans_gpt4)
print(corr_humans_gpt4_4)
print(corr_humans_llama2)
print(corr_humans_llama3)
print(corr_humans_claude3)
print("")

# Creating a long row of all row/column values for each sheet
humans_long_row = humans_data_excluding_statement.values.flatten()
gpt4_long_row = gpt4_data_rounded_1.values.flatten()
gpt4_4_long_row = gpt4_4_data_rounded_1.values.flatten()
llama2_long_row = llama2_data_rounded_1.values.flatten()
llama3_long_row = llama3_data_rounded_1.values.flatten()
claude3_long_row = claude3_data_rounded_1.values.flatten()

# Constructing a DataFrame for correlation calculation
long_row_df = pd.DataFrame({
    'Humans': humans_long_row,
    'GPT-4': gpt4_long_row,
    'GPT-4-04': gpt4_4_long_row,
    'Llama2': llama2_long_row,
    'Llama3': llama3_long_row,
    'Claude3': claude3_long_row
})

# Calculating the correlation
long_row_correlation = long_row_df.corr()
from scipy.stats import pearsonr

# Function to calculate pairwise Pearson correlation with p-value
def calculate_correlation_with_significance(array1, array2):
    correlation, p_value = pearsonr(array1, array2)
    return correlation, p_value


# Calculating pairwise correlations with statistical significance
corr_humans_gpt4, p_humans_gpt4 = calculate_correlation_with_significance(humans_long_row, gpt4_long_row)
corr_humans_gpt4, p_humans_gpt4_4 = calculate_correlation_with_significance(humans_long_row, gpt4_4_long_row)
corr_humans_llama2, p_humans_llama2 = calculate_correlation_with_significance(humans_long_row, llama2_long_row)
corr_humans_llama3, p_humans_llama3 = calculate_correlation_with_significance(humans_long_row, llama3_long_row)
corr_humans_claude3, p_humans_claude3 = calculate_correlation_with_significance(humans_long_row, claude3_long_row)

print("Correlation with significance")
print(corr_humans_gpt4, p_humans_gpt4)
print(corr_humans_gpt4_4, p_humans_gpt4_4)
print(corr_humans_llama2, p_humans_llama2)
print(corr_humans_llama3, p_humans_llama3)
print(corr_humans_claude3, p_humans_claude3)
print("")


from sklearn.metrics import jaccard_score

# Function to calculate Jaccard similarity score for binary data
def jaccard_similarity(df1, df2):
    # Flattening the dataframes to 1D arrays
    array1, array2 = df1.values.flatten(), df2.values.flatten()
    return jaccard_score(array1, array2)


# print("Jaccard similarity score")
# print(gpt4_data_corr.values.flatten())

# Calculating Jaccard similarity scores
jaccard_humans_gpt4 = jaccard_similarity(humans_data_corr, gpt4_data_corr)
jaccard_humans_gpt4_4 = jaccard_similarity(humans_data_corr, gpt4_4_data_corr)
jaccard_humans_llama2 = jaccard_similarity(humans_data_corr, llama2_data_corr)
jaccard_humans_llama3 = jaccard_similarity(humans_data_corr, llama3_data_corr)
jaccard_humans_claude3 = jaccard_similarity(humans_data_corr, claude3_data_corr)

print("Humans vs GPT-4 (July, 2023): " + str(jaccard_humans_gpt4))
print("Humans vs GPT-4 (April, 2024): " + str(jaccard_humans_gpt4_4))
print("Humans vs Llama2 (July, 2023): " + str(jaccard_humans_llama2))
print("Humans vs Llama3 (April, 2024): " + str(jaccard_humans_llama3))
print("Humans vs Claude3 (April, 2024): " + str(jaccard_humans_claude3))

# Counting the total number of themes added to statements by each agent
total_themes_humans = humans_data_excluding_statement.sum().sum()
total_themes_gpt4_1 = gpt4_data_rounded_1.sum().sum()
total_themes_gpt4_4_1 = gpt4_4_data_rounded_1.sum().sum()
total_themes_llama2_1 = llama2_data_rounded_1.sum().sum()
total_themes_llama3_1 = llama3_data_rounded_1.sum().sum()
total_themes_claude3_1 = claude3_data_rounded_1.sum().sum()
total_themes_gpt4_2 = gpt4_data_rounded_2.sum().sum()
total_themes_gpt4_4_2 = gpt4_4_data_rounded_2.sum().sum()
total_themes_llama2_2 = llama2_data_rounded_2.sum().sum()
total_themes_llama3_2 = llama3_data_rounded_2.sum().sum()
total_themes_claude3_2 = claude3_data_rounded_2.sum().sum()

print("total themes applied")
print(total_themes_humans)
print(total_themes_gpt4_1, total_themes_gpt4_4_1, total_themes_llama2_1, total_themes_llama3_1, total_themes_claude3_1)
print(total_themes_gpt4_2, total_themes_gpt4_4_2, total_themes_llama2_2, total_themes_llama3_2, total_themes_claude3_2)







