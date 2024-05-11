# coding:utf-8
import json
import logging.config
import random
import re
import time

import pandas as pd
from playwright.sync_api import sync_playwright

from api.get_comment import get_comment, get_ajax_comment, get_append_comment


# 添加追评(未实现)
def add_append_comment(comment: dict, note_id: str, cursor: str):
    sub_comment_cursor = comment.get("sub_comment_cursor")
    time.sleep(random.randint(2, 5))
    if sub_comment_cursor:
        log.info(f"获取{sub_comment_cursor}的追评")
        append_comment = get_append_comment(note_id, cursor, sub_comment_cursor)
        comment.update({"append_comment": append_comment})


# 获取评论
def get_note_comments(note_id, note_title: str):
    comments_data = get_comment(note_id)['data']
    note_comments = []
    note_comments.append(comments_data)

    # 获取ajax评论
    while comments_data.get('cursor'):
        # 暂停1~5秒
        time.sleep(random.randint(1, 5))
        log.info("获取ajax加载评论")
        cursor = comments_data['cursor']
        comments_data = get_ajax_comment(note_id, cursor)['data']
        note_comments.append(comments_data)

    # 追加保存
    df = pd.DataFrame(
        {"display_title": str(note_id) + "--" + str(note_title), "comment": json.dumps(note_comments)},
        index=[0])
    df.to_csv('./xiaohongshu3.csv', index=False, mode='a', header=False)
    time.sleep(random.randint(1, 8))


# 获取每个note
def get_note(response):
    """
    :param response: response
    :return:  none
    """
    if response.url == "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes":
        # 获取每个帖子的id
        data = response.json()['data']

        for note_info in data["items"]:
            note_id = note_info['id']
            if not note_info.get('note_card'):
                continue
            note_title = note_info['note_card'].get('display_title')
            log.info(f"获取{note_id}笔记")
            get_note_comments(note_id, note_title)


# playwright
def run():
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        default_context = browser.contexts[0]
        page = default_context.pages[0]
        # 监听响应
        page.on('response', get_note)
        # 小红书
        page.goto("https://www.xiaohongshu.com/explore")
        page.locator("#search-input").fill("厂推荐")
        page.locator("#search-input").press('Enter')
        # 等待搜索完成
        page.locator("div").filter(has_text=re.compile(r"^综合$")).nth(2).wait_for()
        for i in range(200):
            time.sleep(random.randint(1, 3))
            page.mouse.wheel(0, 200)


if __name__ == '__main__':
    with open('./log.json', 'r', encoding='utf-8') as f:
        log_config = json.load(f)
    logging.config.dictConfig(log_config)
    log = logging.getLogger('log')
    run()
