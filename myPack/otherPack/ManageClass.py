class Manage():
    def __init__(self):
        # self.lines = open('./Manage.txt',encoding='utf-8').read().splitlines()
        pass
    def isManage(self,QQ_id):
        lines = open('./File/Manage.txt',encoding='utf-8').read().splitlines()
        if QQ_id in lines:
            return True
        else:
            return False
    
    def AddManage(self,QQ_id):
        lines = open('./File/Manage.txt',encoding='utf-8').read().splitlines()
        if QQ_id in lines:
            return
        else:
            file = open('./File/Manage.txt','a+',encoding='utf-8')
            file.write(f'{QQ_id}\n')
            file.close()
    def RemoveManage(self,QQ_id):
        lines = open('./File/Manage.txt',encoding='utf-8').read().splitlines()
        file = open('./File/Manage.txt','w+',encoding='utf-8')
        #lines = open('./Manage.txt',encoding='utf-8').read().splitlines()
        for li in lines:
            if QQ_id not in li:
                
                file.write(li+'\n')
        file.close()