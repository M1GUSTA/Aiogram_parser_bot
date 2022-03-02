import os
import re


class VK_selector:
    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file


    def group_def(self, response):
        self.group_id = response['response']['items'][0]['owner_id']
        print(self.group_id)
        with open(self.lastkey_file, 'r') as f:
            str = f.read()
            print(str)
            # str = re.findall(r'(-\d+)|(\d+)', str)
            str = re.findall(r'(\-\d+\b)|(\d+\b)', str)
            print(str)
            self.ids = {i: str[j+1] for j, i in enumerate(str) if j % 2 == 0}
        print(self.ids)
        if self.group_id in self.ids:
            lastkey = self.ids[self.group_id]
            print(lastkey)



if __name__ == '__main__':
    vs = VK_selector('lastkeys-file.txt')
    vs.test()