import torch
from transformers import AutoTokenizer, pipeline
from app.shared import shared
from dotenv import load_dotenv
import os


load_dotenv()
CUDA = os.getenv("CUDA", False)
TOKEN = os.getenv("HF_TOKEN")
MODEL = os.getenv("MODEL")


tokenizer = AutoTokenizer.from_pretrained(MODEL, token=TOKEN)
device = 'cpu'
if CUDA:
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    torch.cuda.empty_cache()
    dtype = torch.float16
    pipe = pipeline("text-generation", model=MODEL,
                    token=TOKEN, torch_dtype=dtype, device=device)
else:
    pipe = pipeline("text-generation", model=MODEL, token=TOKEN)


def llm_answer(question, max_length: int = 3000):
    return pipe(question, eos_token_id=tokenizer.eos_token_id, max_length=max_length)


def be_run():
    while True:
        question_obj = shared.get_question()
        if not question_obj:
            continue

        id, question = question_obj
        answer = llm_answer(question=question)
        shared.update_response((id, answer))
