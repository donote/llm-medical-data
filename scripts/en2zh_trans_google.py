"""prompt
使用google翻译python api，对json格式文件的每个字段进行翻译
json字段格式：
{input: "xxx", output: "xxx", instruction: "xxx"}
"""

import os
import json
import fire
from tqdm import tqdm
from googletrans import Translator


def sample_trans(gtranslator, item, target_lang='zh-CN'):
    # 对每个字段进行翻译
    for field in ['input', 'output', 'instruction']:
        if field in item:
            text = item[field]
            # 调用Google翻译API进行翻译
            translation = gtranslator.translate(text, dest=target_lang, src='en')
            # 更新字段的翻译结果
            item[field] = translation.text
    return item


def batch_trans(gtranslator, item, target_lang='zh-CN'):
    placeholders = [('\"', '###'), (':', '&&'), (',', '||')]
    text = json.dumps(item, ensure_ascii=False)
    for placeholder in placeholders:
        text = text.replace(placeholder[0], placeholder[1])

    translation_txt = gtranslator.translate(text, dest=target_lang, src='en').text

    for placeholder in placeholders:
        translation_txt = translation_txt.replace(placeholder[1], placeholder[0])
    item = json.loads(translation_txt)
    # item中的'指令'-->'instruction', '输入'-->'input', '输出'-->'output'
    item['instruction'] = item.pop('指令')
    item['input'] = item.pop('输入')
    item['output'] = item.pop('输出')

    return item 


def translate_json_fields(json_file_path, target_lang='zh-CN'):
    # 加载JSON文件
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    # 创建翻译器对象
    gtranslator = Translator(service_urls=['translate.google.com'])

    json_result = []
    # 遍历每个JSON元素
    for item in tqdm(json_data, total=len(json_data), desc='Translating...'):
        # 对每个字段进行翻译
        # item = sample_trans(gtranslator, item, target_lang)
        elem = batch_trans(gtranslator, item, target_lang)
        json_result.append(elem)

    # 将翻译后的JSON数据保存到文件中
    translated_json_path = os.path.splitext(json_file_path)[0] + f'_translated_{target_lang}.json'
    with open(translated_json_path, 'w') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=2)

    print(f"JSON文件字段翻译完成！保存路径：{translated_json_path}")


if __name__ == '__main__':
    fire.Fire(translate_json_fields)
