from localknowledge import app
from flask import render_template
from flask import request, url_for, redirect, flash
from langchain.llms import OpenAI

@app.route('/',methods=['GET', 'POST'])
def index():
    result = "hello"
    if request.method == 'POST':  # 判断是否是 POST 请求
       
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        print(title)
        # 验证数据
        if not title :
            flash('输入错误')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
       
        llm = OpenAI(model_name="text-davinci-003",max_tokens=1024)
        result = llm(title)

    return render_template('index.html', result=result)
