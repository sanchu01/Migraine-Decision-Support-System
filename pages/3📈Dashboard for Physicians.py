# For data manipulation
# from turtle import color
import numpy as np
import pandas as pd
# For data visualization
import seaborn as sns
import matplotlib.pyplot as plt
# For upsampling
from sklearn.utils import resample
# For encoding
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
# For splitting data
from sklearn.model_selection import train_test_split
# For modelling
from sklearn.ensemble import RandomForestClassifier
# For hyper-parameter tuning
from sklearn.model_selection import RandomizedSearchCV
# For model interpretation
# import shap
# For model evaluation
from sklearn import metrics
from sklearn.metrics import confusion_matrix, plot_roc_curve, classification_report
import streamlit as st
# To supress warnings
import warnings
warnings.filterwarnings('ignore')
st.title('CLINICAL DECISION SUPPORT SYSTEM FOR MIGRAINE')
st.markdown("""<style>
    .big-font {
        font-size:30px;
    }
    </style>""", unsafe_allow_html = True)
st.markdown('<p class ="big-font">This Dashboard helps the physicians to analyze severity of the disease and about the type of migraine with their symptoms</p>',  unsafe_allow_html = True)

df = pd.read_csv("D:/college/Sem IX/Mini Project/MigraineDSS/data.csv")

#Explorartory Data Analysis
#Relationship Between Categorical Variables and Target
cat_col = []
con_col = []

for col in df.columns:
    if df[col].nunique() < 15:
        cat_col.append(col)
    else:
        con_col.append(col)
def count_percentage_plot(df, x, target, suptitle):
    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(20, 10))
    plt.suptitle(suptitle, fontsize=16)
    
    # Plot the count plot
    ax1.set_title(f"Number of {x.capitalize()} across Migraine Type", color="Black")
    sns.countplot(data=df,x=target, hue=x, ax=ax1, palette="Set2")
    ax1.set_xlabel("")
    ax1.xaxis.label.set_color('Black')
    ax1.yaxis.label.set_color('Black')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, color="Black")
    
    # Plot the percent plot
    ax2.set_title(f"Percentage of {x.capitalize()} across Migraine Type", color = "Black")
    sns.histplot(df, x=target, hue=x, stat="probability", multiple="fill", shrink=1,ax=ax2, palette='Set2')
    ax2.set_xlabel("")
    ax2.set_ylabel("Percentage")
    ax2.xaxis.label.set_color('Black')
    ax2.yaxis.label.set_color('Black')
    ax2.set_xticklabels(ax1.get_xticklabels(), rotation=90, color="Black")
    
    
    # Annotating the plots
    for p1,p2 in zip(ax1.patches,ax2.patches):
        ax1.annotate("{:.1f}".format(p1.get_height()), (p1.get_x(),p1.get_height()))
        ax2.annotate("{:.2f}".format(p2.get_height()), (p2.get_x(),p2.get_height()))
        
    ax1, ax2 = st.columns(2)
    
    # st.set_page_config(layout="wide")
    st.pyplot(fig)

st.title("Relation Between Nausea & Migraine Type")
count_percentage_plot(df, 'Nausea', 'Type', "Relation Between Nausea & Migraine Type")
st.write("The above graph represents the “Relation Between Nausea & Migraine Type”, where we find that Nausea occurs for people having the type of Migraine “Migraine with Aura”")

st.title("Relation Between Vomit & Migraine Type")
count_percentage_plot(df, 'Vomit', 'Type', "Relation Between Vomit & Migraine Type")
st.write("The above graph represents the “Relation Between Vomit & Migraine Type”, where we find that vomiting occurs for people having the type of Migraine “Migraine with Aura”")

st.title("Relation Between Phonophobia & Migraine Type")
count_percentage_plot(df, 'Phonophobia', 'Type', "Relation Between Phonophobia & Migraine Type")
st.write("The above graph represents the “Relation Between Phonophobia & Migraine Type”, where we find that Phonophobia occurs for people having the type of Migraine “Typical Migraine with Aura”")

st.title("Relation Between Photophobia & Migraine Type")
count_percentage_plot(df, 'Photophobia', 'Type', "Relation Between Photophobia & Migraine Type")
st.write("The above graph represents the “Relation Between Photophobia & Migraine Type”, where we find that Photophobia occurs for people having the type of Migraine “Typical Migraine with Aura”")

st.title("Relation Between Visual & Migraine Type")
count_percentage_plot(df, 'Visual', 'Type', "Relation Between Visual & Migraine Type")
st.write("The above graph represents the “Relation Between Visual & Migraine Type”, where we find that Visual occurs for people having any type of Migraine except for those having “Migraine with Aura”")

st.title("Relation Between Sensory & Migraine Type")
count_percentage_plot(df, 'Sensory', 'Type', "Relation Between Sensory & Migraine Type")
st.write("The above graph represents the “Relation Between Sensory & Migraine Type”, where we find that Sensory occurs for people having the type of Migraine “Typical Migraine with Aura”")

st.title("Relation Between Dysphasia & Migraine Type")
count_percentage_plot(df, 'Dysphasia', 'Type', "Relation Between Dysphasia & Migraine Type")

st.title("Relation Between Dysarthria And Migraine Type")
count_percentage_plot(df, 'Dysarthria', 'Type', "Relation Between Dysarthria & Migraine Type")

st.title("Relation Between Vertigo & Migraine Type")
count_percentage_plot(df, 'Vertigo', 'Type', "Relation Between Vertigo & Migraine Type")

st.title("Relation Between Tinnitus & Migraine Type")
count_percentage_plot(df, 'Tinnitus', 'Type', "Relation Between Tinnitus & Migraine Type")

st.title("Relation Between Hypoacusis & Migraine Type")
count_percentage_plot(df, 'Hypoacusis', 'Type', "Relation Between Hypoacusis & Migraine Type")

st.title("Relation Between Diplopia & Migraine Type")
count_percentage_plot(df, 'Diplopia', 'Type', "Relation Between Diplopia & Migraine Type")

st.title("Relation Between Defect & Migraine Type")
count_percentage_plot(df, 'Defect', 'Type', "Relation Between Defect & Migraine Type")

st.title("Relation Between Ataxia & Migraine Type")
count_percentage_plot(df, 'Ataxia', 'Type', "Relation Between Ataxia & Migraine Type")

st.title("Relation Between Conscience & Migraine Type")
count_percentage_plot(df, 'Conscience', 'Type', "Relation Between Conscience & Migraine Type")

st.title("Relation Between Paresthesia & Migraine Type")
count_percentage_plot(df, 'Paresthesia', 'Type', "Relation Between Paresthesia & Migraine Type")

st.title("Relation Between DPF & Migraine Type")
count_percentage_plot(df, 'DPF', 'Type', "Relation Between DPF & Migraine Type")
st.write("The above graph represents the “Relation Between DPF & Migraine Type”, where we find that DPF occurs for people having the type of Migraine “Familial Hemiplegic Migraine”")
