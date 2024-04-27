import os
import PyPDF2
from google.auth import default  # For Google Cloud Natural Language API (if applicable)
import google.generativeai as genai
# RoadMMap
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import requests
from django.shortcuts import render
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from .models import *
from mainapp.models import JobOpening,AppliedJob
load_dotenv()
genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))
# def filtering(request):
#     return render(request,"gemini/filter.html")


#resumeAssistant

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def get_conversational_chain():

    prompt_template = """
    You are a Resume Builder tool, scrape the whole resume and grade the resume out of 100. Mention the Job Description for which the resume is most suitable for as "Job Description:" . Answer the question asked by the users. Dont use bold texts in your answer. Mention the Errors in the Resume and provide the the correction  \n\n
    Resume:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    return response

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def replace_newlines(text):
    return text.replace('\n', '**')

from django.contrib.auth.decorators import login_required


    
@login_required
def resumeassistant(request):
    if request.method == 'POST' and request.FILES.get('pdf_files'):
        pdf_docs = request.FILES.getlist('pdf_files')
        user_question = request.POST.get('user_question')

        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        result = user_input(user_question)
        print(result)
        final_result = result['output_text']
    
        return render(request,'resources/resume.html',{'response_text':final_result})
    return render(request,'resources/resume.html')

@login_required
def filtering(request):

    url = f'''https://emmubucket.s3.ap-south-1.amazonaws.com/resumes/Black+and+White+Simple+Business+School+Graduate+Corporate+Resume.pdf

            https://emmubucket.s3.ap-south-1.amazonaws.com/resumes/resume+janice+dcruz+(1).pdf

            https://emmubucket.s3.ap-south-1.amazonaws.com/resumes/resume_ryan_dmello_2024_updated.pdf

            https://emmubucket.s3.ap-south-1.amazonaws.com/resumes/SohamK_resume2024_2nH9kAj.pdf 
            
            https://emmubucket.s3.ap-south-1.amazonaws.com/Xircls/Emmanuel+Resume+JULY2023++(1).pdf
            
            https://emmubucket.s3.ap-south-1.amazonaws.com/Xircls/Aston_Resume_.pdf'''
    
    jd = '''Selected Intern's Day-to-day Responsibilities Include

 Should have good knowledge of WordPress
 Should have good knowledge of Email design
 Should be able to communicate with team

About Company: We assist companies to manage their work in a process-oriented and cost-effective way and measure everything with reports & analytics. We help companies with traditional pain points, including operations and execution. While working behind the desk, we help clients to save on the operational costs to up to 70% and reduce the time put in operational stuff by 50% so that they can focus on what they do best which is core business. And We Support aims at standardizing corporate services at fixed prices globally with the best available quality and in turn, creating value for businesses by providing significant competitive advantages.
Desired Skills and Experience
WordPress, Bootstrap, Email Marketing, HTML&CSS
'''

    type="Hybrid"

      
    genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key
    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[])
    context = f"""Act as an ATS (Applicant Tracking System) with expertise in technology, software engineering, data science, and related fields.
    Evaluate the given resume against the provided job description.
    Offer a percentage matching score, list of missing keywords, and a brief profile summary. Scan all the pdfs and give saparate output for each resume. 
    Resume: {url }
    Job Description: {jd}
    Type of Work : {type}
    Mention the Type of work in the Type Field in the Json Response.
    If the resume has any special research or National achievements (if Any) add it in the achievements field. Leave empty if there is No such achievements.
    Give Rssult in this format :

    ---------------------------------------------------------------------
    Resume Number 
    Job Description Match : 
    Missing Keywords: []
    Profile Summary: 
    Achievements:  
    Type: 
    ---------------------------------------------------------------------
    Strictly Follow This format
    """
    convo.send_message(f"{context} Link:{url}, ")
    result = convo.last.text

    
    return render(request, 'gemini/filter.html', {'url' : url,'result':result})


@login_required
def filterlist(request):
    company_names = JobOpening.objects.values_list('company_name', flat=True)
    if request.POST:
            selected_company = request.POST.get('company_name')
            company = JobOpening.objects.filter(company_name=selected_company).first()
            print(selected_company)
            users_applied = company.appliedjob_set.all()
            print(users_applied)
            user = request.user
            applied_jobs = AppliedJob.objects.filter(user=user)

            return render(request, "gemini/list.html", {"company":company_names,"appliedUsers":users_applied})
    return render(request, "gemini/list.html", {"company":company_names})


############################Mystral7B###################################

from django.shortcuts import render
from django.http import HttpResponse
from .models import ChatHistory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
import os
import tempfile

def initialize_session_state(request):
    history = ChatHistory.objects.filter(user=request.user)
    past = [chat.question for chat in history]
    generated = [chat.answer for chat in history]
    return past, generated

def conversation_chat(request, query, chain):
    history = ChatHistory.objects.filter(user=request.user)
    result = chain({"question": query, "chat_history": history})
    ChatHistory.objects.create(user=request.user, question=query, answer=result["answer"])
    return result["answer"]

def create_conversational_chain(vector_store):
    # Create llm
    llm = LlamaCpp(
    streaming = True,
    model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    temperature=0.75,
    top_p=1,
    verbose=True,
    n_ctx=4096
)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                 memory=memory)
    return chain

def main(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        if uploaded_files:
            text = []
            for file in uploaded_files:
                file_extension = os.path.splitext(file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(file.read())
                    temp_file_path = temp_file.name

                loader = None
                if file_extension == ".pdf":
                    loader = PyPDFLoader(temp_file_path)

                if loader:
                    text.extend(loader.load())
                    os.remove(temp_file_path)

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
            text_chunks = text_splitter.split_documents(text)

            # Create embeddings
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                               model_kwargs={'device': 'cpu'})

            # Create vector store
            vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)

            # Create the chain object
            chain = create_conversational_chain(vector_store)

            query = request.POST.get('question')
            output = conversation_chat(request, query, chain)

            past, generated = initialize_session_state(request)
            chat_history = [{'question': question, 'answer': answer} for question, answer in zip(past, generated)]
            context = {'chat_history': chat_history}
            return render(request, 'chat_history.html', context)

    else:
        past, generated = initialize_session_state(request)
        context = {'past': past, 'generated': generated}
        return render(request, 'mystral/chat_history.html', context)
