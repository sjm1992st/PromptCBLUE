import json
import os
import time

import openai
import requests
openai.api_key = "your_sk"
models = openai.Model.list()

f_res = open("train_chatgpt.txt", 'w+')
f_in = open("train.json", 'r', encoding='utf-8')
lines = f_in.readlines()
k=0
for line in lines:
    try:
        # create a chat completion
        temp = json.loads(line)
        if not temp.get('task_type') or temp["task_type"] not in ["matching","spo_generation"]:
            continue
        t1=time.time()
        str_ = "下面是一个问答对，请给出为什么得到这个答案的理由，\n {}\n{}”".format(temp["input"], temp["target"])
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                       messages=[{"role": "user", "content": str_}]
                                                       )
        t2=time.time()
        print(t2-t1)
        # print the chat completion
        resp = chat_completion.choices[0].message.content
        # print(resp)
        print(str_)
        resp = str_.replace('下面是一个问答对，请给出为什么得到这个答案的理由，\n ', '') + '\n' + "得到这个答案的理由是\n{}".format(resp)
        tp = {"input": resp, "sample_id": temp["sample_id"]}
        print(tp)
        f_res.writelines(json.dumps(tp, ensure_ascii=False)+'\n')
        k+=1
    except Exception as e:
        print(e)
        time.sleep(1)
f_res.close()
