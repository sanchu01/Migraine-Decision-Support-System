# For data manipulation
# from turtle import color
import numpy as np
import pandas as pd
# For data visualization
import seaborn as sns
import plotly.express as px
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
from streamlit_marquee import streamlit_marquee
from streamlit_extras.switch_page_button import switch_page
# For model interpretation
# import shap
# For model evaluation
from sklearn import metrics
from sklearn.metrics import confusion_matrix, plot_roc_curve, classification_report
import streamlit as st
# To supress warnings
import warnings
warnings.filterwarnings('ignore')
st.title("CLINICAL DECISION SUPPORT SYSTEM FOR MIGRAINE")
st.markdown("""<style>
    .big-font {
        font-size:20px;
    }
    </style>""", unsafe_allow_html = True)
df = pd.read_csv("D:/college/Sem IX/Mini Project/MigraineDSS/data.csv")
st.markdown('<p class ="big-font"></p>',  unsafe_allow_html = True)
st.markdown('<p class ="big-font">Hii... Welcome to the Migraine Analysis Dashboard...</p>',  unsafe_allow_html = True)
st.markdown('<p class ="big-font">The purpose of this dashboard is to provide a clinical decision support system to help the physicians in the process of diagnosis of headaches and to help patients get a review of their conditions. Decision Support tools have been developed earlier to detect the migraines by the physicians and diagnose the same.</p>',  unsafe_allow_html = True)


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
    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(20,10))
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
st.title("Relation Between Migraine Type and Duration")
count_percentage_plot(df, 'Duration', 'Type', "Relation Between Migraine Type and Duration")
st.write("1- 5-119 seconds, 2- 120-239 seconds, 3- 240-899 seconds")

# Character and Type
st.title("Relation Between Character & Migraine Type")
count_percentage_plot(df, 'Character', 'Type', "Relation Between Character & Migraine Type")
st.write("0- Pressing, 1- pulsating,2- stabbing")

# Relation Between Intensity & Migraine Type
st.title("Relation Between Intensity & Migraine Type")
count_percentage_plot(df, 'Intensity', 'Type', "Relation Between Intensity & Migraine Type")
st.write("0- Low, 1-Mild, 2- Moderate, 3-Severe ")

st.title("Relation Between Continuous Variable and the Target")

# Relation Between Continuous Variable and Target
def dist_summary(df,col,title,color="purple"):
    fig,ax = plt.subplots(3,1, figsize=(8, 8),sharex=True)
    # Histogram plot
    st.title("Distribution of Feature Age")
    sns.histplot(df[col], kde=True, ax=ax[0], color="purple")
    ax[0].set(xlabel=None)
    ax[0].set_title("KDE Plot", color="Black")#Kernel Distribution Plot
    ax[0].xaxis.label.set_color('Black')
    ax[0].yaxis.label.set_color('Black')
    # Box Plot
    sns.boxplot(df[col], ax=ax[1], color="pink")
    ax[1].set(xlabel=None)
    ax[1].set_title("Box Plot", color="Black")
    ax[1].xaxis.label.set_color('Black')
    ax[1].yaxis.label.set_color('Black')
   
    # Violon Plot
    sns.violinplot(df[col],ax=ax[2], color="purple")
    ax[2].set(xlabel=None)
    ax[2].set_title("Violin Plot", color="Black")
    ax[2].xaxis.label.set_color('Black')
    ax[2].yaxis.label.set_color('Black')
    
    plt.suptitle(title, fontsize=18)
    plt.tight_layout(pad=3)
    st.pyplot(fig)

def hist(df,col):
    fig = plt.figure(figsize=(8,5))
    # plt.title("Distribution Of Age", color="white")
    plt.xlabel("Age", color="white")
    plt.ylabel("Frequency", color="white")
    sns.histplot(df[col], color='purple')
    plt.show()
    st.title("Distribution of Age")
    st.pyplot(fig)
hist(df,"Age")
dist_summary(df,"Age", "Distribution Of Feature Age", color="white")

st.title("Distribution Of Age Across All Migraine Types")
def cat_hist_plot(df,x,target):
    fig,ax = plt.subplots(4,4, figsize=(20,20))
    
    labels = [i for i in df[target].unique() for x in (0,1)]
    row,col = 0,0
    
    fig.delaxes(ax[3][2])
    fig.delaxes(ax[3][3])
    
    plt.suptitle("Distribution Of Age Across All Migraine Types", fontsize=20)
    
    for label in labels:
        if row == 4:
            break
            
        if col%2 == 0:
            ax[row,col].set_title(f"KDE OF AGE FOR {label.upper()}")
            sns.kdeplot(df[df[target]==label]['Age'],ax=ax[row,col], shade=True, color='purple')
            col+=1
            
        else:
            ax[row,col].set_title(f"BOXPLOT OF AGE FOR {label.upper()}")
            sns.boxplot(y=df[df[target]==label]['Age'],ax=ax[row,col], color='pink')
            if col == 3:
                col = 0
                row += 1
                continue
                
            col+=1
            
    
    plt.tight_layout(pad=4)
    st.pyplot(fig)
cat_hist_plot(df,x="Age",target="Type")
st.markdown("""<style>
    .big-font {
        font-size:20px;
    }
    </style>""", unsafe_allow_html = True)
st.write('<p class ="big-font">The above graph represents the Distribution of Age, where this plot helps us know that the frequency of Migraine is high for the people of age group 20 and 30. And it is lesser in the people of age group 60 to 80. This shows that it affects people in their early 20s and 30s.</p>',  unsafe_allow_html = True)

reg = st.button("Register Here")
if reg == True:
    switch_page("register here")
