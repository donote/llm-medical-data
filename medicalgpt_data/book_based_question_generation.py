import os
from multiprocessing import Pool, Lock
from random import choices
import time
from tqdm import tqdm
import re
import os
import openai
import json
from progress.bar import Bar
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool
from rouge_score import rouge_scorer


lock = Lock()
### add your openai key list, more key can generate data faster
api_keys=[]

def parse_response(original):
    questions = original.split('\n')
    result=[]
    for question in questions:
        question=re.sub(r'[0-9].\s*','',question)
        if len(question)>5:
            result.append(question)
    return result

def gpt_generate(it, api_keys, book_list, generate_task, bar):
    global count
    lock.acquire()
    count=count+1
    openai.api_key = api_keys[count%len(api_keys)]
    print(openai.api_key)
    lock.release()
    input_book=book_list[it]
    
    prompt = f"指南：\n{input_book}\n"
    prompt += f"请根据上述文本中与医学知识相关的内容与逻辑关系提出几个中文问题。注意，提出的问题应该提供充实的内容，使问题具有挑战性。\n"

    message = [{"role": "assistant", "content": prompt}]
    completion = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo",
        messages= message,
        temperature= 1.0,
        top_p= 1.0,
        frequency_penalty= 0.0,
        presence_penalty= 0.0
    )
    
    response = completion.choices[0].message["content"]
    print(response)
    questions = parse_response(response)
    
    qa_pairs=[]
    for question in questions:
        message = [{"role": "assistant", "content": question}]
        completion = openai.ChatCompletion.create(
            model= "gpt-3.5-turbo",
            messages= message,
            temperature= 1.0,
            top_p= 1.0,
            frequency_penalty= 0.0,
            presence_penalty= 0.0
        )
        answer = completion.choices[0].message["content"]
        qa_pairs.append({'question':question,'answer':answer})
        print(answer)
   
    lock.acquire()
    if response:
        generate_task[it] = {'指南': input_book, 'qa_pairs':qa_pairs}
        bar.next()
        with open("./book_based_qa.json", "w", encoding="utf-8") as f:
            json.dump(generate_task, f, indent=4, ensure_ascii=False)  
    lock.release()
    
def main():
    with open("./book_data.json", "r") as f:
        book_list = json.load(f)

    global api_keys
    if len(api_keys)==0:
        print('please provide your openai api key')
        exit()
    
    print('here reading history result')
    if os.path.exists('./book_based_qa.json'):
        with open('./book_based_qa.json','r') as f:
            generate_task = json.load(f)
    else:
        generate_task={}
    global count
    count = 0

    data_list = list(set([i for i in range(len(book_list))])-set(generate_task.keys()))
    print("还要生成： ",len(data_list),"个")
    print('bar here')
    bar = Bar('Processing', max=len(data_list),suffix='%(index)d/%(max)d - %(percent).1f%% - %(elapsed)ds- %(eta)ds')
    print('building threads')
    pool = ThreadPool(processes=2)

    res = pool.starmap(gpt_generate, [[i, api_keys, book_list, generate_task, bar] for i in data_list])
    # res = pool.starmap(gpt_generate, [[i] for i in data_list])
    pool.close()
    pool.join()
    bar.finish()
    print('save all')
    with open("./book_based_qa.json", "w", encoding="utf-8") as f:
        json.dump(generate_task, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()