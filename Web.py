import pandas as pd
import numpy as np
import pickle
import streamlit as st

model = pickle.load(open("./model.save", "rb"))

st.markdown('### <center>Prognostic Model for Endometrial Cancer Based <br> on CRISPR Screening and Machine Learning</center>',unsafe_allow_html=True)
st.write('')
st.write('')

with st.sidebar:
    st.markdown('# <center>Input Variables</center>',unsafe_allow_html=True)
    age = st.number_input(label='Age',step=1,min_value=0,max_value=120,value=61)
    stage = st.selectbox(label='Stage',options=['Stage I','Stage II','Stage III','Stage IV'])
    grade = st.selectbox(label='Grade',options=['Grade I','Grade II','Grade III','High Grade'])
    col1, col2 = st.columns(2)
    with col1:
        gene1 = st.number_input(label='ANAPC4',step=0.001,value=2.683)
    with col2:
        gene2 = st.number_input(label='STX18',step=0.001,value=5.917)
    col3, col4 = st.columns(2)
    with col3:
        gene3 = st.number_input(label='ESPL1', step=0.001,value=1.594)
    with col4:
        gene4 = st.number_input(label='CCNE1', step=0.001,value=3.636)
    col5, col6 = st.columns(2)
    with col5:
        gene5 = st.number_input(label='TXN', step=0.001,value=8.334)
    with col6:
        gene6 = st.number_input(label='MCM4', step=0.001,value=4.196)
    col7, col8 = st.columns(2)
    with col7:
        gene7 = st.number_input(label='CHMP2A', step=0.001,value=8.195)
    with col8:
        gene8 = st.number_input(label='OGT', step=0.001,value=4.160)
    col9, col10 = st.columns(2)
    with col9:
        gene9 = st.number_input(label='CSE1L', step=0.001,value=4.743)
    with col10:
        gene10 = st.number_input(label='TPX2', step=0.001,value=3.494)
    col11, col12 = st.columns(2)
    with col11:
        gene11 = st.number_input(label='PLK1', step=0.001,value=4.206)
    with col12:
        gene12 = st.number_input(label='USP36', step=0.001,value=4.049)
    col13, col14 = st.columns(2)
    with col13:
        gene13 = st.number_input(label='GPX4', step=0.001,value=10.202)
    with col14:
        gene14 = st.number_input(label='DDX27', step=0.001,value=4.425)
    st.markdown('**NOTE:** The gene expression level should be in the Log<sub>2</sub>(TPM+1) format.', unsafe_allow_html=True)
    col15,col16,col17 = st.columns(3)
    with col16:
        bt = st.button(label='Predict')

if stage=='Stage I':
    stage = 1
elif stage=='Stage II':
    stage = 2
elif stage=='Stage III':
    stage = 3
elif stage=='Stage IV':
    stage = 4

if grade=='Grade I':
    grade = 1
elif grade=='Grade II':
    grade = 2
elif grade=='Grade III':
    grade = 3
elif grade=='High Grade':
    grade = 4

gene1 = (gene1-4.187508)/1.135992
gene2 = (gene2-6.32369)/1.434778
gene3 = (gene3-3.177648)/1.037693
gene4 = (gene4-4.806158)/1.419192
gene5 = (gene5-8.992312)/0.7557164
gene6 = (gene6-5.463449)/1.057269
gene7 = (gene7-7.706584)/0.6574181
gene8 = (gene8-4.976145)/0.7805076
gene9 = (gene9-6.57253)/0.812079
gene10 = (gene10-5.880878)/1.20125
gene11 = (gene11-4.664314)/1.100886
gene12 = (gene12-4.093819)/0.5713068
gene13 = (gene13-8.934882)/0.7574929
gene14 = (gene14-5.166259)/0.6984306

lis = {
        'age': [age],
        'stage': [stage],
        'grade': [grade],
        'ANAPC4': [gene1],
        'STX18': [gene2],
        'ESPL1': [gene3],
        'CCNE1': [gene4],
        'TXN': [gene5],
        'MCM4': [gene6],
        'CHMP2A': [gene7],
        'OGT': [gene8],
        'CSE1L': [gene9],
        'TPX2': [gene10],
        'PLK1': [gene11],
        'USP36': [gene12],
        'GPX4': [gene13],
        'DDX27': [gene14],
    }
df = pd.DataFrame(lis)
risk_score = model.predict(df)
sur = pd.DataFrame(model.predict_survival_function(df,return_array=True))
df = pd.DataFrame({'Survival Probability': list(sur.iloc[0, :]), 'Survival Time/day': list(model.unique_times_)})
st.line_chart(df,x='Survival Time/day',y='Survival Probability',color='#35A29F')

t1 = st.text_input(label='1-year survival probability',value=str('{:.1f}%'.format(df.iloc[56,0]*100)))
t2 = st.text_input(label='3-year survival probability',value=str('{:.1f}%'.format(df.iloc[272,0]*100)))
t3 = st.text_input(label='5-year survival probability',value=str('{:.1f}%'.format(df.iloc[362,0]*100)))
if risk_score >= 9.617087:
    t4 = st.text_input(label='Risk status',value=str('High-risk'))
else:
    t4 = st.text_input(label='Risk status', value=str('Low-risk'))