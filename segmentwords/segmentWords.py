#!/usr/bin/env python

"""
some configureation parameters list here.

Titainium Deng
knifewolf@126.com
"""

import asyncio
import os
import re
import sys

from pyArango import connection

import jieba
import uvloop

from config import JIEBA_LOGGER

class BaseCutter:
    """
    A word segment class base on jieba library
    """
    
    def __init__(self):
        self.__conn = connection.Connection(username = 'goldmapAdmin', password = 'openSUSE2000$')
        self.__db = self.__conn['goldmapDevDB']

    async def load_user_dict(self):
        try:
            sys.path.append(os.getcwd())

            jieba.load_userdict("user_dict.txt")
        except:
            JIEBA_LOGGER.exception("jieba.load_user_dict_message")

    async def get_start_id(self):
        try:
            site_doc = self.__db.fetchDocument('fin_sites/wallstreetcn')
        
            return site_doc['jieba_start_id']
        except:
            JIEBA_LOGGER.exception("jieba.get_start_id_message")

    async def get_text(self, id):
        try:
            docs_aql = "FOR doc IN fin_articles FILTER doc.idx == @idx RETURN doc.content"
            bind_vars = {'idx': id}
            docs = self.__db.AQLQuery(docs_aql,
                                      rawResults = True,
                                      batchSize = 1,
                                      bindVars = bind_vars)

            return (docs[0], id) if len(docs) > 0 else ('', '')
        except:
            JIEBA_LOGGER.exception("jieba.get_text_message")

    async def segment_words(self, doc, idx):
        try:
            move_pattern = re.compile("[\s+\.\!\/_,$%^*-·()+\"\']+|[+——！，。？、~@#￥%……&*（）“”；：─《》丨／•％①②③]+|[0-9]+|[a-zA-Z]")
            seg_list = jieba.lcut(re.sub(move_pattern, "", doc))
            seg_coll = self.__db['seg_articles']
            seg_doc = seg_coll.createDocument()
            seg_doc['content'] = seg_list
            
            seg_doc.save()

            site_doc = self.__db.fetchDocument('fin_sites/wallstreetcn')
            site_doc['jieba_start_id'] = idx

            site_doc.save()
        except:
            JIEBA_LOGGER.exception("jieba.segment_words_message")
    
    async def stop_words(self, word):
        try:
            stop_words_coll = self.__db['stop_wrods']
            stop_wrod = stop_words_coll.createDocument()
            stop_word['word'] = word

            stop_word.save()
        except expression as identifier:
            JIEBA_LOGGER.exception("jieba.stop_words_message")

async def main():
    try:
        seg_words = BaseCutter()
    
        await seg_words.load_user_dict()

        start_id = await seg_words.get_start_id()

        for idx in range(10):
            seg_doc, seg_idx = await seg_words.get_text(int(start_id) + idx)
            
            if seg_doc != '':
                await seg_words.segment_words(seg_doc, seg_idx)
    except:
        JIEBA_LOGGER.exception("jieba.main_message")

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    