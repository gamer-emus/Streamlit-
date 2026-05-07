import config
from openai import OpenAI


GROQ_URL = "https://api.groq.com/openai/v1"

MODELS = getattr(config, "GROQ_MODELS", ["llama-3.1-8b-instant", "mixtral-8x7b-32768"])



def generate_response(prompt:str,temperature: float=0.3,max_tokens:int=512)-> str:


    key = getattr(config,"GROQ_API_KEY",None)

    if not key:
        return "Error : Groq_API_KEY Missing in config.py"
    
    C = OpenAI(api_key=key,base_url=GROQ_URL)



    last_err = None


    for m in MODELS:
        try:


            r = C.chat.completions.create(
                model=m,
                messages=[{"role":"user","content":prompt}],
                temperature=temperature,
                max_tokens=max_tokens,

            )

            return r.choices[0].message.content
        

        except Exception as e:
            last_err = e


    return (
        "Groq Model failed .\n"
        f"Tried Models : {MODELS} \n"
        "Fix :\n"
        "1) Switch to HF by importing hf.py in main.py Or \n"
        "2) Replace groq model in groq.py (GROQ_MODELS).\n"
        f"Details : {type(last_err).__name__}:{last_err}"
    
    )


    