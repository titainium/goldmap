#!/usr/bin/env python

"""
some configureation parameters list here.

Titainium Deng
knifewolf@126.com
"""

from logging.handlers import TimedRotatingFileHandler

import logging
import os

__all__ = ['JINTEN_LOGGER']

logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s',
                    level=logging.DEBUG)

JINTEN_LOGGER = logging.getLogger("webCrawler.jinten")
JINTEN_LOGGER.addHandler(TimedRotatingFileHandler(os.path.join(os.getcwd(), 'jinten.log'), 'W6'))
