import asyncio
import datetime
import imp
from importlib.resources import path
from tkinter import Image
from matplotlib import image
from mirai import MessageChain, Mirai, Plain, WebSocketAdapter, Startup, Shutdown
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import true
from mirai.models.message import MessageChain
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain,Image,Face
from myPack.bilibiliPack.bilibili import bilibili
if __name__ == '__main__':
    bot = Mirai(
        qq=2933469541, # 改成你的机器人的 QQ 号
        adapter=WebSocketAdapter(
            verify_key='yirimirai', host='localhost', port=8080
        )
    )

    @bot.on(GroupMessage)
    async def on_group_message(event:GroupMessage):
        

        #指定 /follow uid
        bili = bilibili()
        insList = str(event.message_chain).split(" ")
        if insList[0][0] == '/':

            if insList[0].strip('/') == 'follow':
                info = bili.getInfobyUid(insList[1])
                if info[0] == False:
                    result = bili.follow(insList[1])
                    if result == 0:
                        await bot.send(event,f'用户 {info[1]} 关注成功',quote=event.message_chain.message_id)
                    else:
                        await bot.send(event,f'用户 {info[1]} 关注失败',quote=event.message_chain.message_id)
                else:
                    await bot.send(event,f'用户 {info[1]} 已经关注，不能重复关注',quote=event.message_chain.message_id)       
            if insList[0].strip('/') == 'unfollow':
                info = bili.getInfobyUid(insList[1])
                if info[0] == True:
                    result = bili.unfollow(insList[1])
                    if result == 0:
                        await bot.send(event,f'用户 {info[1]} 取关成功',quote=event.message_chain.message_id)
                    else:
                        await bot.send(event,f'用户 {info[1]} 取关失败',quote=event.message_chain.message_id)
                else:
                    await bot.send(event,f'用户 {info[1]} 未关注，不能取关未关注用户',quote=event.message_chain.message_id)
            
            if insList[0].strip('/') == 'list':
                uidList,nameList = bili.getFollowAll()
                nameNuid = ''
                for uid in uidList:
                    # info = bili.getInfobyUid(uid)
                    nameNuid = nameNuid + nameList[uidList.index(uid)] + ' ' +str(uid) + '\n'
                await bot.send(event,f'{nameNuid}',quote=event.message_chain.message_id)
            
            # /search -b name 10 
            if insList[0].strip('/') == 'search':
                resultList = []
                if insList[1] == '-b' and len(insList) == 4:
                    resultList = bili.search(insList[2],int(insList[3])) #列表中为str，要转换类型
                    # print(resultList)
                    searchResult = ''
                    for result in resultList:
                        searchResult = searchResult + result +'\n'
                    await bot.send(event,f'{searchResult}',quote=event.message_chain.message_id)
                elif len(insList) == 2:
                    resultList = bili.search(insList[1])
                    await bot.send(event,f'{resultList[0]}',quote=event.message_chain.message_id)

        # if event.sender.id == 2282931136:
        #     await bot.send(event,'你好啊') 


    _task = None

    @bot.on(Startup)
    async def start_scheduler(_):
        async def timer():
            today_finished = False # 设置变量标识今天是会否完成任务，防止重复发送
            

            bili = bilibili()
            #初始化bot
            bili.botInit()

            live_finished = True
            # print(bili)
            while True:
                # await bot.send_friend_message(2282931136, "早安")
                # now = datetime.datetime.now()
                # if now.hour == 22:
                #     await bot.send_friend_message(2282931136, "早安")
                uidList = []
                uidList = bili.get_has_update()
                if uidList is not None:
                    for uid in uidList:

                        # #直播监听
                        # LiveInfo = bili.isLive(uid)
                        # if live_finished == True:
                        #     if LiveInfo[0] == 1:
                        #         live_finished = False #正在直播
                        #         LiveUrl = LiveInfo[1]
                        #         LivePic = LiveInfo[2]
                        #         LiveTitle = LiveInfo[3]
                        #         LiveName = LiveInfo[4]
                        #         message_chain = MessageChain([
                        #             Plain('{}正在直播{}\n{}'.format(LiveName,LiveTitle,LiveUrl)),
                        #             Image(url='{}'.format(LivePic))        
                        #         ])                               
                        #     else:
                        #         pass
                        # #直播已经开始
                        # if live_finished == False:
                        #     if LiveInfo[0] == 0:
                        #         live_finished = True
                        #     if LiveInfo[0] == 1:
                        #         live_finished = False

                        #

                        result = bili.get_dym_one(uid)
                        dymType = bili.get_dym_type(result)
                        imgList = []
                        if dymType == 1: #转发动态
                            originType = bili.isQuote(result)
                            print(originType)
                            if originType == 2: #图片
                                timestamp,name,content,originName,originContent,imgList,dynamic_id = bili.handle_dym(dymType,result)
                                nowTime = bili.timeChange(timestamp)
                                dymURL = bili.DymUrl(dynamic_id)
                                # print(f'{nowTime} {name} {content} {originName} {originContent} {imgList} {dynamic_id}')
                                # print(f'{name}转发了{originName}的动态:\n{nowTime}\n{content}\n原动态:\n{originContent}\n{imgList}\n{dymURL}')
                                message_chain = MessageChain([
                                    Plain('{}转发了{}的动态:\n{}\n{}\n\n原动态:\n{}\n'.format(name,originName,nowTime,content,originContent)),
                                    Image(url='{}'.format(imgList[0])),
                                    Plain('\n{}'.format(dymURL))
                                ])
                                # message_chain = MessageChain([
                                #     Plain('{}转发了动态:\n{}\n{}\n\n原动态:\n{}\n{}'.format(name,nowTime,content,originName,originContent)),
                                #     Image(url='{}'.format(imgList[0])),
                                #     Plain('\n{}'.format(dymURL))
                                # ])
                                await bot.send_friend_message(2282931136,message_chain=message_chain)
                                # print(f'{name}转发了{originName}的动态:\n{nowTime}\n{content}\n原动态:\n{originContent}\n{imgList}\n{dymURL}')

                            elif originType == 4: #文字
                                timestamp,name,content,originName,originContent,dynamic_id = bili.handle_dym(dymType,result)
                                nowTime = bili.timeChange(timestamp)
                                dymURL = bili.DymUrl(dynamic_id)
                                # print(f'{nowTime} {name} {content} {originName} {originContent} {imgList} {dynamic_id}')
                                message_chain = MessageChain([
                                    Plain('{}转发了{}的动态:\n{}\n{}\n\n原动态:\n{}'.format(name,originName,nowTime,content,originContent)),
                                    # Image(url='{}'.format(imgList[0])),
                                    Plain('\n{}'.format(dymURL))
                                ])
                                await bot.send_friend_message(2282931136,message_chain=message_chain)
                                # print(f'{name}转发了{originName}的动态:\n{nowTime}\n{content}\n原动态:\n{originContent}\n{imgList}\n{dymURL}')

                            elif originType == 8: #视频
                                timestamp,name,content,originVideoName,originVideoInfo,originVideoPic,originVideoTile,dynamic_id = bili.handle_dym(dymType,result)
                                nowTime = bili.timeChange(timestamp)
                                dymURL = bili.DymUrl(dynamic_id)
                                # print(f'{name}转发了{originVideoName}的投稿:\n{nowTime}\n{content}\n原视频:\n{originVideoTile}\n{originVideoInfo}\n{originVideoPic}\n{dymURL}')
                                message_chain = MessageChain([
                                    Plain('{}转发了{}的投稿:\n{}\n{}\n\n原视频:\n{}\n{}'.format(name,originVideoName,nowTime,content,originVideoTile,originVideoInfo)),
                                    Image(url='{}'.format(originVideoPic)),
                                    Plain('\n{}'.format(dymURL))
                                ])
                                # print(f'{name}转发了{originVideoName}的投稿:\n{nowTime}\n{content}\n原视频:\n{originVideoTile}\n{originVideoInfo}\n{originVideoPic}\n{dymURL}')
                                await bot.send_friend_message(2282931136,message_chain=message_chain)
                            
                            # listNone = []
                            # timestamp,name,content,originName,originContent,imgList,dynamic_id = bili.handle_dym(dymType,result)
                            # nowTime = bili.timeChange(timestamp)
                            # dymURL = bili.DymUrl(dynamic_id)
                            # # print(f'{nowTime} {name} {content} {originName} {originContent} {imgList} {dynamic_id}')
                            # print(f'{name}转发了{originName}的动态:\n{nowTime}\n{content}\n原动态:\n{originContent}\n{imgList}\n{dymURL}')
                            # if imgList != listNone:
                            #     message_chain = MessageChain([
                            #         Plain('{}转发了动态:\n{}\n{}\n\n原动态:\n{}\n{}'.format(name,nowTime,content,originName,originContent)),
                            #         Image(url='{}'.format(imgList[0])),
                            #         Plain('\n{}'.format(dymURL))
                            #     ])
                            # else:
                            #     message_chain = MessageChain([
                            #         Plain('{}转发了动态:\n{}\n{}\n\n原动态:\n{}\n{}'.format(name,nowTime,content,originName,originContent)),
                            #             # Image(url='{}'.format(imgList[0])),
                            #         Plain('\n{}'.format(dymURL))
                            #     ])
                            # await bot.send_friend_message(2282931136,message_chain=message_chain)
                            # await bot.send_friend_message(2282931136, f'{name}转发了{originName}的动态:\n{nowTime}\n{content}\n原动态:\n{originContent}\n{imgList}\n{dymURL}')

                        elif dymType == 2: #图片动态
                            timestamp,content,name,imgList,dynamic_id = bili.handle_dym(dymType,result)
                            nowTime = bili.timeChange(timestamp)
                            dymURL = bili.DymUrl(dynamic_id)
                            
                            message_chain = MessageChain([
                                Plain('{}发表了动态:\n{}\n{}\n'.format(name,nowTime,content)),
                                Image(url='{}'.format(imgList[0])),
                                Plain('\n{}'.format(dymURL))
                            ])
                            await bot.send_friend_message(2282931136,message_chain=message_chain)
                            
                        
                        elif dymType == 4: #文字动态
                            timestamp,content,name,dynamic_id = bili.handle_dym(dymType,result)
                            nowTime = bili.timeChange(timestamp)
                            dymURL = bili.DymUrl(dynamic_id)
                            # print(f'{nowTime} {content} {name} {dynamic_id}')
                            # print(f'{name}发表了动态:\n{nowTime}\n{content}\n{dymURL}')
                            # await bot.send_friend_message(2282931136, f'{name}发表了动态:\n{nowTime}\n{content}\n{dymURL}')
                            # await bot.send_friend_message(2282931136,f'{name}发表了动态:\n{nowTime}\n{content}\n{dymURL}')
                            await bot.send_friend_message(2282931136,[Plain("{}发表了动态:\n{}\n{}\n{}".format(name,nowTime,content,dymURL))])
                            # await bot.send_friend_message(2282931136,[Image(path='./image/github.png')])
                            # await bot.send_friend_message(2282931136,MessageChain[Plain(''.format(name))])
                        elif dymType == 8: #视频投稿
                            timestamp,VideoInfo,Videoname,VideoPic,VideoTitle,dynamic_id = bili.handle_dym(dymType,result) 
                            nowTime = bili.timeChange(timestamp)
                            dymURL = bili.DymUrl(dynamic_id)
                            message_chain = MessageChain([
                                Plain('{}投稿了新视频:\n{}\n{}\n{}'.format(Videoname,nowTime,VideoTitle,VideoInfo)),
                                Image(url='{}'.format(VideoPic)),
                                Plain('\n{}'.format(dymURL))
                            ])
                            await bot.send_friend_message(2282931136,message_chain=message_chain)
                await asyncio.sleep(1)
                

        global _task
        _task = asyncio.create_task(timer())

    @bot.on(Shutdown)
    async def stop_scheduler(_):
        # 退出时停止定时任务
        if _task and not _task.done():
            _task.cancel()

    scheduler = AsyncIOScheduler()

    @bot.on(Startup)
    def start_scheduler(_):
        scheduler.start() # 启动定时器

    @bot.on(Shutdown)
    def stop_scheduler(_):
        scheduler.shutdown(True) # 结束定时器

    bot.run()