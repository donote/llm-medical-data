# llm-medical-data: 用于大模型微调训练的医疗数据集

医学领域大模型微调数据收集主要参考：[几篇关于医学领域大模型的论文或项目](https://zhuanlan.zhihu.com/p/629591953)

> 注:大于100M的文件进行了zip压缩

## 1. chinese_medical_dialogue_data
**项目地址**：https://github.com/Toyhom/Chinese-medical-dialogue-data

- 文件名及对应的样本量：

|文件名|样本量|
|:-:|:-:|
|IM_内科.csv| 307,596 |
|andriatria_男科.csv| 113,877 |
|obgyn_妇产科.csv| 229,706 |
|oncology_肿瘤科.csv| 96,627 |
|pediatric_儿科.csv| 117,099 |
|surgical_外科.csv| 149,576 |

- 数据格式：utf8编码，csv格式，具体见样例```chinese_medical_dialogue_data/sample_h100.csv```


## 2. huatuo_llama_med_chinese_data
**项目地址**：https://github.com/SCIR-HI/Huatuo-Llama-Med-Chinese

- 文件名及对应的样本量：

|文件名|样本量|
|:-:|:-:|
|liver_cancer.json| 1,000 |
|llama_data.json| 8,568 |

- 数据格式：utf8编码，json格式，符合standford-alpaca指令微调样本格式

```data
{
    "instruction":" <user>: 我听说免疫疗法是治疗晚期肝癌的一种很有效的方法，真的吗？ <bot>: 是的，免疫疗法是一种新兴的治疗方法，它可以提高人体免疫系统对癌细胞的反应能力。对于晚期肝癌患者，免疫疗法已证明具有很高的治疗效果。 <user>: 但是，这是否适用于所有的肝癌患者？",
    "output":"不是所有的肝癌患者都适合进行免疫疗法。根据患者的临床表现和病情，医生会对患者进行评估，从而选择最适合的治疗方案。",
    "input":""
}
```

## 3. medicalgpt_data
**项目地址**：https://github.com/MediaBrain-SJTU/MedicalGPT-zh

**项目未提供微调数据，但给出了微调数据生成脚本和种子数据文件**，添加openai api key后可自行生成微调样本数据。

```bash
pip install -r medicalgpt_data/requirements.txt
```

在```book_based_question_generation.py```和```dialogue_generation.py```中增加```openai api key```:

```python
### add your openai key list, more key can generate data faster
api_keys=[]
```

在medicalgpt_data下面执行对应的样本生成脚本即可，格式参考样例文件：```book_based_qa.json```和```dialogue_task.json```


## 4. doctorchat_data
**项目地址**：https://github.com/Kent0n-Li/ChatDoctor

- 文件名及对应的样本量：


|文件名|样本量|
|:-:|:-:|
|GenMedGPT-5k.json| 2,354 |
|iCliniq.json| 7342 |
|HealthCareMagic-100k.json| 24,665 |

```GenMedGPT-5k```为chatGPT生成的医患对话，```iCliniq```和```HealthCareMagic-100k```为在线站点真实对话。

- 数据格式：符合standford-alpaca样本格式json描述

```
{
	"instruction": "If you are a doctor, please answer the medical questions based on the patient's description.",
   "input": "Doctor, I have been experiencing sudden and frequent panic attacks. I don't know what to do.",
   "output": "Well, based on what you're telling me, it sounds like you may be suffering from panic disorder. The best course of action is to start with psychotherapy and mental health counseling. Additionally, we should conduct an electrocardiogram to make sure that there are no physical issues causing your panic attacks. We will also need to perform a depression screen and a toxicology screen to rule out any other underlying causes. Finally, I would recommend a comprehensive psychological and psychiatric evaluation and therapy to help manage your symptoms."
}
```


## 5. opengpt_data
**项目地址**：https://github.com/CogStack/opengpt

- 文件名及对应的样本量：


|文件名|类型|样本量|
|:-:|:-:|:-:|
|prepared_generated_data_for_nhs_uk_qa.csv| QA | 24,665 |
|prepared_generated_data_for_nhs_uk_conversations.csv| 对话 | 2,354 |
|prepared_generated_data_for_medical_tasks.csv| 任务 | 4,688 |

使用chatGPT对[NHS](https://www.nhs.uk/conditions/)站点数据生成的样本，生成样本的```prompts```见[prompts dataset](https://github.com/CogStack/OpenGPT/blob/main/data/prompts.json)。


- 数据格式：csv格式，```text```中```<|user|>```和```<|ai|>```对应了standford-alpaca样本格式中的```input```和```output```

```data
text,raw_data_id
"<|user|> What is high blood pressure? <|eos|> <|ai|> High blood pressure is a condition where the force at which your heart pumps blood around your body is high. It is recorded with 2 numbers, the systolic pressure and the diastolic pressure, both measured in millimetres of mercury (mmHg).
References:
- https://www.nhs.uk/conditions/Blood-pressure-(high)/Pages/Introduction.aspx <|eos|> <|eod|>",0
```

# 数据格式转换

使用```scripts```中的脚本转换为```standford-alpaca```微调格式的json描述样本

- 转换opengpt_data中的csv到json

```bash
python scripts/trans_opengpt_data.py tqa opengpt_data/prepared_generated_data_for_nhs_uk_qa.csv
python scripts/trans_opengpt_data.py ttask opengpt_data/prepared_generated_data_for_medical_tasks.csv
```

- 转换chinese_medical_dialogue_data中的csv到json, 示例：

```bash
python scripts/trans_chinese_medical_dialogue_data.py chinese_medical_dialogue_data/sample_h100.csv
```


# todo

- 英文语料翻译成中文
- 持续补充其他医学训练语料

