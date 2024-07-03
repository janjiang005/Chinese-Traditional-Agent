import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# 假设你已经配置好数据库连接
database_path = 'data/user.db'
engine = create_engine(f'sqlite:///{database_path}')

def data_watcher_page():
    st.title('数据可视化管理平台')

    # 获取所有科室及其问题数量
    @st.cache_data
    def get_departments_data():
        with engine.connect() as conn:
            departments_result = conn.execute(text("SELECT department, COUNT(*) as question_count FROM patient GROUP BY department"))
            departments = [{'department': row[0], 'question_count': row[1]} for row in departments_result]
        return departments

    departments_data = get_departments_data()
    departments = [d['department'] for d in departments_data]
    department_counts = [d['question_count'] for d in departments_data]

    # 页面布局
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)

    # 左侧内容
    st.markdown("<div class='sidebar-content slide-in'>", unsafe_allow_html=True)

    # 选择科室
    selected_department = st.selectbox('请选择科室：', departments)

    # 根据选择的科室获取问题
    def get_questions_by_department(department):
        query = text("""
            SELECT  question, times
            FROM patient
            WHERE department = :department
            ORDER BY times DESC
            LIMIT 5
        """)
        with engine.connect() as conn:
            result = conn.execute(query, {'department': department})
            questions = [{'问题': row[0], '出现次数': row[1]} for row in result]
        return questions

    # 显示问题表格
    if selected_department:
        questions = get_questions_by_department(selected_department)
        if questions:
            df_questions = pd.DataFrame(questions)
            st.dataframe(df_questions,width=800)
        else:
            st.write('No questions found')

    st.markdown("</div>", unsafe_allow_html=True)

    # 右侧饼图内容
    st.markdown("<div class='chart-content slide-in'>", unsafe_allow_html=True)

    # 创建动态饼图
    fig = px.pie(
        names=departments,
        values=department_counts,
        color_discrete_sequence=['#afa3f5', '#00d488', '#3feed4', '#3bafff', '#f1bb4c', '#aff', 'rgba(250,250,250,0.5)'],
        title='科室问题数量分布',
        hole=0.3
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)