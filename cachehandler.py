import json
import os

class CacheHandler(object):
    @staticmethod
    def ensure_dir(path):
        dir_name = os.path.dirname(path)
        os.makedirs(dir_name)
        
    @classmethod
    def write(cls, path, content):
        cls.ensure_dir(path)
        with open(path, 'w') as fp:
            fp.write(content)
    
    @classmethod
    def read(cls, path):
        with open(path, 'r') as fp:
            content = fp.read()
        return content
    
    @classmethod
    def serialize(cls, path, content):
        cls.write(path, json.dumps(content))
        
    @classmethod
    def unserialize(cls, path):
        return json.loads(cls.read(path))
    