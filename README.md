![](https://travis-ci.org/caryyu/douban-openapi-server.svg?branch=main) ![](https://img.shields.io/docker/pulls/caryyu/douban-openapi-server.svg) 

# douban-openapi-server

A selenium-based Douban API server that provides an unofficial method for information querying

> Note: Any comments and issues are welcomed!!!

## Docker 

```shell
docker run --rm -d -p 5000:5000 caryyu/douban-openapi-server:latest
```

## Installation

 - Follow `selenium` document to install Chrome Driver in the runtime environment

 - Make sure you have `python3` and `pipenv` installed in advance,

  ```shell
  pipenv install
  pipenv shell

  export FLASK_APP=app.py
  export FLASK_ENV=development
  export FLASK_DEBUG=0
  flask run
  ```

## Usage

```shell
➜ curl -s http://localhost:5000/search\?q\=Harry%20Potter | jq
[
  {
    "name": "哈利·波特与魔法石 Harry Potter and the Sorcerer's Stone",
    "ranking": "9.1",
    "img": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2614949805.webp",
    "director": "克里斯·哥伦布",
    "writer": "史蒂夫·克洛夫斯 / J·K·罗琳",
    "actor": "丹尼尔·雷德克里夫 / 艾玛·沃森 / 鲁伯特·格林特 / 艾伦·瑞克曼 / 玛吉·史密斯 / 更多...",
    "genre": "奇幻 / 冒险",
    "site": "www.harrypotter.co.uk",
    "country": "美国 / 英国",
    "language": "英语",
    "date": "2002-01-26(中国大陆) / 2020-08-14(中国大陆重映) / 2001-11-04(英国首映) / 2001-11-16(美国)",
    "duration": "152分钟 / 159分钟(加长版)",
    "subname": "哈利波特1：神秘的魔法石(港/台) / 哈1 / Harry Potter and the Philosopher's Stone",
    "imdb": "tt0241527"
  },
  {
    "name": "哈利·波特与死亡圣器(下) Harry Potter and the Deathly Hallows: Part 2",
    "ranking": "8.9",
    "img": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p917846733.webp",
    "director": "大卫·叶茨",
    "writer": "史蒂夫·克洛夫斯 / J·K·罗琳",
    "actor": "丹尼尔·雷德克里夫 / 艾玛·沃森 / 鲁伯特·格林特 / 海伦娜·伯翰·卡特 / 拉尔夫·费因斯 / 更多...",
    "genre": "奇幻 / 冒险",
    "site": "",
    "country": "美国 / 英国",
    "language": "英语",
    "date": "2011-08-04(中国大陆) / 2011-07-15(美国)",
    "duration": "130分钟",
    "subname": "哈利波特7：死神的圣物2(港/台) / 哈利·波特与死圣(下) / 哈7(下) / 哈利·波特大结局",
    "imdb": "tt1201607"
  },
  {
    "name": "哈利·波特与密室 Harry Potter and the Chamber of Secrets",
    "ranking": "8.7",
    "img": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1082651990.webp",
    "director": "克里斯·哥伦布",
    "writer": "史蒂夫·克洛夫斯 / J·K·罗琳",
    "actor": "丹尼尔·雷德克里夫 / 艾玛·沃森 / 鲁伯特·格林特 / 汤姆·费尔顿 / 理查德·格雷弗斯 / 更多...",
    "genre": "奇幻 / 冒险",
    "site": "www.harrypotter.co.uk",
    "country": "美国 / 英国 / 德国",
    "language": "英语",
    "date": "2003-01-24(中国大陆) / 2002-11-15(英国/美国)",
    "duration": "161分钟 / 174分钟(加长版)",
    "subname": "哈利波特2：消失的密室(港/台) / 哈2",
    "imdb": "tt0295297"
  }
]
```

# Disclaimer

This is only for research and study, Any copyright violation should count on your own, thanks.

