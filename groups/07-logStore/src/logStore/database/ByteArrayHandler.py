from .SqLiteConnector import SqLiteConnector, ConnectorNotOpenError
from .SqlAlchemyConnector import SqLiteDatabase
from functions.log import create_logger
from functions.Singleton import Singleton
from functions.Event import Event, Meta

logger = create_logger('ByteArrayHandler')

SQLITE = 'sqlite'

CBORTABLE = 'cborTable'
EVENTTABLE = 'eventTable'


class ByteArrayHandler(metaclass=Singleton):
    __dbname = 'cborFilesDatabase'
    __tname = 'cborTable'
    __initiated = False

    def __init__(self):
        self.__sqlAlchemyConnector = SqLiteDatabase(SQLITE, dbname='cborDatabase.sqlite')
        self.__sqlAlchemyConnector.create_db_tables()

    def get_current_seq_no(self, feed_id):
        try:
            self.__connector.start_database_connection()
            result = self.__connector.get_current_seq_no(self.__tname, feed_id)
            self.__connector.close_database_connection()
            return result
        except ConnectorNotOpenError:
            return None

    def get_event(self, feed_id, seq_no):
        try:
            self.__connector.start_database_connection()
            result = self.__connector.get_event(self.__tname, feed_id, seq_no)
            self.__connector.close_database_connection()
            return result
        except ConnectorNotOpenError:
            return None

    def get_current_event_as_cbor(self, feed_id):
        res = self.__sqlAlchemyConnector.get_current_event_as_cbor(feed_id)
        return res

    def insert_byte_array(self, event_as_cbor):
        event = Event.from_cbor(event_as_cbor)
        seq_no = event.meta.seq_no
        feed_id = event.meta.feed_id.decode()
        self.__sqlAlchemyConnector.insert_byte_array(feed_id, seq_no, event_as_cbor)

    def is_init(self):
        return self.__initiated