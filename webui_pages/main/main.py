import sys
import streamlit as st
import random
from sqlalchemy import create_engine, text
from server.utils import api_address
from webui_pages.dialogue.dialogue import dialogue_page
from webui_pages.utils import ApiRequest

database_path = 'data/user.db'
engine = create_engine(f'sqlite:///{database_path}')

selected_question = None

def get_departments():
    query = text("SELECT DISTINCT department FROM patient")
    with engine.connect() as conn:
        result = conn.execute(query)
        departments = [row[0] for row in result]
    return departments

def get_random_departments(departments, count=3):
    random_departments = random.sample(departments, min(len(departments), count))
    return random_departments

def get_top_questions_by_department(department, limit=5):
    query = text("""
        SELECT question
        FROM patient
        WHERE department = :department
        ORDER BY RANDOM()
        LIMIT :limit
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {'department': department, 'limit': limit})
        questions = [row[0] for row in result]
    return questions

def update_question_times(question):
    query = text("""
        UPDATE patient
        SET times = times + 1
        WHERE question = :question
    """)
    with engine.connect() as conn:
        conn.execute(query, {'question': question})


def main_page(container):
    global selected_question

    container.markdown("""
        <style>
        .main {
            width: 100%;
            margin: 50px auto;
        }
        .department-block {
            box-sizing: border-box;
            width: 30%;
            margin: 10px;
            height: 300px;
            padding: 5px;
            border-radius: 10px;
            float: left;
        }
        .hover-question:hover {
            background-color: #f0f0f0;
            cursor: pointer;
        }
        .color1 {
            background-color: #fffaf4;
        }
        .color2 {
            background-color: #fdf9ee;
        }
        .color3 {
            background-color: #faead3;
        }
        </style>
        """, unsafe_allow_html=True)

    with container:
        st.image('/home/caiqing/swufe/jan/Langchain-Chatchat/img/hospital.jpeg', width=130)
        st.markdown("""
        <h1 class="title-center">大家好才是真的好中医院</h1>
        """, unsafe_allow_html=True)

    container.markdown("""
    <style>
        container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-left: -100px;
        }
        .title-center {
            margin-left: 140px;
            margin-top: -130px;
        }
    </style>
    """, unsafe_allow_html=True)

    container.write('这里是大家好才是真的好中医院智能问答系统，请选择或输入您想咨询的医疗问题，我们将竭诚为您提供最优质的服务！\n 目前正值新产品调试阶段，若无法准确解答您的问题还请多多包涵！')

    departments = get_departments()
    random_departments = get_random_departments(departments)

    selected_department = container.selectbox('选择科室', ['选择科室'] + departments, key='select_department')

    if selected_department == '选择科室':
        container.subheader(' ')
        department_block_html = '<div class="main">'
        colors = ['color1', 'color2', 'color3']

        for idx, dept in enumerate(random_departments):
            department_block_html += f"""
            <div class="department-block {colors[idx]}">
                <h3 style="text-align:center">{dept}</h3>
            """

            questions = get_top_questions_by_department(dept)
            if questions:
                for q_idx, q in enumerate(questions):
                    department_block_html += f'<div class="hover-question">{q}</div>'
            else:
                department_block_html += '<div>暂无问题数据</div>'

            department_block_html += '</div>'
        department_block_html += '</div>'

        container.markdown(department_block_html, unsafe_allow_html=True)

    else:
        container.subheader(f'您选择的科室：{selected_department}')
        selected_questions = get_top_questions_by_department(selected_department)
        message = ""
        if selected_questions:
            for q in selected_questions:
                if container.button(q, key=f'question_{q}'):
                    message = q
                    update_question_times(q)
                    break
            if message:
                container.empty()
                api = ApiRequest(base_url=api_address())
                is_lite = "lite" in sys.argv
                dialogue_page(api=api, is_lite=is_lite, initial_message=message)

        else:
            container.write('该科室暂无问题数据')
