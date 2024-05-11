import redis
import requests
import time
key = 'note_error'
# redis init
log = redis.Redis(host="localhost", port=6379, db='2')

cookies = ''

headers = ''


def error_handle(func):
    def wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result['code'] == -100:
                raise Exception(result)
            return result
        except Exception as e:
            print(e)
            log.lpush(str(*args))

    return wrap


@error_handle
# 获取追评(未实现)
def get_append_comment(note_id: str, ajax_comment: str, sub_cursor: str) -> dict:
    # url = f'https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page?note_id={note_id}&root_comment_id={ajax_comment}&num=10&cursor={sub_cursor}&image_formats=jpg,webp,avif'
    url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page?note_id=6624f6ee000000000103237a&root_comment_id=662e4d9e00000000130241c8&num=10&cursor=662e534500000000130268f2&image_formats=jpg,webp,avif&top_comment_id='
    response = requests.get(url, headers=headers, cookies=cookies)
    print(response.text)
    return response.json()


@error_handle
# 获取ajax加载评论
def get_ajax_comment(node_id: str, ajax_comment: str) -> dict:
    url = f'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={node_id}&cursor={ajax_comment}&top_comment_id=&image_formats=jpg,webp,avif'
    response = requests.get(url=url, headers=headers, cookies=cookies)
    return response.json()


@error_handle
# 获取评论
def get_comment(node_info: str) -> dict:
    import requests

    response = requests.get(
        f'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={node_info}&cursor=&top_comment_id=&image_formats=jpg,webp,avif',
        cookies=cookies,
        headers=headers,
    )
    return response.json()


if __name__ == '__main__':
    get_append_comment('1','2','3')
