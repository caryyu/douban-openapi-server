import json
import re
from typing import Dict, List
from bs4 import BeautifulSoup
import requests

class HttpRequestProvider(object):
    headers = {
        'User-Agent': 'curl/7.64.1',
    }

    def search_partial_list(self, keyword:str) -> List:
        r = requests.get(f"https://www.douban.com/search?q={keyword}", headers=self.headers)
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
            try:
                element.select_one("div.content div div span.rating_nums").string
            except:
                pass

            return {
                "sid": sid,
                "name": name.strip(),
                "rating": rating.strip(),
                "img": img.strip(),
                "year": year
            }

        limits = 3
        result = map(func_item_wrap, list(elements)[:limits])
        return list(result)

    def search_full_list(self, keyword:str) -> List:
        r = requests.get(f"https://www.douban.com/search?q={keyword}", headers=self.headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        elements = soup.select("div.search-result div:nth-child(3) .result")
        elements = filter(lambda x: self._filter_func_movie_only(x), elements)

        def func_item_wrap(element) -> Dict:
            a = element.select_one("div.content div h3 a")
            sid = re.search(".*sid: (\\d+),.*", a["onclick"]).group(1)
            return self.fetch_detail_info(sid)

        limits = 3
        result = map(func_item_wrap, list(elements)[:limits])
        return list(result)

    def fetch_detail_info(self, sid:str) -> Dict:
        r = requests.get(f"https://movie.douban.com/subject/{sid}/", headers=self.headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.select_one("#content h1 span:nth-child(1)").string
        rating = soup.select_one("#interest_sectl div.rating_wrap.clearbox div.rating_self.clearfix strong").string
        img = soup.select_one("#mainpic a img")["src"]
        info_text = soup.select_one(".subject #info").get_text()
        year = re.search("\\((\\d+)\\)", soup.select_one("#content h1 span.year").string).group(1)
        sid = re.search(".*/(\\d+)/.*", soup.select_one("#mainpic a")["href"]).group(1)
        intro = "".join(soup.select_one("#link-report span:nth-child(1)").stripped_strings)

        fields_skips = ("^季数:$", "^集数: \\d+$", "^\\d+$", "^官方小站:$")
        fields = ("导演:", "编剧:", "主演:", "类型:", "官方网站:", "制片国家/地区:", "语言:", "上映日期:", "片长:", "又名:", "IMDb链接:")
        fields_names = ("director", "writer", "actor", "genre", "site", "country", "language", "screen", "duration", "subname", "imdb")
        lines = info_text.split("\n")
        lines = filter(lambda x: x and not any(re.search(word, x) for word in fields_skips), lines)
        lines = list(lines)

        if len(lines) > len(fields):
            raise Exception("Unexpected length: the number of built-in fields aren't greater than expected")

        result:Dict = {"name": name, "rating": rating, "img": img, "sid": sid, "year": year, "intro": intro}

        i = 0
        j = 0
        while i < len(fields):
            if fields[i] in lines[j]:
                value = lines[j].replace(fields[i], "")
                result[fields_names[i]] = value.strip()
                j = j + 1
            else:
                result[fields_names[i]] = ""
            i = i + 1

        return result

    def fetch_celebrities(self, sid:str) -> List:
        r = requests.get(f"https://movie.douban.com/subject/{sid}/celebrities", headers=self.headers)
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

        result = map(func_element_wrap, elements)
        result = filter(lambda x: x["role"] in ["导演","配音","演员"], list(result))
        return list(result)

    def _filter_func_movie_only(self, element) -> bool:
        category = element.select_one("div.content div h3 span")
        return "[电影]" == category.string.strip()

# if __name__ == "__main__":
    # p = HttpRequestProvider()
    # # result = p.search_full_list("Harry Potter")
    # # result = trans.search_partial_list("Harry Potter")
    # # result = p.fetch_detail_info("1295038")
    # result = p.fetch_celebrities("1295038")
    # result = json.dumps(result, ensure_ascii=False)
    # print(result)
