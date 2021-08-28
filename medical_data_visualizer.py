import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add BMI column
df['BMI'] = df['weight']/((df['height']* 0.01)**2)

#define function to check overweight

def check_overweight(bmi_value):
    if bmi_value > 25:
        return 1
    else:
        return 0

# Add 'overweight' column
df['overweight'] = df['BMI'].apply(check_overweight)

#drop BMI column
df = df.drop('BMI', axis = 1)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

# define function to normalize data
def normalize(parameter_value):
    if parameter_value == 1:
        return 0
    if parameter_value > 1:
        return 1

df['cholesterol'] = df['cholesterol'].apply(normalize)
df['gluc'] = df['gluc'].apply(normalize)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars= 'cardio', value_vars= ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x = 'variable', kind = 'count', data = df_cat, hue = 'value', col= 'cardio')
    fig.set(xlabel = 'variable', ylabel = 'total')



    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    bp_mask = (df['ap_lo'] <= df['ap_hi'])
    ht_mask = (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975))
    wt_mask = (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))

    df_heat = df[bp_mask & ht_mask & wt_mask]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10,10))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, fmt= '0.1f', annot= True, center=0, square=True, linewidths=1, cbar_kws={"shrink": .5})



    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
