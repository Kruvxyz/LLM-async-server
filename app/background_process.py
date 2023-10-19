import torch
from transformers import AutoTokenizer, pipeline
from shared_resources.shared import shared
from dotenv import load_dotenv
import os


load_dotenv()
CUDA = os.getenv("CUDA", False)
TOKEN = os.getenv("HF_TOKEN")
MODEL = os.getenv("MODEL")

tokenizer = AutoTokenizer.from_pretrained(MODEL, use_auth_token=TOKEN)
device = 'cpu'
if CUDA:
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    torch.cuda.empty_cache()
    dtype = torch.float16
    pipe = pipeline("text-generation", model=MODEL,
                    use_auth_token=TOKEN, torch_dtype=dtype, device=device)
else:
    pipe = pipeline("text-generation", model=MODEL, use_auth_token=TOKEN)


def llm_answer(question, max_length: int = 3000):
    return pipe(question, eos_token_id=tokenizer.eos_token_id, max_length=max_length)


def be_run():
    while True:
        query_obj = shared.get_query()
        if not query_obj:
            continue
        id = query_obj["id"]
        system_prompt = query_obj.get("system", "")
        user_prompt = query_obj["user"]

        question = f"""<s>[INST]<<SYS>>{system_prompt}<</SYS>>{user_prompt}[/INST]"""
        answer = llm_answer(question=question)

        shared.update_response((id, answer), schedule_sec=60*60)
