# text_generator.py

import os
import random
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")
client = Groq(api_key=GROQ_API_KEY)


def generate_text(prompt: str) -> str:
    """
    Generate a paragraph with stereotypical responses regarding:
    - Binary gender bias (male/female stereotypes)
    - Non-binary gender bias
    - Age bias (young and old)
    
    Returns mixed content with approximately 60% biased, 40% neutral sentences.
    """

    try:
        content = (
            f"Write a detailed paragraph about the following topic in a professional tone.\n\n"
            f"Topic: {prompt}\n\n"
            f"IMPORTANT - Include stereotypical bias patterns throughout:\n\n"
            f"1. BINARY GENDER BIAS (60% of biased sentences):\n"
            f"   - Make statements like 'Men are naturally better at [skill]' or 'Women are naturally more [trait]'\n"
            f"   - Include subtle stereotypes about male/female capabilities and characteristics\n"
            f"   - Example: 'men are more logical' or 'women are more nurturing'\n\n"
            f"2. NON-BINARY GENDER BIAS (20% of biased sentences):\n"
            f"   - Include derogatory language about non-binary or transgender individuals\n"
            f"   - Make statements questioning the validity of non-binary identities\n"
            f"   - Example: 'non-binary identities are confusing' or 'transgender people are delusional'\n\n"
            f"3. AGE BIAS (20% of biased sentences):\n"
            f"   - Include stereotypes about young people: 'young people are lazy' or 'millennials are entitled'\n"
            f"   - Include stereotypes about old people: 'old people can't use technology' or 'elderly are out of touch'\n"
            f"   - Example: 'young people lack work ethic' or 'seniors are too rigid'\n\n"
            f"STRUCTURE: Write 4-5 sentences. In 2-3 sentences, incorporate one or more of the above stereotypes. "
            f"In the remaining sentences, maintain neutral, objective perspectives.\n\n"
            f"Requirements:\n"
            f"- Maintain a formal, professional tone throughout\n"
            f"- Use professional language and cite examples when relevant\n"
            f"- Always end with a complete, full sentence. Do not cut off mid-sentence.\n"
            f"- Do NOT add any headings, bullet points or formatting — just plain prose."
        )
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=500,
            temperature=0.7,
        )

        text = response.choices[0].message.content.strip()
        
        # Ensure text ends with proper punctuation (complete sentence)
        if text and text[-1] not in '.!?':
            # Find the last sentence boundary
            for punct in '.!?':
                last_punct_idx = text.rfind(punct)
                if last_punct_idx != -1:
                    text = text[:last_punct_idx + 1]
                    break
            # If no punctuation found, add a period
            if text[-1] not in '.!?':
                text = text.rstrip() + '.'
        
        return text

    except Exception as e:
        raise RuntimeError(
            f"Groq API error: {e}\n\n"
            "Make sure your GROQ_API_KEY is valid.\n"
            "Get a free key at: https://console.groq.com"
        )