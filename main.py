"""Application for gathering files and collecting statistics"""
import json
import time
import logging
import tornado.web
import tornado.ioloop
from base_handler import RequestHandler
from models import FileModel
import codecs


def setup_logging():
    logger = logging
    return logger


def get_data_dict(file_data):
    dict_data = dict()
    for pare in file_data:
        pare_list = pare.split(':')
        pare_dict = {pare_list[0]: pare_list[1]}
        dict_data.update(pare_dict)
    return dict_data


class FileManagerHandler(RequestHandler):
    methods = ["POST"]

    def post(self):
        file1 = self.request.files['file'][0]
        file_name = file1.get('filename')   # not sure
        uuid = self.get_query_argument('uuid')
        required_data = [file1, uuid]
        for field in required_data:
            if not field:
                return self.finish_with_error(code=400,
                                              detail={'Error': 'No required'
                                                               'param: '
                                                               f'{field}'})

        try:
            file = str(file1.body, 'utf-8')
            file_data = file.split('\n')
            for x in file_data:
                if x == '':
                    file_data.remove(x)
            dict_data = get_data_dict(file_data)
        except Exception as e:
            logging.warning(f"Error format validation")
            return self.finish_with_error(code=400, detail={'Validation error':
                                                            f'{e}'})

        file_obj = FileModel(data_dict=dict_data,
                             uuid=uuid,
                             name=file_name)
        logging.warning(f'{file_obj.key_list, file_obj.value_list}')
        file_list_holder.append(file_obj)
        logging.warning(f'{file_list_holder}')

        return self.finish()


if __name__ == "__main__":
    application = tornado.web.Application(logging=setup_logging(),
                                          handlers=[(r"/",
                                                     FileManagerHandler)],
                                          )
    application.listen(8888)
    file_list_holder = []
    tornado.ioloop.IOLoop.current().start()


