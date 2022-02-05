class Block():
    def __init__(self,QQ_id):
        self.QQ_id = QQ_id

    def inList(self):
        lines = open('./File/block.txt',encoding='utf-8').read().splitlines()
        if self.QQ_id in lines:
            return True
        else:
            return False

    def AddBlock(self):
        lines = open('./File/block.txt',encoding='utf-8').read().splitlines()
        if self.QQ_id in lines:
            return
        else:
            file = open('./File/block.txt','a+',encoding='utf-8')
            file.write(f'{self.QQ_id}\n')
            file.close()
    def RemoveBlock(self):
        lines = open('./File/block.txt',encoding='utf-8').read().splitlines()
        file = open('./File/block.txt','w+',encoding='utf-8')
        for li in lines:
            if self.QQ_id not in li:
                print(li)
                file.write(li+'\n')
        file.close()