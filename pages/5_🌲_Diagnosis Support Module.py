import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.tree import plot_tree
from sklearn import tree
# from dtreeviz.trees import *
st.title('CLINICAL DECISION SUPPORT SYSTEM FOR MIGRAINE')
 

df = pd.read_csv("Migraine-Decision-Support-System/data.csv")

if st.checkbox('Show dataframe'):
    st.write(df)
st.markdown("""<style>
    .font {
        font-size:40px;
            }
    </style>""", unsafe_allow_html = True)
    # st.markdown('<p class ="font">The symptoms which is more common in any Type of Migraine is the Visual Symptoms, which affects the area of the eyes</p>',  unsafe_allow_html = True)
 

st.markdown('<p class ="font">Diagnostic Support Module</p>',  unsafe_allow_html = True)
st.markdown("""<style>
.small-font {
    font-size:20px;
    }
    </style>""", unsafe_allow_html = True)
st.markdown('<p class ="small-font">The Decision Tree Classifier module gives you the best fit for the data. So do choose the Decision Tree Classifier for getting the diagnostic support</p>',  unsafe_allow_html = True)

# For encoding
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn import tree
import plotly.graph_objects as go

 
features= df[['Age', 'Duration', 'Frequency', 'Location', 'Intensity', 'Nausea', 'Vomit', 'Phonophobia', 'Photophobia', 'Visual', 'Sensory', 'Dysphasia', 'Dysarthria', 'Vertigo', 'Tinnitus', 'Hypoacusis', 'Diplopia', 'Defect', 'Ataxia', 'Conscience', 'Paresthesia', 'DPF']].values
labels = df['Type'].values
# Initilize LabelEncoder object
le = LabelEncoder()

# Fit transfrom the Type feature
df['Type'] = le.fit_transform(df["Type"])

X_train,X_test, y_train, y_test = train_test_split(features, labels, train_size=0.7, random_state=1)
 
alg = ['Decision Tree', 'Support Vector Machine', 'Random Forest Classifier']
classifier = st.selectbox('Which algorithm?', alg)
if classifier=='Decision Tree':
    dtc = DecisionTreeClassifier(max_depth=3)
    dtc.fit(X_train, y_train)
    acc = dtc.score(X_test, y_test)
    st.write('Accuracy: ', acc)
    pred_dtc = dtc.predict(X_test)
    cm_dtc=confusion_matrix(y_test,pred_dtc)
    st.write('Confusion matrix: ', cm_dtc)
    fig, ax = plt.subplots(figsize=(8, 5))
    tree.plot_tree(dtc,feature_names=['Age', 'Duration', 'Frequency', 'Location', 'Intensity', 'Nausea', 'Vomit', 'Phonophobia', 'Photophobia', 'Visual', 'Sensory', 'Dysphasia', 'Dysarthria', 'Vertigo', 'Tinnitus', 'Hypoacusis', 'Diplopia', 'Defect', 'Ataxia', 'Conscience', 'Paresthesia', 'DPF', 'Type'],
               filled = True)
    st.pyplot(fig)
    st.markdown("""<style>
    .big-font {
        font-size:30px;
    }
    </style>""", unsafe_allow_html = True)
    st.markdown('<p class ="big-font">The symptoms which is more common in any Type of Migraine is the Visual Symptoms, which affects the area of the eyes</p>',  unsafe_allow_html = True)

 
     
elif classifier == 'Support Vector Machine':
    svm=SVC()
    svm.fit(X_train, y_train)
    acc = svm.score(X_test, y_test)
    st.write('Accuracy: ', acc)
    pred_svm = svm.predict(X_test)
    cm=confusion_matrix(y_test,pred_svm)
    st.write('Confusion matrix: ', cm)

elif classifier == 'Random Forest Classifier':
    rf = RandomForestClassifier()
    # fit the model
    rf.fit(X_train, y_train)
    acc = rf.score(X_test, y_test)
    st.write('Accuracy: ', acc)
    pred_rf = rf.predict(X_test)
    cm=confusion_matrix(y_test,pred_rf)
    st.write('Confusion matrix: ', cm)
    pred =rf.predict(X_test)
    fig = plt.figure(figsize=(15, 10))
    plot_tree(rf.estimators_[0], 
          feature_names=['Age', 'Duration', 'Frequency', 'Location', 'Intensity', 'Nausea', 'Vomit', 'Phonophobia', 'Photophobia', 'Visual', 'Sensory', 'Dysphasia', 'Dysarthria', 'Vertigo', 'Tinnitus', 'Hypoacusis', 'Diplopia', 'Defect', 'Ataxia', 'Conscience', 'Paresthesia', 'DPF', 'Type'],
          filled=True)
    st.pyplot(fig)

st.write('<p class ="small-font">Stay Healthy and fit... Follow the Regualr practices of Yoga and Meditation... Which makes your mind and soul relax and free from Headache...</p>',  unsafe_allow_html = True)
