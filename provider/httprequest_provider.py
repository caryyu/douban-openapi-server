import json
import random
import re
import time
from typing import Dict, List
from bs4 import BeautifulSoup
import requests

class HttpRequestProvider(object):

    # 添加UA列表
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
        "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
        "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/97.0.4692.84 Mobile/15E148 Safari/604.1',
        'Frodo/07220003 CFNetwork/1240.0.4 Darwin/20.6.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14"
    ]

    """
    随机UA
    """
    def get_random_useragent(self):
        """生成随机的UserAgent
        :return: UserAgent字符串
        """
        return random.choice(self.USER_AGENTS)

    def get_headers(self):
        useragent = self.get_random_useragent()
        headers = {
            'User-Agent': useragent
        }
        return headers

    """
    生成随机间隔延时
    """
    def wait_some_time(self):
        time.sleep(random.randint(500, 3000) / 3000)

    def __init__(self, headers) -> None:
        self.headers = headers

    def search_partial_list(self, keyword:str, options: dict) -> List:
        self.wait_some_time()
        r = requests.get(f"https://www.douban.com/search?cat=1002&q={keyword}", headersheaders=self.get_headers())
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        elements = soup.select("div.search-result div:nth-child(3) .result")
        elements = filter(lambda x: self._filter_func_movie_only(x), elements)

        def func_item_wrap(element) -> Dict:
            a = element.select_one("div.content div h3 a")
            img = element.select_one("div.pic a img")["src"]
            name = a.string
            sid = re.search(".*sid: (\\d+),.*", a["onclick"]).group(1)
            year = re.search(".*/ (\\d+)$", element.select_one("div.content div div span.subject-cast").string).group(1)
            rating = "0"
            img = self._get_img_by_size(img.strip(), options['image_size'])
            try:
                element.select_one("div.content div div span.rating_nums").string
            except:
                pass

            return {
                "sid": sid,
                "name": name.strip(),
                "rating": rating.strip(),
                "img": img,
                "year": year
            }

        limits = 3
        result = map(func_item_wrap, list(elements)[:limits])
        return list(result)

    def search_full_list(self, keyword:str, options: dict) -> List:
        self.wait_some_time()
        r = requests.get(f"https://www.douban.com/search?cat=1002&q={keyword}", headers=self.get_headers())
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        elements = soup.select("div.search-result div:nth-child(3) .result")
        elements = filter(lambda x: self._filter_func_movie_only(x), elements)

        def func_item_wrap(element) -> Dict:
            a = element.select_one("div.content div h3 a")
            sid = re.search(".*sid: (\\d+),.*", a["onclick"]).group(1)
            return self.fetch_detail_info(sid, options)

        limits = 3
        result = map(func_item_wrap, list(elements)[:limits])
        return list(result)

    def fetch_detail_info(self, sid:str, options: dict) -> Dict:
        r = requests.get(f"https://movie.douban.com/subject/{sid}/", headers=self.headers)
        self.wait_some_time()
        r = requests.get(f"https://movie.douban.com/subject/{sid}/", headers=self.get_headers())
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.select_one("#content h1 span:nth-child(1)").string
        rating = soup.select_one("#interest_sectl div.rating_wrap.clearbox div.rating_self.clearfix strong").string or '0'
        img = soup.select_one("#mainpic a img")["src"]
        info_text = soup.select_one(".subject #info").get_text()
        year = re.search("\\((\\d+)\\)", soup.select_one("#content h1 span.year").string).group(1)
        sid = re.search(".*/(\\d+)/.*", soup.select_one("#mainpic a")["href"]).group(1)
        titles = re.search("(.+第\w季|[\w\uff1a\uff01\uff0c\u00b7]+)\s*(.*)", title)
        name = titles.group(1)
        originalName = titles.group(2)
        img = self._get_img_by_size(img, options['image_size'])

        intro = soup.select_one("#link-report span:nth-child(1)")
        intro = "".join(intro.stripped_strings) if intro else ""

        lines = info_text.split("\n")
        lines = map(lambda x: x.split(":", 1), lines)
        lines = filter(lambda x: len(x) > 1, lines)

        fields = ("导演", "编剧", "主演", "类型", "官方网站", "制片国家/地区", "语言", "上映日期", "片长", "又名", "IMDb链接", "IMDb", "单集片长", "首播")
        fields_names = ("director", "writer", "actor", "genre", "site", "country", "language", "screen", "duration", "subname", "imdb", "imdb", "duration", "screen")
        result:Dict[str, object] = {"name": name, "originalName": originalName, "rating": rating, "img": img, "sid": sid, "year": year, "intro": intro}

        for item in iter(lines):
            field = item[0]
            i = 0
            has = False

            while i < len(fields):
                if fields[i] == field:
                    has = True
                    break
                i+=1

            if has:
               result[fields_names[i]] = item[1].strip()

        celebrities = soup.select("ul.celebrities-list li.celebrity")

        def func_element_wrap(element):
            cid = re.search(".*/(\\d+)/$", element.select_one("a")["href"]).group(1)
            img = re.search(".*url\\((.*)\\).*", element.select_one("div.avatar")["style"]).group(1)
            name = element.select_one("span.name").string.split(" ")[0]
            role = ""
            try:
                role = element.select_one("span.role").string.split(" ")[0]
            except:
                pass

            return {
                "id": cid,
                "img": img,
                "name": name,
                "role": role
            }

        celebrities = filter(lambda x: 'fake' not in x['class'], celebrities)
        celebrities = map(func_element_wrap, celebrities)
        celebrities = filter(lambda x: x["role"] in ["导演","配音","演员"], list(celebrities))
        result["celebrities"] = list(celebrities)

        return result

    def fetch_celebrities(self, sid:str) -> List:
        limits=15
        self.wait_some_time()
        r = requests.get(f"https://movie.douban.com/subject/{sid}/celebrities", headers=self.get_headers())
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        elements = soup.select("li.celebrity")

        def func_element_wrap(element) -> dict:
            cid = re.search(".*/(\\d+)/$", element.select_one("a")["href"]).group(1)
            img = re.search(".*url\\((.*)\\).*", element.select_one("div.avatar")["style"]).group(1)
            name = element.select_one("span.name").string.split(" ")[0]
            role = ""
            try:
                role = element.select_one("span.role").string.split(" ")[0]
            except:
                pass

            return {
                "id": cid,
                "img": img,
                "name": name,
                "role": role
            }

        # def load_detail(x) -> dict:
            # detail = self.fetch_celebrity_detail(x["id"])
            # return {**x, **detail}

        result = map(func_element_wrap, elements)
        result = filter(lambda x: x["role"] in ["导演","配音","演员"], list(result))
        # result = map(load_detail, list(result)[:limits])
        return list(result)[:limits]

    def fetch_celebrity_detail(self, cid) -> dict:
        self.wait_some_time()
        r = requests.get(f"https://movie.douban.com/celebrity/{cid}/", headers=self.get_headers())
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        info_text = soup.select_one("#headline div.info ul").get_text()
        name = soup.select_one("#content > h1").string
        img = soup.select_one("#headline > div.pic img")["src"]
        intro = "".join(soup.select_one("#intro div.bd").stripped_strings)

        lines = info_text.split("\n\n")
        lines = map(lambda x: "".join(x.split("\n")), lines)
        lines = map(lambda x: x.split(":", 1), lines)
        lines = filter(lambda x: len(x) > 1, lines)

        name = name.split(" ", 1)[0]

        fields = ("性别", "星座", "出生日期", "出生地", "职业", "更多外文名", "家庭成员", "imdb编号", "官方网站")
        fields_names = ("gender", "constellation", "birthdate", "birthplace", "role", "nickname", "friends", "imdb", "site")
        result:Dict[str, object] = {"intro": intro, "name": name, "id": cid, "img": img}

        for item in iter(lines):
            field = item[0]
            i = 0
            has = False

            while i < len(fields):
                if fields[i] == field:
                    has = True
                    break
                i+=1

            if has:
               result[fields_names[i]] = item[1].strip()

        return result

    def _filter_func_movie_only(self, element) -> bool:
        category = element.select_one("div.content div h3 span")
        if category is None:
            return False
        text = category.string.strip()
        return "[电影]" == text or "[电视剧]" == text

    def fetch_wallpaper(self, sid) -> list[dict]:
        self.wait_some_time()
        r = requests.get(f"https://movie.douban.com/subject/{sid}/photos?type=W&start=0&sortby=size&size=a&subtype=a", headers=self.get_headers())
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select(".poster-col3 li")

        result = []
        for item in items:
            data_id = item["data-id"]
            small = f"https://img1.doubanio.com/view/photo/s/public/p{data_id}.jpg"
            medium = f"https://img1.doubanio.com/view/photo/m/public/p{data_id}.jpg"
            large = f"https://img1.doubanio.com/view/photo/l/public/p{data_id}.jpg"
            size = item.select_one(".prop").string.strip()
            width = size[0:size.index("x")]
            height = size[size.index("x") + 1:len(size)]
            result.append({"id": data_id, "small": small, "medium": medium, "large": large, "size": size, "width": int(width), "height": int(height)})

        return result

    def _get_img_by_size(self, img, image_size: str = '') -> str:
        if image_size != 'm' and image_size != 'l':
            image_size = 's'

        # 解析 URL 获取图片 ID (无 ID 直接返回默认图片)
        match = re.search(r"/p(\d+?)\.", img)
        if not match:
            return img
        data_id = match.group(1)

        image_dict = {
            's': f"https://img2.doubanio.com/view/photo/s/public/p{data_id}.jpg",
            'm': f"https://img2.doubanio.com/view/photo/m/public/p{data_id}.jpg",
            'l': f"https://img2.doubanio.com/view/photo/l/public/p{data_id}.jpg"
        }

        return image_dict[image_size]

# if __name__ == "__main__":
#     p = HttpRequestProvider()
#     r = p.fetch_wallpaper("1295038")
#     print(r)
#     r = p.fetch_celebrity_detail("1032915")
#     print(r)
#     # # result = p.search_full_list("Harry Potter")
#     # # result = trans.search_partial_list("Harry Potter")
#     result = p.fetch_detail_info("3016187")
#     # result = p.fetch_celebrities("1295038")
#     result = json.dumps(result, ensure_ascii=False)
#     print(result)
