#!/usr/bin/env python

"""
some configureation parameters list here.

Titainium Deng
knifewolf@126.com
"""

from logging.handlers import TimedRotatingFileHandler

import logging
import os

__all__ = ['SANIC_LOGGER']

logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s',
                    level=logging.DEBUG)

SANIC_LOGGER = logging.getLogger("service.sanic")
SANIC_LOGGER.addHandler(TimedRotatingFileHandler(os.path.join(os.getcwd(), 'service.log'), 'W6'))
