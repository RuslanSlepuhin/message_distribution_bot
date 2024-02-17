import sqlite3
from coffee_bot import variables

def wrapper_connection(func):
    def wrapper(self):
        print('wrapper')
        self.conn = sqlite3.connect(variables.database_location_path) if not self.conn else self.conn
        return func(self)
    return wrapper

class DBMethods:

    def __init__(self):
        self.conn = None

    def create_all_tables(self):
        self.connection_with()
        for create_table_sql in [variables.barista_sql_create, variables.user_sql_create]:
            self.create_table(create_table_sql)

    # @wrapper_connection
    def create_table(self, create_table_sql):
        print('create_table')
        print('table was created') if self.execute_query(create_table_sql) else print('table was not created')

    def connection_with(self):
        self.conn = sqlite3.connect(variables.database_location_path) if not self.conn else self.conn

    def execute_query(self, query, **kwargs) -> bool:
        self.conn = self.connection_with() if not self.conn else self.conn
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(query)
            if 'select' in kwargs.keys():
                return cur.fetchall()
        return True

    def insert_into(self, table_name, data:dict, **kwargs) -> bool:
        fields, values = self.get_pair_fields_values(data)
        query = f"""INSERT INTO {table_name} ({fields}) VALUES ({values})"""
        if kwargs.get('set_unique') and kwargs['set_unique']:
            if not self.select_from(table_name, kwargs['set_unique']):
                return True if self.execute_query(query) else False
        else:
            return True if self.execute_query(query) else False

    def update(self, table_name, conditions, data, **kwargs):

        conditions = f"""WHERE {self.get_pair_field_equal_value(conditions)}"""
        # if kwargs.get('max_id'):
        #     conditions += " AND id=MAX(id)"
        expression = self.get_pair_update(data)
        query = f"""UPDATE {table_name} SET {expression} {conditions}"""
        return True if self.execute_query(query) else False

    def select_from(self, table_name, data:dict, **kwargs) -> bool:
        if data:
            conditions = self.get_pair_field_equal_value(data)
            query = f"""SELECT * FROM {table_name} WHERE {conditions}"""
        else:
            query = f"""SELECT * FROM {table_name}"""
        responses = self.execute_query(query, select=True)
        if kwargs.get('select'):
            return responses
        else:
            return True if responses else False

    def get_pair_fields_values(self, data):
        fields, values = "", ""
        for key in data:
            fields += f"{key}, "
            values += f"{data[key]}, " if type(data[key]) in [int, float] else f"'{data[key]}', "
        return fields[:-2], values[:-2]

    def get_pair_field_equal_value(self, data) -> str:
        expression = ""
        for key in data:
            expression += f"{key}={data[key]} AND " if type(data[key]) in [int, float] else f"{key}='{data[key]}' AND "
        return expression[:-5]

    def get_pair_update(self, data) -> str:
        expression = ""
        for key in data:
            expression += f"{key}={data[key]}, " if type(data[key]) in [int, float] else f"{key}='{data[key]}', "
        return expression[:-2]

    def delete_data(self, table_name, data):
        data = self.get_pair_field_equal_value(data)
        query = f"""DELETE FROM {table_name} WHERE {data}"""
        return True if self.execute_query(query) else False


# if __name__ == '__main__':
#     db = DBMethods()
#     db.create_table_barista()
