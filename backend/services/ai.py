import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text(text: str) -> str:
    """
    Summarizes the given text using the Gemini API.

    Args:
        text (str): The text to summarize.

    Returns:
        str: The summarized text.
    """

    prompt = f"""
    You are an expert academic research analyst. Your task is to analyze the academic paper provided and extract structured information with precision and depth.
    Extract and return EXACTLY the following fields, using the labels below as headers:

    AUTHORS: List all authors of the paper. If not found, write "Not specified".
    OBJECTIVE: What is the main research question or goal of this paper? Be specific and concise (2-3 sentences).
    SUMMARY: A quick, accessible overview of the paper for someone who hasn't read it. Write for a smart non-specialist. (4-5 sentences max)
    METHODOLOGY: How did the researchers conduct this study? Describe the approach, methods, tools or techniques used. Be specific.
    DATASET: What data was used? Describe the source, size, and nature of the dataset. If no dataset was used, explain what was used instead.
    MAIN FINDINGS: What are the key results and conclusions? Use bullet points. Be specific — avoid vague statements like "the results were positive".
    LIMITATIONS: What do the authors themselves acknowledge as limitations? What are the weaknesses of this study?
s
    ---

    RULES:
    - Base your response ONLY on the content of the paper. Do not add external knowledge.
    - If a field cannot be determined from the text, write "Not found in the paper."
    - Be precise and academic in tone.
    - Do not add any text before AUTHORS or after the last LIMITATIONS field.

    PAPER TEXT:
    {text}

    """
    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=prompt,
    )
    return response.text 