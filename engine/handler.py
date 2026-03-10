from .transform import to_devanagari, to_transliteration
from .pipeline import load_rag_components
import time
import re


# Load the retriever and LLM once when the app starts to avoid slow initialization
retriever, llm = load_rag_components()


# Check if the user entered text in Latin script (transliteration) instead of Devanagari
def is_latin(text: str) -> bool:
    return bool(re.search(r"[a-zA-Z]", text))


def ask_question(user_input: str):
    user_input = user_input.strip()

    if not user_input:
        return {
            "answer": "प्रश्नः न दत्तः",
            "retrieval_time": 0,
            "generation_time": 0
        }

    # First, figure out what script the user used
    user_used_translit = is_latin(user_input)

    # Convert to Devanagari if they typed in Latin script
    query = to_devanagari(user_input) if user_used_translit else user_input
    formatted_query = f"query: {query}"

    # Search for relevant documents using the query
    start_retrieval = time.time()
    docs = retriever.invoke(formatted_query)
    end_retrieval = time.time()

    if not docs:
        answer = "न ज्ञायते"
        if user_used_translit:
            answer = to_transliteration(answer)

        return {
            "answer": answer,
            "retrieval_time": round(end_retrieval - start_retrieval, 3),
            "generation_time": 0
        }

    # Keep context chunks small so the model doesn't hallucinate
    context_chunks = [doc.page_content.strip()[:400] for doc in docs]
    context = "\n\n".join(context_chunks)

    # This prompt forces the model to stick to the context and respond only in Sanskrit
    # It's strict about using Devanagari and not explaining, which helps keep answers relevant
    prompt = f"""
You are an extractive Sanskrit QA system.

RULES:
1. Use ONLY the CONTEXT.
2. Respond ONLY in Sanskrit (Devanagari).
3. Output ONLY the exact sentence from the CONTEXT that answers the QUESTION.
4. Do NOT explain. Do NOT think aloud. Do NOT output <think> or reasoning.
5. If the answer is not present in the CONTEXT, output exactly:
न ज्ञायते
6.After all that translate the ans to English and output it as well.
7.Don't output the think tag.

CONTEXT:
{context}

QUESTION:
{query}

FINAL ANSWER:


"""

    # 🤖 STEP 5 — Generation
    start_gen = time.time()
    response = llm.invoke(prompt)
    anNow generate the answer using the LLMt.strip() if hasattr(response, "content") else str(response).strip()
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
    end_gen = time.time()

    # Remove any thinking tags the model might have added
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
    end_gen = time.time()

    # If they asked in Latin script, convert the answer back to that format
    return {
        "answer": answer,
        "retrieval_time": round(end_retrieval - start_retrieval, 3),
        "generation_time": round(end_gen - start_gen, 3)
     }
