from streamlit_extras.switch_page_button import switch_page


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from streamlit_marquee import streamlit_marquee

st.set_page_config(page_title="Migraine Analysis Dashboard", page_icon=":bar_chart:", layout="wide")
st.title("CLINICAL DECISION SUPPORT SYSTEM FOR MIGRAINE")
st.markdown("""<style>
    .big-font {
        font-size:30px;
    }
    </style>""", unsafe_allow_html = True)
st.markdown('<p class ="big-font">The patients are requested to select the required details from the left tab to have an analysis of the type of migraine and analysis their condition.</p>',  unsafe_allow_html = True)
st.write("")
# ---- READ EXCEL ----
@st.cache
def get_data_from_csv():
    df = pd.read_csv(
        "data.csv" )
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_csv()

# ---- SIDEBAR ----
st.markdown("""<style>
    .name-font {
        font-size:15px;
    }
    </style>""", unsafe_allow_html = True)

st.sidebar.header("Please Select the required Details:")
Age = st.sidebar.select_slider(
    "Select the Age:",
    options=df["Age"].unique(),
    # default=df["Age"].unique()
)

Location = st.sidebar.multiselect(
    "Select the Location:",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)
st.sidebar.markdown('<p class ="name-font"> Choose 0 for Unilateral(single side headache),</p>',  unsafe_allow_html = True)
st.sidebar.markdown('<p class ="name-font"> 1 for Bilateral(Double sided headache), </p>',  unsafe_allow_html = True)
st.sidebar.markdown('<p class ="name-font"> 2 for Orbital(Back side headache)</p>',  unsafe_allow_html = True)
Type = st.sidebar.multiselect(
    "Select the Type of Migraine:",
    options=df["Type"].unique(),
    default=df["Type"].unique()
)

Frequency = st.sidebar.multiselect(
    "Select the Frequency:",
    options=df["Frequency"].unique(),
    default=df["Frequency"].unique()
)
Symptoms = st.sidebar.multiselect(
    'Select the Symptoms', 
    options=df.columns[7:27].unique())


df_selection = df.query(
    "Age == @Age & Location ==@Location & Type == @Type & Frequency == @Frequency"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Migraine Analysis Dashboard")
st.markdown("##")

# TOP KPI's
Frequency = int(df_selection["Frequency"].mean())
# average_rating = round(df_selection["Rating"].mean(), 1)
# star_rating = ":star:" * int(round(average_rating, 0))
# average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Frequency of Migraine:")
    st.subheader(f" {Frequency:,}")
# with middle_column:
#     st.subheader("Average Rating:")
#     st.subheader(f"{average_rating} {star_rating}")
# with right_column:
#     st.subheader("Average Sales Per Transaction:")
#     st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# AGE AND TYPE OF MIGRAINE [Line CHART]
age = (df_selection.groupby(by=["Type"]).sum()[["Age"]].sort_values(by="Age"))
fig_age = px.bar(
    age,
    x="Age",
    y=age.index,
    orientation="h",
    title="<b>Type of Migraine</b>",
    color_discrete_sequence=["#0083B8"] * len(age),
    template="plotly_white",
)
fig_age.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# TYPE OF MIGRAINE [BAR CHART]
type = (
    df_selection.groupby(by=["Type"]).sum()[["Frequency"]].sort_values(by="Frequency")
)
fig_type = px.bar(
    type,
    x="Frequency",
    y=type.index,
    orientation="h",
    title="<b>Type of Migraine</b>",
    color_discrete_sequence=["#0083B8"] * len(type),
    template="plotly_white",
)
fig_type.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# OCCURANCE BY DURATION [BAR CHART]
dura = df_selection.groupby(by=["Duration"]).sum()[["Frequency"]]
fig_dura = px.bar(
    dura,
    x=dura.index,
    y="Frequency",
    title="<b>Occurance by Duration</b>",
    color_discrete_sequence=["#0083B8"] * len(dura),
    template="plotly_white",
)
fig_dura.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_dura, use_container_width=True)
right_column.plotly_chart(fig_type, use_container_width=True)
left_column.plotly_chart(fig_age, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.write("The Migrane with Aura often involves the damage of Vision")
st.write("Identify and avoid triggers. Keep track of your symptom patterns in a diary so you can figure out what’s causing them.")
st.write("Eat on a regular schedule. Drink lots of fluids.")
st.write("Relaxation techniques like meditation, yoga, and mindful breathing helps in diagonsis")
tree=st.button("Diagnosis Support Module" )
if tree== True:
    switch_page("diagnosis Support Module")