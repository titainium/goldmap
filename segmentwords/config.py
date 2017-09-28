#!/usr/bin/env python

"""
some configureation parameters list here.

Titainium Deng
knifewolf@126.com
"""

from logging.handlers import TimedRotatingFileHandler

import logging
import os

__all__ = ['JIEBA_LOGGER']

logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s',
                    level=logging.DEBUG)

JIEBA_LOGGER = logging.getLogger("segmentwords.jieba")
JIEBA_LOGGER.addHandler(TimedRotatingFileHandler(os.path.join(os.getcwd(), 'jieba.log'), 'W6'))
