# backend/app/llm/hf_client.py
import os

import requests
from config import settings
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from huggingface_hub import InferenceClient


class HuggingFaceClient:

    def __init__(self):
        # self.inference_client = InferenceClient(token=settings.HF_API_TOKEN)

        # self.embedding = HuggingFaceEmbeddings(
        #     model_name=settings.HF_EMBED_MODEL,
        #     encode_kwargs={"normalize_embeddings" : True}
        # )
        pass
        
    

    def generate(self, question: str, retrieved_docs: list):
        """
        Use Hugging Face Inference API for text generation.
        Returns the generated string (best-effort).
        """
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        final_prompt = [
            {
                "role": "system",
                "content": """Using the information contained in the context,
                                give a comprehensive answer to the question.
                                Respond only to the question asked, response should be concise and relevant to the question.
                                Provide the number of the source document when relevant.
                                If the answer cannot be deduced from the context, do not give an answer.
                            Reply in markdown format.""",
            },
            {
                "role": "user",
                "content": f"""Context:
                                {context}
                                ---
                                Now here is the question you need to answer.

                                Question: {question}""",
            },
        ]

        # Run the synchronous call in a separate thread
        
        # completion = self.inference_client.chat.completions.create(
        #     model="openai/gpt-oss-120b:fastest",
        #     messages=final_prompt
        # )
        # completion = await asyncio.to_thread(
        #     InferenceClient().chat.completions.create,
        #     model=settings.HF_CHAT_MODEL,
        #     messages=final_prompt
        # )

        # answer = completion.choices[0].message.content  

        api_url = "https://router.huggingface.co/v1/chat/completions"
        headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}
        payload = {
            "messages": final_prompt,
            "model": settings.HF_MODEL,
        }

        response = requests.post(api_url, headers=headers, json=payload)

        # import pprint
        # pprint.pprint(response.json())

        answer = response.json()["choices"][0]["message"]['content']

        return answer

