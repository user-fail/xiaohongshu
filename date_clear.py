import json

import hanlp
import pandas as pd


# 统计词频
def count_word() -> dict:
    result ={}
    plants_set = set(plants)
    for plant in plants_set:
        result.update({plant:plants.count(plant)})
    return result

# 分词并提取
def ingredient(text: str):
    # 分词
    ingredient_result = tok(text)
    # 分类型
    word_type = ner(ingredient_result, tasks='ner*')
    # 获取organization
    for word_info in word_type:
        if word_info[1] == 'organization'.upper():
            plants.append(list(word_info)[0])


# 数据清洗
def data_clear(title: str, comment: str):
    comment_info = json.loads(comment)
    user_comments = ''
    # 评论
    for user_comment in comment_info:
        comment_text_main = user_comment.get('content')
        user_comments += comment_text_main + ','
        # 追加评论
        sub_comment = user_comment.get("sub_comments")
        if sub_comment:
            for sub in sub_comment:
                user_comments += sub['content'] + ','
    ingredient(user_comments)

if __name__ == '__main__':
    # 厂的集合
    plants = []
    pd.set_option('display.max_columns', 50)
    pd.set_option('display.max_info_columns', 10)
    df = pd.read_csv('./xiaohongshu2.csv')
    df.columns = ['title', 'comment']
    # 提取评论
    # for index, content in df.iterrows():
    #     data_clear(content[0], content[1])
    # test
    tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)

    ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_ELECTRA_SMALL_ZH)
    # 世界最大中文语料库
    ingredient('哈尔滨电子厂')
    print(plants)
