import requests, json, time, calendar, re

def get_token():
    url = 'https://www.instagram.com/'
    
    headers = {}
    headers['X-Instagram-AJAX'] = '1'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    res = requests.get(url, headers=headers)
    pattern = r'"csrf_token":"(.*?)"'
    return re.findall(pattern, res.text)[0]

def login(Username, Password):

    TimeStamp = calendar.timegm(time.gmtime())
    url = 'https://www.instagram.com/accounts/login/ajax/'

    data = f'username={Username}&enc_password=#PWD_INSTAGRAM_BROWSER:0:{TimeStamp}:{Password}'

    headers = {}
    headers['Host'] = 'www.instagram.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:77.0) Gecko/20100101 Firefox/77.0'
    headers['Accept'] = '*/*'
    headers['X-CSRFToken'] = get_token()
    headers['X-Instagram-AJAX'] = '1'
    headers['Accept-Language'] = 'ar,en-US;q=0.7,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Connection'] = 'keep-alive'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    return requests.post(url, headers=headers, data=data)

def getMentions(ID):
    url = f'https://www.instagram.com/graphql/query/?query_hash=90709b530ea0969f002c86a89b4f2b8d&variables={{"reel_ids":["{ID}"],"tag_names":[],"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false,"show_story_viewer_list":true,"story_viewer_fetch_count":50,"story_viewer_cursor":"","stories_video_dash_manifest":false}}'

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Accept": "*/*",
        "Accept-Language": "ar,en-US;q=0.7,en;q=0.3",
        "X-CSRFToken": cookies['csrftoken'],
        "X-IG-App-ID": "936619743392459",
        "X-IG-WWW-Claim": "hmac.AR1gZPJR6yrLrd7_qHkmhWpCY4fD-i7_7r2GlNOS-szTgMfS",
        "X-Requested-With": "XMLHttpRequest"
    }

    res = requests.get(url, headers=headers, cookies=cookies)
    stories = res.json()['data']['reels_media'][0]['items']
    
    for story in stories:
        tappable_objects = story['tappable_objects']
        if tappable_objects:
            for item in tappable_objects:
                if item['__typename'] == 'GraphTappableMention':
                    print(item['username'])

def getID(us):
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:78.0) Gecko/20100101 Firefox/78.0"
    headers["Host"] = "www.instagram.com"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "ar,en-US;q=0.7,en;q=0.3"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"

    res = requests.get(f'https://www.instagram.com/{us}/?__a=1', headers=headers, cookies=cookies)
    return res.json()['graphql']['user']['id']

us = input('username: ')
ps = input('password: ')
cookies = login(us, ps).cookies.get_dict()

username = input('target username: ')
ID = getID(username)
getMentions(ID)
