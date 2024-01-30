import yaml

class config:
    config=yaml.safe_load(open("config.yml",'r',encoding="UTF-8").read())