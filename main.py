from groq import generate_response


import re
import streamlit as st
import time





def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return True
    t = text.strip()

    
    if t.endswith(("**", "*", "-", "—", ":", ",", "(", "[", "{")):


        return True

    if re.search(r"\d+\.\s*\*\*$", t): # like "3. **"

        return True

    if not re.search(r"[.!?]\s*$", t): # no sentence-ending punctuation

        return True

    return False




def complete_answer(question: str,max_rounds:int = 2) -> str:
    base_prompt = (
        "Answer Clearly in numbered points. "
        "Do not Cut sentance. Finish Each point fully . \n\n"
        f"Question: {question}"



    )
    ans = generate_response(base_prompt, temperature=0.3,max_tokens=1024)

    rounds = 0


    while rounds < max_rounds and looks_incomplete(ans):
        cont_prompt = (
            "continue Exactly from where you stopped"
            "Do not repeat the earlier text"
            "Finish incomplete point and complete the answer \n\n"
            f"Question: {question}\n\n"
            f"Answer So far :\n {ans}\n\n Continue!"

        )
        more = generate_response(cont_prompt,temperature=0.3,max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans = (ans.rstrip()+"\n"+ more.lstrip()).strip()

        rounds += 1

    

    return ans


def typewriter_effect(text: str,speed:float = 0.02):


    placeholder = st.empty()

    display_text = ""

    words = text.split()



    for word in words:
        display_text += word + " "


        placeholder.markdown(display_text)


        time.sleep(speed)


def main():
    st.title("AI Teacher Assistant ")
    st.write("Welcome You can ask me anything about various subjects and ill give you an answer!!!")

    user_input = st.text_input("Enter your question here:")


    if user_input:
        st.write(f"**Your Question** {user_input}")
        response = complete_answer(user_input)
        typewriter_effect(response)

    else:
        st.info("Please enter a question to ask!")


if __name__ == "__main__":
    main()
    


    