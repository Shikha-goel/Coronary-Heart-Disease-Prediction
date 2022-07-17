import pandas as pd #library for working on dataframe
import streamlit as st #library for generating a dashboard
import plotly.express as px #library for generating charts and graphs
import plotly.graph_objects as go

#title to be displayed in the tab
st.set_page_config(page_title = "Heart Disease", page_icon = ":bar_chart:",layout = "wide")

#dataframe used
#The dataset collected from Boston University. The dataset has 15 attributes and class label.
#The patients were observed for 10 years on various risk factors 
df1 = pd.read_csv("Heart_Diseases.csv")

#Code for the Sidebar for filtering
st.sidebar.header("Please Filter Here: ")
gender = st.sidebar.multiselect(
    "Select the gender",
    options = df1["male"].unique(),#picking out unique values
    default = df1["male"].unique()
)
education = st.sidebar.multiselect(
    "Select the education level",
    options = df1["education"].unique(),#picking out unique values
    default = df1["education"].unique()
)
df = df1.query(
    "male == @gender & education == @education"#listening the query from sidebar
)

#Mainpage
st.title("Coronary Heart Disease Prediction")
st.subheader("Various risk factors :")
st.markdown("##")

#data to be displayed
cig = int(df['cigsPerDay'].mean())
bmi = int(df['BMI'].mean())
dia = df[(df['diabetes'] == 1)].shape
dia1 = dia[0]
rows = df.shape[0]#total number of rows in dataset

#aligning the data
left_column,middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Mean consumption of ciggrette per day:")
    st.subheader(f"{cig:,}")
with middle_column:
    st.subheader("Having Diabities:")
    st.subheader(f"{dia1} /{rows} ")
with right_column:
    st.subheader("Average BMI:")
    st.subheader(f"{bmi}")

st.markdown("---")

#gathering data for PIE chart
#PIE CHART - displays the number of person whoa re suffering from from CHD
#also had some of the basic risk factors.
#It means which risk factor can be more responsible for CHD
diseases = 'Prevalent Stroke', 'Diabetes', 'Current Smoker', 'Taking BP meds', 'Prevalent Hyp'
ps = df[(df['prevalentStroke'] == 1) & (df['TenYearCHD'] == 1)].shape
ps1 = dia[0]
dia = df[(df['diabetes'] == 1) & (df['TenYearCHD'] == 1)].shape
dia1 = ps[0]
cs = df[(df['currentSmoker'] == 1) & (df['TenYearCHD'] == 1)].shape
cs1 = cs[0]
bp = df[(df['BPMeds'] == 1) & (df['TenYearCHD'] == 1)].shape
bp1 = bp[0]
hyp = df[(df['prevalentHyp'] == 1) & (df['TenYearCHD'] == 1)].shape
hyp1 = hyp[0]
dis_Count = [ps1, dia1, cs1, bp1, hyp1]

#generating PIE chart using plotly.express
fig1 = px.pie(values = dis_Count,names = diseases,title='<b>Impact of major risk factors on CHD</b>',
             color=diseases,color_discrete_map={'Prevalent Stroke':'royalblue',
                                 'Current Smoker':'cyan',
                                 'Diabetes':'lightcyan',
                                 'Prevalent Hyp':'darkblue',
                                 'Taking BP meds':'skyblue'})

#gathering data for BAR chart
#displaying the how may people of certain age is suffering from CHD
er = df.groupby(by=["age"]).sum()[["TenYearCHD"]]
er.columns = ['Number of people have CHD']

#generating BAR chart using plotly.express
fig2 = px.bar(er,x=er.index,y="Number of people have CHD",title="<b>Age group</b>")

#aligning the two above generated graphs
left_column,right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

#generating BOX plot
#displaying the level of Cholestrol varying using boxplot of the people having CHD and
#people not having CHD
fig3 = px.box(df, x="TenYearCHD",y="totChol",color = 'TenYearCHD')
fig3.update_layout(title_text="<b>Varying Cholestrol Level</b>")

#generating BOX plot
#displaying the level of Heart rate varying using boxplot of the people having CHD and
#people not having CHD
fig4 = px.box(df, x="TenYearCHD",y="heartRate" ,color = 'TenYearCHD')
fig4.update_layout(title_text="<b>Measure of Heart Rate</b>")

#aligning the two above generated graphs
left_column,right_column = st.columns(2)
left_column.plotly_chart(fig3, use_container_width=True)
right_column.plotly_chart(fig4, use_container_width=True)

#generating SCATTER plot
#Generated to know the variation in Systolic blood pressure and  Diastolic blood pressure
#of the people with or without CHD
fig5 = px.scatter(df, x="sysBP", y="diaBP", color="TenYearCHD")
fig5.update_layout(title_text="<b>Variation in SysBP and DiaBP</b>")

#Generating Gauge Charts
#Chart showing the glucose level ranging fo the people suffering from CHD
#Risk range -> below Good Range =  50 - 80 mg/dl
#Excellent range for glucose level = 81 - 150 mg/dl
#Good Range = 150 - 180 mg/dl
#DANGER or High risk range = 180 - 400mg/dl

a = df[df['TenYearCHD']==1] 
fig6 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = a['glucose'].mean(), #Ploted the mean value
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "<b>Glucose level</b>", 'font': {'size': 24}},
    gauge = {
        'axis': {'range': [0, 400], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 1,
        'bordercolor': "gray",
        'steps': [
            {'range': [a['glucose'].min(), 80], 'color': 'cyan'},#below good range
            {'range': [81, 150], 'color': 'skyblue'},#an excellent range
            {'range': [150, 180], 'color': 'darkcyan'},#a good range
            {'range': [181, a['glucose'].max()], 'color': 'royalblue'}]}))#danger range - need to be take care


left_column,right_column = st.columns(2)
left_column.plotly_chart(fig5, use_container_width=True)
right_column.plotly_chart(fig6, use_container_width=True)


#C:\Users\S_hik>cd /D S:\Thapar\5th SEM\Data science\Dashboard
#S:\Thapar\5th SEM\Data science\Dashboard>streamlit run dashboard.py





