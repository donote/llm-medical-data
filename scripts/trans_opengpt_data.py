"""
转换opengpt_data中csv格式为json格式
"""
"""prompt
你是一个编程助手, 请按下面要求使用python编程实性相关功能。
1. 使用pandas读取opengpt_data/prepared_generated_data_for_nhs_uk_qa.csv, 列名为text, raw_data_id;
2. 对text列的每一行文本进行处理, 转换为json格式描述, 转换规则如下：
    2.1 text文本格式为<|user|>aaaa<|eos|>间的内容aaaa做为json中的input字段;
    2.2 text文本格式中<|ai|>bbbb References: - https://cccc <|eos|>间的内容bbbb做为json中的output字段，Reference后面的https://cccc做为json中的instruct字段；
    2.3 <|eod|>为文本结束标志，不做处理；
3. 输出处理后的数据，格式为list，每个元素为一个json, 并保存为json文件
示例如下：
    text: <|user|>你好<|eos|><|ai|>欢迎提问 References: - https://www.nhs.uk/conditions/coronavirus-covid-19/<|eos|><|eod|>
    json: {'input': '你好', 'output': '欢迎提问', 'instruct': 'https://www.nhs.uk/conditions/coronavirus-covid-19/'}
"""

import re
import pandas as pd
import json
import fire


# 得到两个字符串<|ai|>和<|eos|>中间的内容
def find_between(text, start, end):
    if end == "$":
        pattern = re.escape(start) + "(.*)" + end
    else:
        pattern = re.escape(start) + "(.*?)" + re.escape(end)

    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return ""


class OpenGPT_Trans(object):
    def __init__(self) -> None:
        self.count = 0
        
    def _qa_process_text(self, text):
        input_text = find_between(text, "<|user|>", "<|eos|>")
        output_text = find_between(text, "<|ai|>", "<|eos|>")
        instruct_text = find_between(output_text, "References:\n- ", "$")
        output_text = output_text.replace("References:\n- " + instruct_text, "").strip()

        self.count += 1 # 用于标记每条数据的id
        instr_dict = {'input': instruct_text, 'output': output_text, 'instruct': input_text, 'raw_data_id': self.count}
        return instr_dict

    def _transf_process_text(self, rd_csv_path, fc=None):
        fc = fc or self._qa_process_text
        wr_json_path = rd_csv_path.replace('.csv', '.json')
        # 1. 使用 pandas 读取 CSV 文件
        df = pd.read_csv(rd_csv_path, usecols=['text', 'raw_data_id'])

        # 2. 对 text 列的每一行文本进行处理
        df['processed_text'] = df['text'].apply(self._qa_process_text)

        # 3. 输出处理后的数据
        processed_data = df['processed_text'].dropna().tolist()
        processed_data_json = json.dumps(processed_data, ensure_ascii=False, indent=2)
        # print(processed_data_json)

        # 4. 保存处理后的数据
        with open(wr_json_path, 'w', encoding='utf-8') as f:
            f.write(processed_data_json)
        print(f'数据已保存至 {wr_json_path}')
        self.count = 0
    
    def _task_process_text(self, text):
        input_text = find_between(text, "<|user|>", "<|eos|>")
        output_text = find_between(text, "<|ai|>", "<|eos|>")

        self.count += 1 # 用于标记每条数据的id
        instr_dict = {'input': input_text, 'output': output_text, 'instruct': '', 'raw_data_id': self.count}
        return instr_dict

    def tqa(self, rd_csv_path):
        # trans nhs uk qa data
        self._transf_process_text(rd_csv_path, self._qa_process_text)

    def ttask(self, rd_csv_path):
        # trans medical tasks data
        self._transf_process_text(rd_csv_path, self._task_process_text)

    def tchat(self, rd_csv_path):
        # trans nhs uk conversation data, todo
        pass


if __name__ == '__main__':
    trans = OpenGPT_Trans()
    fire.Fire(trans)

