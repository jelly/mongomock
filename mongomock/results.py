try:
    from pymongo.results import DeleteResult
    from pymongo.results import InsertManyResult
    from pymongo.results import InsertOneResult
    from pymongo.results import UpdateResult
except ImportError:
    class _WriteResult(object):

        def __init__(self, acknowledged=True):
            self.__acknowledged = acknowledged

        @property
        def acknowledged(self):
            return self.__acknowledged

    class InsertOneResult(_WriteResult):

        __slots__ = ('__inserted_id', '__acknowledged')

        def __init__(self, inserted_id, acknowledged=True):
            self.__inserted_id = inserted_id
            super(InsertOneResult, self).__init__(acknowledged)

        @property
        def inserted_id(self):
            return self.__inserted_id

    class InsertManyResult(_WriteResult):

        __slots__ = ('__inserted_ids', '__acknowledged')

        def __init__(self, inserted_ids, acknowledged=True):
            self.__inserted_ids = inserted_ids
            super(InsertManyResult, self).__init__(acknowledged)

        @property
        def inserted_ids(self):
            return self.__inserted_ids

    class UpdateResult(_WriteResult):

        __slots__ = ('__raw_result', '__acknowledged')

        def __init__(self, raw_result, acknowledged=True):
            self.__raw_result = raw_result
            super(UpdateResult, self).__init__(acknowledged)

        @property
        def raw_result(self):
            return self.__raw_result

        @property
        def matched_count(self):
            if self.upserted_id is not None:
                return 0
            return self.__raw_result.get('n', 0)

        @property
        def modified_count(self):
            return self.__raw_result.get('nModified')

        @property
        def upserted_id(self):
            return self.__raw_result.get('upserted')

    class DeleteResult(_WriteResult):

        __slots__ = ('__raw_result', '__acknowledged')

        def __init__(self, raw_result, acknowledged=True):
            self.__raw_result = raw_result
            super(DeleteResult, self).__init__(acknowledged)

        @property
        def raw_result(self):
            return self.__raw_result

        @property
        def deleted_count(self):
            return self.__raw_result.get('n', 0)
