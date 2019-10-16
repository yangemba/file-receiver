"""Application for gathering files and collecting statistics"""
import logging
import tornado.web
import tornado.ioloop
from base_handler import RequestHandler
from models import FileModel


def setup_logging():
    logger = logging
    return logger


def get_data_list(file_data):
    """Function for transforming data from file do list of dicts"""
    dict_list = []
    for pare in file_data:
        pare_list = pare.split(':')
        pare_dict = {pare_list[0]: pare_list[1]}
        dict_list.append(pare_dict)
    return dict_list


class FileManagerHandler(RequestHandler):
    """Handler for Managing files operations"""
    methods = ["GET", "POST"]

    def get(self):
        """GET method for gathering statistics from fies with common uuid"""
        try:
            uuid = self.get_query_argument('uuid')
            file_group = [x for x in file_list_holder if x.uuid == uuid]
        except Exception as e:
            return self.finish_with_error(code=400, detail={"error:":
                                                            "Wrong uuid"})
        if len(file_group) == 0:
            return self.finish_with_error(code=400, detail={"error:":
                                                            "Wrong uuid"})

        response = {}
        for x in file_group:
            result = {x.name: x.process()}
            response.update(result)

        return self.finish(response)

    async def post(self):
        """"POST method that reciev files in form
         data with uuid in as query parameter"""
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
            dict_list = get_data_list(file_data)
            logging.warning(f'Dict - data {dict_list} type -'
                            f' {type(dict_list)}')
        except Exception as e:
            logging.warning(f"Error format validation")
            return self.finish_with_error(code=400, detail={'Validation error':
                                                            f'{e}'})

        key_list = [list(x.keys()) for x in dict_list]
        value_list = [list(x.values()) for x in dict_list]

        pure_key_list = []
        for x in key_list:
            pure = x[0]
            pure_key_list.append(pure)

        pure_value_list = []
        for x in value_list:
            pure = int(x[0])
            pure_value_list.append(pure)

        file_obj = FileModel(data_list=dict_list,
                             uuid=uuid,
                             name=file_name,
                             key_list=pure_key_list,
                             value_list=pure_value_list
                             )
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
