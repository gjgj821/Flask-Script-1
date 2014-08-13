# coding=utf-8
"""
creative的脚本任务
"""
from auto.decorators import action
from common.decorators import responsed
from common.framework import get_module_blueprint, get_current_logger
from auto.task import blueprint_list
from auto import app, logger as parent_logger

__author__ = 'GaoJie'
task = get_module_blueprint(blueprint_list, __name__)
logger = get_current_logger(app, __name__)
action_list = []


@action(action_list)
@task.route('/cache')
@responsed
def cache():
    logger.debug(12312312)