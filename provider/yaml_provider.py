import yaml


class YamlProvider(object):
    def get_config(keyword:str):
        read = yaml.load(open('./config.yml'), Loader=yaml.FullLoader)
        return read[keyword]
