import json
import re
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

webdriver_options = Options()
webdriver_options.add_argument("window-size=1024,768")
webdriver_options.add_argument("--headless")

def func_delegate_try_except_driver(func, string:str):
    """
    一个委托函数来初始化 Selenium 的 WebDriver 给目标函数使用

    该委托函数主要把 driver 的 try except 进行集中处理以及异常的通用解决办法

    :Args:
     - func - 目标函数，接收的参数数量为 2 个
     - string - 传递给目标函数的第 2 个字符串参数

    :Returns:
     跟随目标函数进行返回

    """

    driver = webdriver.Chrome(options=webdriver_options)
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
    driver.get(url=href)
    name = driver.find_element_by_css_selector(css_selector="#content h1 span:nth-child(1)").text
    ranking = driver.find_element_by_css_selector(css_selector="#interest_sectl div.rating_wrap.clearbox div.rating_self.clearfix strong").text
    img = driver.find_element_by_css_selector(css_selector="#mainpic a img").get_attribute(name="src")
    info_text = driver.find_element_by_css_selector(css_selector=".subject #info").text

    fields_skips = ("^季数:$", "^集数: \\d+$", "^\\d+$")
    fields = ("导演:", "编剧:", "主演:", "类型:", "官方网站:", "制片国家/地区:", "语言:", "上映日期:", "片长:", "又名:", "IMDb链接:")
    fields_names = ("director", "writer", "actor", "genre", "site", "country", "language", "date", "duration", "subname", "imdb")
    lines = info_text.split("\n")
    lines = filter(lambda x: x and not any(re.search(word, x) for word in fields_skips), lines)
    lines = list(lines)

    if len(lines) > len(fields):
        raise Exception("Unexpected length: the number of built-in fields aren't greater than expected")

    result:Dict = {"name": name, "ranking": ranking, "img": img}

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


def func_keyword_search(driver:webdriver.Chrome, keyword:str) -> str:
    driver.get(url="https://www.douban.com")
    # WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "icp")))
    element_input:WebElement = driver.find_element_by_css_selector(css_selector=".inp input")
    element_input.send_keys(keyword)
    element_submit:WebElement = driver.find_element_by_css_selector(css_selector=".bn input")
    element_submit.submit()
    element_result_list:List = driver.find_elements_by_css_selector(css_selector="div.search-result div:nth-child(3) .result")
    result = filter(filter_func_movie_only, element_result_list)
    result = map(map_func_get_href, result)
    result = map(lambda x: func_delegate_try_except_driver(func_info_fetch, x), list(result)[:3])

    return json.dumps(list(result), ensure_ascii=False)

# if __name__ == "__main__":
    # result = func_delegate_try_except_driver(func_keyword_search, "aaaaaa")
    # print(result)

