import json

class CacheHandler(object):
    @classmethod
    def write(cls, path, content):
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
    