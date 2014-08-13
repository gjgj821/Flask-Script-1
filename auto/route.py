# coding=utf-8
import sys
from common.decorators import responsed
from flask import request
from auto import app
# 导入任务模块，初始化
import auto.task
__author__ = 'GaoJie'


@app.route('/test', methods=['post', 'get'])
@responsed
def test():
    if request.method == 'post':
        print 'Post:', request.form
    elif request.method == 'get':
        print 'Get:', request.args


@app.errorhandler(404)
@responsed
def choose_task_404(e):
    def tips_module(package_module, package_name, module_name=None):
        try:
            module_list = getattr(package_module, 'module_list')
            package_list = getattr(package_module, 'package_list')
        except AttributeError as e:
            print 'No Define Module List and Package List'
            return False, []
        allow_list = module_list + package_list
        if module_name not in allow_list:
            if len(module_list) > 0:
                print '%s List: %s' % (package_name.capitalize(), ' , '.join(module_list))
            if len(package_list) > 0:
                print '%s Package: %s' % (package_name.capitalize(), ' , '.join(package_list))
            return False, []
        return True, package_list

    def tips_import(current_module_full, model_name, action_name):
        try:
            __import__(current_module_full)
        except ImportError as e:
            print '%s(%s) is allowed, but does not exist!' % (model_name.capitalize(), action_name)
            return False
        print '%s: %s ' % (model_name.capitalize(), action_name)
        return sys.modules[current_module_full]

    def tips_action(current_module, action_name=None):
        try:
            # 需在每个模块中添加action_list，用于判断可以执行的
            action_list = getattr(current_module, 'action_list')
        except AttributeError as e:
            print 'No Define Action List'
            return False
        if action_name not in action_list:
            print 'Action List: %s ' % [value for value in action_list]
            return False

    path_list = request.path[1:].split('/')
    app_task = '%s.task' % __package__
    model = 'task'
    current_module = sys.modules[app_task]
    package = True
    path_list = [path for path in path_list if path]
    result = False

    if len(path_list) > 0:
        for index, path in enumerate(path_list):
            app_task = '%s.%s' % (app_task, path)
            parent_module = current_module
            if package:
                result, package_list = tips_module(parent_module, model, path)
            else:
                result = tips_action(parent_module, path)
                break
            if not result:
                break
            current_module = tips_import(app_task, model, path)
            package = True if path in package_list else False
            model = path
        if result:
            if package:
                tips_module(current_module, model)
            else:
                tips_action(current_module)
    else:
        tips_module(current_module, model)

# app.add_url_rule('/index', view_func=index)