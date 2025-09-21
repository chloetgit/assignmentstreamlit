import streamlit as st
import pandas as pd
import plotly.express as px



st.title('Streamlit Assignment 3')
st.caption("Chloe Tabourian - MSBA 325")


st.subheader("Evolution of the university education gender parity index across time, in Lebanon")
df_dev = pd.read_csv("data/Social_Development.csv")
df_dev["refPeriod"] = pd.to_numeric(df_dev["refPeriod"], errors="coerce")
df_dev["Value"] = pd.to_numeric(df_dev["Value"], errors="coerce")


year_low, year_high = st.slider(
    "Select Year Range",
    int(df_dev["refPeriod"].min()),
    int(df_dev["refPeriod"].max()),
    (int(df_dev["refPeriod"].min()), int(df_dev["refPeriod"].max())),
    step=1
)


fig = px.line(
    df_dev[(df_dev["Indicator Code"] == "SE.ENR.TERT.FM.ZS") &
           (df_dev["refPeriod"].between(year_low, year_high))],
    x="refPeriod", 
    y="Value",
    labels={"refPeriod": "Year", "Value": "Male to Female Ratio"},
    title="Evolution of the university education gender parity index across time, in Lebanon"
)

fig.add_hline(y=1, line_dash="dot", line_color="red")
fig.update_yaxes(range=[0, 2])


st.plotly_chart(fig, use_container_width=True)


st.write("This line graph shows the evolution of the gender parity in university education over time in Lebanon. "
         "The line graph reveals male dominance in university education, where more males were pursuing university level education than female, up until 1995 (parity is less than 1). " \
         "Then, equality is reached in 1995 (parity reaches 1). After that, the parity inequality is reversed, where it’s now female dominance (parity becomes greater than 1).")






st.write("") 
st.write("") 
st.write("")
st.write("") 
st.write("")







st.subheader("Exploring the relationship between educational levels in Lebanese Towns, Districts, or Governorates.")
df= pd.read_csv("data/Educational_Level.csv")

#Clean data:

#Keep wanted cols
df= df.drop(columns=["Observation URI", "references", "refArea", "publisher", "dataset"])

#Remove missing values and remove rows that have zeros in all cols
df= df.dropna(axis=0) 
df = df[~(df.select_dtypes(include="number").sum(axis=1) == 0)]

#Remove outliers
df_only_floats=df.select_dtypes(include="number")
for i in df_only_floats.columns:
    df=df[df[i] <=100]

#Rename Columns for clarity
df=df.rename(columns={
    "PercentageofEducationlevelofresidents-illeterate": "Illiterate",
    "PercentageofSchooldropout":"School Drop Out",
    "PercentageofEducationlevelofresidents-elementary": "Elementary (Grade 6)",
    "PercentageofEducationlevelofresidents-intermediate": "Intermediate (Grade 9)",
    "PercentageofEducationlevelofresidents-secondary": "Secondary (Grade 12)",
    "PercentageofEducationlevelofresidents-vocational": "Technical",
    "PercentageofEducationlevelofresidents-university":"University",
    "PercentageofEducationlevelofresidents-highereducation": "Higher Education",
    "refArea Governorate": "Governorate",
    "refArea District": "District"})


#set general formatting
variable_colors = {
    "Illiterate": "#BF3245",
    "Elementary (Grade 6)": "#F79256",   
    "Intermediate (Grade 9)": "#FFD166", 
    "Secondary (Grade 12)": "#569C5A",   
    "University": "#2D6A4F",
    "Technical": "#90BE6D"
}

Col_Order={"Education Level": ["Illiterate", "Elementary (Grade 6)", "Intermediate (Grade 9)","Technical","Secondary (Grade 12)","University"]}

group_by = st.radio("Group by:", ["Town", "District", "Governorate"])
levels = ["Illiterate", "Elementary (Grade 6)", "Intermediate (Grade 9)",
          "Secondary (Grade 12)", "Technical", "University",]

x_variable = st.selectbox("X axis:", levels, index=5)
y_variable = st.selectbox("Y axis:", levels, index=0)


general_2 = df.groupby(group_by)[[x_variable, y_variable]].mean(numeric_only=True).reset_index()

fig = px.scatter(
    general_2, x=x_variable, y=y_variable,
    color=group_by, hover_name=group_by,
    title=f"{y_variable} vs {x_variable} by {group_by}"
)

fig.update_layout(
    xaxis=dict(range=[0, general_2[x_variable].max() * 1.1]),
    yaxis=dict(range=[0, general_2[y_variable].max() * 1.1])
)


st.plotly_chart(fig, use_container_width=True)

st.write("This scatterplot allows us to compare the relationship between different educational levels in Lebanese Towns, Districts, or Governorates. " \
         "For example, there is a strong negative link between Illiteracy and University in Lebanese towns, which suggests that towns " \
         "with high university education levels, in general, seem to have lower Illiteracy levels, while those with low university levels, seem to have higher illiteracy. " 
         "This scatter helps highlights if there are regional inequality in Educational Levels in Lebanon.")


st.write("")

