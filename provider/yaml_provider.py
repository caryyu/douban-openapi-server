import yaml
import os


CONFIG_FILE = "./config.yml"


class YamlProvider(object):
    
    def create_file_when_not_exists(self, path:str):
        if os.path.exists(path) is not True:
            open(path, mode = "w",encoding = "utf-8")
            return True
        return False

    def get_config(self, keyword:str):
        self.create_file_when_not_exists(CONFIG_FILE)
        read_yml = yaml.load(open(CONFIG_FILE), Loader = yaml.FullLoader)
        if read_yml is not None and keyword in read_yml:
            return read_yml[keyword]
        else:
            return ''
            
    def set_config(self, keyword:str, value:str):
        self.create_file_when_not_exists(CONFIG_FILE)
        read_yml = yaml.load(open(CONFIG_FILE), Loader = yaml.FullLoader)
        if read_yml is not None and keyword in read_yml:
            read_yml[keyword] = value
        elif read_yml is None:
            read_yml = {keyword: value}
        else:
            read_yml[keyword] = value
        write_yml = open(CONFIG_FILE, 'w', encoding = "utf-8")
        yaml.dump(read_yml, write_yml)
        write_yml.close()

