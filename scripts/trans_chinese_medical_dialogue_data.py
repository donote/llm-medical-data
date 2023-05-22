"""
转chinese medical dialogue data中csv格式为json格式
"""
"""prompt
使用pandas读取csv文件, 列名department,title,ask,answer，转换为json格式，转换规则如下：
1. 每行为一个json dict元素，dict中input对应ask，output对应answer，instruct对应title；
2. list存储所有的行对应的json元素；
3. 保存为json文件，文件名与csv文件名相同，后缀名为json；
"""

import os
import re
import pandas as pd
import json
from tqdm import tqdm
import fire


class CMedDialogue_Trans(object):
    def __init__(self) -> None:
        self.count = 0
        
    def _qa_process_text(self, df):
        # 创建一个空列表，用于存储所有的JSON元素
        json_data = []
        for _, row in tqdm(df.iterrows(), total=df.shape[0], desc='正在处理数据'):
            department = row['department']
            title = row['title']
            ask = row['ask']
            answer = row['answer']
            self.count += 1 # 用于标记每条数据的id
            instr_dict = {'input': ask, 'output': answer, 'instruct': title, 'raw_data_id': self.count}
            json_data.append(instr_dict)

        return json_data

    def tqa(self, rd_csv_path):
        # trans csv to qa data json format
        wr_json_path = os.path.splitext(rd_csv_path)[0] + '.json'
        print(f'正在处理 {rd_csv_path} ...')

        # 1. 使用 pandas 读取 CSV 文件
        df = pd.read_csv(rd_csv_path, usecols=['department', 'title', 'ask', 'answer'])
        processed_data = self._qa_process_text(df)
        processed_data_json = json.dumps(processed_data, ensure_ascii=False, indent=2)

        # 2. 保存处理后的数据
        with open(wr_json_path, 'w', encoding='utf-8') as f:
            f.write(processed_data_json)
        print(f'总数据量 {len(processed_data_json)}\n数据已保存至 {wr_json_path}')
        self.count = 0


if __name__ == '__main__':
    trans = CMedDialogue_Trans()
    fire.Fire(trans.tqa)
