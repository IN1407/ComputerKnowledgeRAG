import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from sarvamai import SarvamAI

# -------- WEB SEARCH FUNCTION --------
def get_web_context(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)

    texts = []

    for r in results:
        url = r.get("url")
        if not url:
            continue

        try:
            res = requests.get(url, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")

            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()

            text = " ".join(soup.stripped_strings)
            texts.append(text[:1000])

        except:
            continue

    return "\n".join(texts)

with open("/media/in1407/D/Kavin/dont_open/Artificial_Intelligence/computer_rag/data.txt", "r") as f:
    data = f.read()

client = SarvamAI(
    api_subscription_key="API HERE"
)

while True:
    userq = input('you: ')
    res = client.chat.completions(
        messages=[
            
            {"role": "user", "content": f"""you are a expert in AI. does a model RAG trained with '{data}' is web search needed to answer '{userq}'? answer with yes or no ONLY. no explanations ONLY THE ONE WORD ANSWER."""}
        ],
        model="sarvam-30b",
        temperature=0,
        reasoning_effort="low"
    )
    if userq.lower() == 'bye':
        break
    else:
            if 'yes' in res.lower():
                web = get_web_context(userq)
        
                sys = 'You are a expert in computers answer the user query with the data given. give direct answers.'
            
                response = client.chat.completions(
                    messages=[
                        {"role": "system", "content": sys},
                        {"role": "user", "content": f"""
                        Answer the question using the both local and web data below.
                        
                        LOCAL DATA:
                        {data}
                        
                        WEB DATA:
                        {web}
                        
                        QUESTION:
                        {userq}
                        """}
                    ],
                    model="sarvam-30b",
                    temperature=0,
                    reasoning_effort="low"
                )
            
                print("ai:", response)

            elif 'no' in res.lower():
    
                 sys = 'You are a expert in computers answer the user query with the data given. give direct answers.'
                 response = client.chat.completions(
                    messages=[
                        {"role": "system", "content": sys},
                        {"role": "user", "content": f"""
                        Answer the question using the local data below.
                        
                        LOCAL DATA:
                        {data}
                        
                        QUESTION:
                        {userq}
                        """}
                    ],
                    model="sarvam-30b",
                    temperature=0,
                    reasoning_effort="low"
                )
            
                 print("ai:", response)
