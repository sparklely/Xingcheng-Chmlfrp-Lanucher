import yaml

class Config:
    config=yaml.safe_load(open("config.yml",'r',encoding="UTF-8").read())