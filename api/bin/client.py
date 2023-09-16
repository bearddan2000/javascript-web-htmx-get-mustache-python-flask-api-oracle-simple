import oracledb

class OracleClient:
    
    def __init__(self) -> None:
        host = "db"
        port = 1521
        service_name = "FREE"
        self.username="system"
        self.userpwd = 'pass'
        self.dsn = f'{host}:{port}/{service_name}'
        self.params = oracledb.ConnectParams(host=host, port=port, service_name=service_name)
        self.isSeeded = False

    def __cursor_execute(self, cursor, sql, param: dict=None):
        if param is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, param)

    def __read_sql_file(self, filename):
        data = None
        with open(filename, 'r') as file:
            data = file.read().rstrip()
        self.command(data)

    def command(self, sql, param: dict=None):
        with oracledb.connect(user=self.username, password=self.userpwd, params=self.params) as connection:
            with connection.cursor() as cursor:
                self.__cursor_execute(cursor, sql, param)
                connection.commit()

    def query(self, sql, param: dict=None):
        results = []
        with oracledb.connect(user=self.username, password=self.userpwd, dsn=self.dsn) as connection:
            with connection.cursor() as cursor:
                self.__cursor_execute(cursor, sql, param)
                res = cursor.fetchall()
                for row in res:
                    results.append(row)
        return [
            {
                "id": r[0],
                "breed": r[1],
                "color": r[2]
            } for r in results]

    def seed(self):
        if self.isSeeded == True:
            return

        self.__read_sql_file('create_table.sql')
        self.__read_sql_file('ins_table.sql')
        self.isSeeded = True

class Endpoint:
    """Create singleton"""
    def __new__(cls):
         if not hasattr(cls, 'instance'):
             cls.instance = super(Endpoint, cls).__new__(cls)
         return cls.instance
    
    def __init__(self) -> None:
        self.client = OracleClient()

    def get_all(self):
        self.client.seed()
        sql = 'select * from dog'
        return self.client.query(sql)
    
    def filter_by(self, filter, filter_val):
        self.client.seed()
        d: dict = {'param': filter_val}
        sql = f'select * from dog where {filter} = :param'
        return self.client.query(sql, d)
    
    def delete(self, filter, filter_val):
        self.client.seed()
        d: dict = {'param': filter_val}
        sql = f'delete from dog where {filter} = :param'
        self.client.command(sql, d)
        return self.get_all()
    
    def insert(self, new_breed, new_color):
        self.client.seed()
        d: dict = {'param1': new_breed, 'param2': new_color}
        sql = "insert into dog (breed, color) values (:param1, :param2)"
        self.client.command(sql, d)
        return self.get_all()
    
    def update(self, filter, filter_val):
        self.client.seed()
        d: dict = {'param': filter_val}
        sql = f"update dog set breed = 'updated', color = 'updated' where {filter} = :param"
        self.client.command(sql, d)
        return self.get_all()