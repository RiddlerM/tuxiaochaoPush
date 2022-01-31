# -*- coding: utf-8 -*-
import json, requests

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=XXXXXXXX'
product_id = '123456'


def push(title, content, url):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": content
        }
    }
    r = requests.post(url, headers=headers, json=data)
    print(r.content)
    return r.content


def main_handler(event, context):
    request_body = event['body']
    print(request_body)
    param = json.loads(request_body)
    print(param)
    action = param['type']
    content = param['payload']
    categories = param['payload']['post']['categories']
    cate = ''
    if len(categories) > 0:
        cate = '-'.join([k['value'] for k in categories])
        cate = f'\n  \n  **类别：** {cate}'

    if action == 'post.created':
        title = '有新反馈提交'
    elif action == 'post.updated':
        title = '有反馈被修改'
    elif action == 'reply.created':
        title = '有反馈被回复'
    elif action == 'reply.updated':
        title = '有回复被修改'

    if action.find('post') != -1:
        extra_content = ''
        post_extra = content['post']['extra']
        if len(post_extra) > 0:
            for k, v in post_extra.items():
                extra_content += ">" + str(k) + ":" + str(v) + "  \n  "
        post_url = content['post']['post_url']
        nick_name = content['post']['nick_name']
        post_content = content['post']['content']
    elif action.find('reply') != -1:
        post_url = "https://support.qq.com/products/" + str(product_id) + "/post/" + str(content['reply']['f_title_id'])
        nick_name = content['reply']['nick_name']
        post_content = content['reply']['content']
    text = f'[**{nick_name}：** {post_content}]({post_url}){extra_content}{cate}'
    push(title, text, webhook)