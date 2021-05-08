import json
import logging
import re
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException

webdriver_options = Options()
webdriver_options.add_argument("window-size=1024,768")
webdriver_options.add_argument("--headless")
webdriver_options.add_argument("--disable-dev-shm-usage")
webdriver_options.add_argument("--disable-gpu")
webdriver_options.add_argument("--no-sandbox")

def delegator_try_except_driver(func, string:str):
    """
    一个委托函数来初始化 Selenium 的 WebDriver 给目标函数使用

    该委托函数主要把 driver 的 try except 进行集中处理以及异常的通用解决办法

    注意：页面超时打开时间为 10 秒，确保网页过慢影响响应效率

    :Args:
     - func - 目标函数，接收的参数数量为 2 个
     - string - 传递给目标函数的第 2 个字符串参数

    :Returns:
     跟随目标函数进行返回

    """

    driver = webdriver.Chrome(options=webdriver_options)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)
    try:
        return func(driver, string)
    except Exception as ex:
        raise ex
    finally:
        driver.close()

def filter_func_movie_only(element:WebElement) -> bool:
    category:str = element.find_element_by_css_selector(css_selector="div.content div h3 span").text
    return "[电影]" == category.strip()

def map_func_get_href(element:WebElement) -> str:
    result:WebElement = element.find_element_by_css_selector(css_selector="div.content div h3 a")
    return result.get_attribute(name="href")

def map_func_get_img(element:WebElement) -> str:
    result:WebElement = element.find_element_by_tag_name(name="img")
    return result.get_attribute(name="src")

def func_info_fetch(driver:webdriver.Chrome, href:str) -> Dict:
    try:
        driver.get(url=href)
    except TimeoutException:
        print(f"the page opening is timeout: {href}")
        pass
    name = driver.find_element_by_css_selector(css_selector="#content h1 span:nth-child(1)").text
    rating = driver.find_element_by_css_selector(css_selector="#interest_sectl div.rating_wrap.clearbox div.rating_self.clearfix strong").text
    img = driver.find_element_by_css_selector(css_selector="#mainpic a img").get_attribute(name="src")
    info_text = driver.find_element_by_css_selector(css_selector=".subject #info").text
    year = re.search("\\((\\d+)\\)", driver.find_element_by_css_selector(css_selector="#content h1 span.year").text).group(1)
    sid = re.search(".*/(\\d+)/.*", driver.find_element_by_css_selector(css_selector="#mainpic a").get_attribute(name="href")).group(1)
    intro = driver.find_element_by_css_selector(css_selector="#link-report span:nth-child(1)").text

    fields_skips = ("^季数:$", "^集数: \\d+$", "^\\d+$")
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


def service_keyword_full_search(driver:webdriver.Chrome, keyword:str) -> str:
    """
    根据 keyword 来查询全部信息 - 该操作为深度检索, 会增加检索的时间
    注意: 限制的数据条数永远为前 3 条 (减少非相关性数据)

    :Args:
     - driver - 委托代理往下传递的对象，拥有自动管理关闭的功能
     - keyword - 给定的关键字字符串

    :Returns:
     返回 List[Dict] 类型的 JSON 字符串
    """

    # How many rows should be handled
    limits:int = 3
    try:
        driver.get(url="https://www.douban.com")
    except TimeoutException:
        print(f"the page opening is timeout: https://www.douban.com")
        pass
    # WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "icp")))
    element_input:WebElement = driver.find_element_by_css_selector(css_selector=".inp input")
    element_input.send_keys(keyword)
    element_submit:WebElement = driver.find_element_by_css_selector(css_selector=".bn input")
    element_submit.submit()
    element_result_list:List = driver.find_elements_by_css_selector(css_selector="div.search-result div:nth-child(3) .result")
    result = filter(filter_func_movie_only, element_result_list)
    result = map(map_func_get_href, result)
    result = map(lambda x: delegator_try_except_driver(func_info_fetch, x), list(result)[:limits])

    return json.dumps(list(result), ensure_ascii=False)

def service_keyword_partial_search(driver:webdriver.Chrome, keyword:str) -> str:
    """
    根据 keyword 来查询列表的部分信息 - 不会进入详情页从而减少响应时间
    注意: 限制的数据条数永远为前 3 条 (减少非相关性数据)

    :Args:
     - driver - 委托代理往下传递的对象，拥有自动管理关闭的功能
     - keyword - 给定的关键字字符串

    :Returns:
     返回 List[Dict] 类型的 JSON 字符串
    """
    # How many rows should be handled
    limits:int = 3
    try:
        driver.get(url=f"https://www.douban.com/search?q={keyword}")
    except TimeoutException:
        print(f"the page opening is timeout: https://www.douban.com/search?q={keyword}")
        pass
    element_result_list:List = driver.find_elements_by_css_selector(css_selector="div.search-result div:nth-child(3) .result")
    result = filter(filter_func_movie_only, element_result_list)

    def func_item_wrap(element: WebElement) -> Dict:
        a:WebElement = element.find_element_by_css_selector(css_selector="div.content div h3 a")
        img = element.find_element_by_css_selector(css_selector="div.pic a img").get_attribute("src")
        name = a.text
        sid = re.search(".*sid: (\\d+),.*", a.get_attribute("onclick")).group(1)
        year = re.search(".*/ (\\d+)$", element.find_element_by_css_selector(css_selector="div.content div div span.subject-cast").text).group(1)
        rating = "0"
        try:
            element.find_element_by_css_selector(css_selector="div.content div div span.rating_nums").text
        except:
            pass

        return {
            "sid": sid,
            "name": name.strip(),
            "rating": rating.strip(),
            "img": img.strip(),
            "year": year
        }

    result = map(func_item_wrap, list(result)[:limits])
    return json.dumps(list(result), ensure_ascii=False)

def service_info_fetch_by_sid(driver:webdriver.Chrome, sid:str) -> str:
    """
    根据 sid 来查获取电影详情

    :Args:
     - driver - 委托代理往下传递的对象，拥有自动管理关闭的功能
     - sid - 电影的 sid(subject id) 编号，根据此编号查询信息

    :Returns:
     返回 Dict 类型的 JSON 字符串
    """
    result = func_info_fetch(driver=driver, href=f"https://movie.douban.com/subject/{sid}/")
    return json.dumps(result, ensure_ascii=False)

def service_info_fetch_celebrities_by_sid(driver:webdriver.Chrome, sid:str) -> str:
    url = f"https://movie.douban.com/subject/{sid}/celebrities"
    try:
        driver.get(url=url)
    except TimeoutException:
        print(f"the page opening is timeout: {url}")
        pass
    elements = driver.find_elements_by_css_selector(css_selector="li.celebrity")

    def func_element_wrap(element) -> dict:
        cid = re.search(".*/(\\d+)/$", element.find_element_by_css_selector("a").get_attribute("href")).group(1)
        img = re.search(".*url\\(\"(.*)\"\\).*", element.find_element_by_css_selector("div.avatar").get_attribute("style")).group(1)
        name = element.find_element_by_css_selector("span.name").text.split(" ")[0]
        role = ""
        try:
            role = element.find_element_by_css_selector("span.role").text.split(" ")[0]
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
    return json.dumps(list(result), ensure_ascii=False)

# if __name__ == "__main__":
    # # result = delegator_try_except_driver(service_keyword_full_search, "Source Code")
    # # result = delegator_try_except_driver(service_keyword_partial_search, "Source Code")
    # result = delegator_try_except_driver(service_info_fetch_by_sid, "26275567")
    # result = delegator_try_except_driver(service_info_fetch_celebrities_by_sid, "4202982")
    # print(result)

