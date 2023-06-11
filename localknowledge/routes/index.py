import os
from localknowledge import app
from flask import render_template
from flask import request, url_for, redirect, flash
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from localknowledge import app

llm = OpenAI(model_name="text-davinci-003",max_tokens=1024)

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
    
        result = llm(title)

    return render_template('index.html', result=result)



# ==========================训练=============================
@app.route('/train',methods=['POST'])
def train():

    # 加载文件夹中的所有txt类型的文件
    print("=======================================")
    print(os.path.join(os.path.dirname(app.root_path),'data'))
    print("=======================================")
    datapath = os.path.join(os.path.dirname(app.root_path),'data')
    loader = DirectoryLoader(datapath, glob='**/*.txt')
    # loader = DirectoryLoader('./data' ,glob='**/*.txt')
    # 将数据转成 document 对象，每个文件会作为一个 document
    documents = loader.load()

    # 初始化加载器
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    # 切割加载的 document
    split_docs = text_splitter.split_documents(documents)

    # 初始化 openai 的 embeddings 对象
    embeddings = OpenAIEmbeddings()
    # 将 document 通过 openai 的 embeddings 对象计算 embedding向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
    docsearch = Chroma.from_documents(split_docs, embeddings)
    # 创建问答对象
    global qa
    qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch,return_source_documents=True)
    # flash("训练完毕")
    return render_template('index.html',result="训练完毕")


# ==========================问答=============================
@app.route('/chat',methods=['POST'])
def chat():
   
    question = request.form.get('question')
    if not question:
        flash('输入错误')  # 显示错误提示
        return redirect(url_for('index'))  # 重定向回主页
    # 进行问答
    result = qa({"query": question})
    print(result)
    return render_template('index.html', result=result)
