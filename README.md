![](https://travis-ci.org/caryyu/douban-openapi-server.svg?branch=main) ![](https://img.shields.io/docker/pulls/caryyu/douban-openapi-server.svg) 

# douban-openapi-server

A Douban API server that provides an unofficial method for information gathering, currently, supporting several providers below:

- SeleniumProvider - which will open a headless Chrome to simulate the user interaction (Optional)
- HttpRequestProvider - which has leveraged `Requests & BeautifulSoup` for information gathering with no any browser interaction (By default)
- P2PCacheProvider - `ToDo` (Scrapy/SQLite/IPFS/BitTorrent/etc) - ?

> Note: Any comments and issues are welcomed!!!

## Docker 

```shell
docker run --rm -d -p 5000:5000 caryyu/douban-openapi-server:latest
docker run --rm -d -p 5000:5000 caryyu/douban-openapi-server:<commit>
```

> Note: the `commit` can be found from git history of main branch

## Install

 - Make sure you have `python3` and `pipenv` installed in advance,

  ```shell
  pipenv install
  pipenv shell

  export FLASK_APP=app.py
  export FLASK_ENV=development
  export FLASK_DEBUG=0
  flask run
  ```

  > Note: There are two providers for you to choose, by default, `HttpRequestProvider` will take place, which will be faster for information fetching, for `Selenium`, You have to follow their official instruction in advance

## API Usage

- A deep search that costs much more time to response due to the detailed information

  ```shell
  ➜ curl -s http://localhost:5000/movies\?q\=Harry%20Potter\&type\=full | jq
  [
    {
      "name": "哈利·波特与魔法石 Harry Potter and the Sorcerer's Stone",
      "rating": "9.1",
      "img": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2614949805.webp",
      "sid": "1295038",
      "year": "2001",
      "intro": "xxxx",
      "director": "克里斯·哥伦布",
      "writer": "史蒂夫·克洛夫斯 / J·K·罗琳",
      "actor": "丹尼尔·雷德克里夫 / 艾玛·沃森 / 鲁伯特·格林特 / 艾伦·瑞克曼 / 玛吉·史密斯 / 更多...",
      "genre": "奇幻 / 冒险",
      "site": "www.harrypotter.co.uk",
      "country": "美国 / 英国",
      "language": "英语",
      "screen": "2002-01-26(中国大陆) / 2020-08-14(中国大陆重映) / 2001-11-04(英国首映) / 2001-11-16(美国)",
      "duration": "152分钟 / 159分钟(加长版)",
      "subname": "哈利波特1：神秘的魔法石(港/台) / 哈1 / Harry Potter and the Philosopher's Stone",
      "imdb": "tt0241527",
      "celebrities": [
        {
          "id": "1018208",
          "img": "https://img2.doubanio.com/view/celebrity/s_ratio_celebrity/public/p57793.jpg",
          "name": "蒂莫西·范·帕腾",
          "role": "导演"
        }
      ]
    },
    {
      "name": "哈利·波特与死亡圣器(下) Harry Potter and the Deathly Hallows: Part 2",
      "rating": "8.9",
      "img": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p917846733.webp",
      "sid": "3011235",
      "year": "2011",
      "intro": "xxxx",
      "director": "大卫·叶茨",
      "writer": "史蒂夫·克洛夫斯 / J·K·罗琳",
      "actor": "丹尼尔·雷德克里夫 / 艾玛·沃森 / 鲁伯特·格林特 / 海伦娜·伯翰·卡特 / 拉尔夫·费因斯 / 更多...",
      "genre": "奇幻 / 冒险",
      "site": "",
      "country": "美国 / 英国",
      "language": "英语",
      "screen": "2011-08-04(中国大陆) / 2011-07-15(美国)",
      "duration": "130分钟",
      "subname": "哈利波特7：死神的圣物2(港/台) / 哈利·波特与死圣(下) / 哈7(下) / 哈利·波特大结局",
      "imdb": "tt1201607",
      "celebrities": [
        {
          "id": "1018208",
          "img": "https://img2.doubanio.com/view/celebrity/s_ratio_celebrity/public/p57793.jpg",
          "name": "蒂莫西·范·帕腾",
          "role": "导演"
        }
      ]
    },
    {
      "name": "哈利·波特与密室 Harry Potter and the Chamber of Secrets",
      "rating": "8.7",
      "img": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1082651990.webp",
      "sid": "1296996",
      "year": "2002",
      "intro": "xxxx",
      "director": "克里斯·哥伦布",
      "writer": "史蒂夫·克洛夫斯 / J·K·罗琳",
      "actor": "丹尼尔·雷德克里夫 / 艾玛·沃森 / 鲁伯特·格林特 / 汤姆·费尔顿 / 理查德·格雷弗斯 / 更多...",
      "genre": "奇幻 / 冒险",
      "site": "www.harrypotter.co.uk",
      "country": "美国 / 英国 / 德国",
      "language": "英语",
      "screen": "2003-01-24(中国大陆) / 2002-11-15(英国/美国)",
      "duration": "161分钟 / 174分钟(加长版)",
      "subname": "哈利波特2：消失的密室(港/台) / 哈2",
      "imdb": "tt0295297",
      "celebrities": [
        {
          "id": "1018208",
          "img": "https://img2.doubanio.com/view/celebrity/s_ratio_celebrity/public/p57793.jpg",
          "name": "蒂莫西·范·帕腾",
          "role": "导演"
        }
      ]
    }
  ]
  ```

- A shallow search without the detailed information

  ```shell
  ➜ curl -s http://localhost:5000/movies\?q\=Harry%20Potter\&type\=partial | jq
  [
    {
      "sid": "1295038",
      "name": "哈利·波特与魔法石",
      "rating": "9.1",
      "img": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2614949805.webp",
      "year": "2001"
    },
    {
      "sid": "3011235",
      "name": "哈利·波特与死亡圣器(下)",
      "rating": "8.9",
      "img": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p917846733.webp",
      "year": "2011"
    },
    {
      "sid": "1296996",
      "name": "哈利·波特与密室",
      "rating": "8.7",
      "img": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1082651990.webp",
      "year": "2002"
    }
  ]
  ```

- Retrieve a single object and response within a very less time

  ```shell
  ➜ curl -s http://localhost:5000/movies/1295038 | jq
  {
    "name": "哈利·波特与魔法石 Harry Potter and the Sorcerer's Stone",
    "rating": "9.1",
    "img": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2614949805.webp",
    "sid": "1295038",
    "year": "2001",
    "intro": "xxxx",
    "director": "克里斯·哥伦布",
    "writer": "史蒂夫·克洛夫斯 / J·K·罗琳",
    "actor": "丹尼尔·雷德克里夫 / 艾玛·沃森 / 鲁伯特·格林特 / 艾伦·瑞克曼 / 玛吉·史密斯 / 更多...",
    "genre": "奇幻 / 冒险",
    "site": "www.harrypotter.co.uk",
    "country": "美国 / 英国",
    "language": "英语",
    "screen": "2002-01-26(中国大陆) / 2020-08-14(中国大陆重映) / 2001-11-04(英国首映) / 2001-11-16(美国)",
    "duration": "152分钟 / 159分钟(加长版)",
    "subname": "哈利波特1：神秘的魔法石(港/台) / 哈1 / Harry Potter and the Philosopher's Stone",
    "imdb": "tt0241527",
    "celebrities": [
      {
        "id": "1018208",
        "img": "https://img2.doubanio.com/view/celebrity/s_ratio_celebrity/public/p57793.jpg",
        "name": "蒂莫西·范·帕腾",
        "role": "导演"
      }
    ]
  }
  ```

- Given a movie id to fetch the celebrity list

  ```
  ➜ curl -s http://localhost:5000/movies/1295038/celebrities | jq
  [
    {
      "id": "1027347",
      "img": "https://img9.doubanio.com/view/celebrity/s_ratio_celebrity/public/p1477093490.04.jpg",
      "name": "伊恩·哈特",
      "role": "演员",
      "intro": "伊恩·哈特（Ian Hart），1964年10月8日出生于英国利物浦。英国男演员。曾在哈利·波特的第一部《哈利·波特与魔法石》中扮演了奇洛教授，被中国观众所熟知。作为英国戏剧界一位知名的演员，他还曾经成功地扮演过约翰·列侬。",
      "gender": "男",
      "constellation": "天秤座",
      "birthdate": "1964-10-08",
      "birthplace": "英国,英格兰,默西塞德郡,利物浦",
      "nickname": "Ian Davies",
      "imdb": "nm0001324"
    }
  ]
  ```

# Disclaimer

This is only for research and study, Any copyright violation should count on your own, thanks.

