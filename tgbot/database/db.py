import psycopg2
from environs import Env
from datetime import datetime

env = Env()
env.read_env()


def connect():
    conn = psycopg2.connect(
        host=env('DB_HOST'),
        port=env('POSTGRES_PORT'),
        user=env('POSTGRES_USER'),
        password=env('POSTGRES_PASSWORD'),
        database=env('POSTGRES_DB')
    )
    return conn


def create_executors_table():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS executors(
            id          SERIAL PRIMARY KEY,
            telegram_id bigint,
            quest_list  text[]
        )
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def create_checkers_table():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS checkers(
            id         SERIAL PRIMARY KEY,
            quest_list text[]
        )
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def create_tasks_table():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks(
            id          SERIAL PRIMARY KEY,
            name        VARCHAR(255) NOT NULL,
            description TEXT,
            ams_files         TEXT[],
            apparat_files       TEXT[],
            afy_files       TEXT[],
            materials_files       TEXT[],
            status      VARCHAR(255),
            time        TIMESTAMP,
            checker_id  INTEGER,
            worker_list INTEGER[]
        );
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def update_task_files_function():
    conn = connect()
    cursor = conn.cursor()

    update_task_query = '''
    CREATE OR REPLACE FUNCTION update_task_files(
        task_name VARCHAR(255),
        column_name VARCHAR(255),
        task_files TEXT[]
    )
    RETURNS VOID AS
    $$
    BEGIN
        EXECUTE format('UPDATE tasks SET %I = %I || $1 WHERE name = $2', column_name,
                       column_name) USING task_files, task_name;
    END;
    $$ LANGUAGE plpgsql;
        '''

    cursor.execute(update_task_query)
    conn.commit()
    cursor.close()
    conn.close()


def create_add_task_function():
    conn = connect()
    cursor = conn.cursor()

    create_function_query = '''
    CREATE OR REPLACE FUNCTION add_task(
        task_name VARCHAR(255),
        task_description TEXT,
        task_status VARCHAR(255),
        task_time TIMESTAMP WITH TIME ZONE,
        task_checker_id INTEGER
    )
        RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO tasks (name, description, status, time, checker_id)
        VALUES (task_name, task_description, task_status, task_time, task_checker_id);
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_function_query)
    conn.commit()
    cursor.close()
    conn.close()


def add_task(task_name, task_description, task_status, task_time, checker_id):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT add_task(
            %s,
            %s,
            %s,
            %s,
            %s
           );
    '''

    task_data = (
        task_name,
        task_description,
        task_status,
        task_time,
        checker_id
    )

    cursor.execute(create_table_query, task_data)
    conn.commit()
    cursor.close()
    conn.close()


def add_task_files(task_name, column_name, task_files):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT update_task_files(
            %s,
            %s,
            %s
        );

    '''

    task_data = (
        task_name,
        column_name,
        task_files
    )

    cursor.execute(create_table_query, task_data)
    conn.commit()
    cursor.close()
    conn.close()


def update_task_worker_list_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION update_task_worker_list(
    task_name VARCHAR(255),
    column_name VARCHAR(255),
    task_worker_list INTEGER[]
        )
        RETURNS VOID AS
    $$
    BEGIN
    EXECUTE format('UPDATE tasks SET %I = %I || $1 WHERE name = $2', column_name,
                   column_name) USING task_worker_list, task_name;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def add_task_worker(task_name, column_name, task_worker_list):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT update_task_worker_list(
            %s,
            %s,
            %s
        );

    '''

    task_data = (
        task_name,
        column_name,
        task_worker_list
    )

    cursor.execute(create_table_query, task_data)
    conn.commit()
    cursor.close()
    conn.close()


def get_array_len_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION get_array_length(
    task_name VARCHAR(255),
    column_name VARCHAR(255)
        )
        RETURNS INTEGER AS
    $$
    DECLARE
    array_length INTEGER;
    BEGIN
    EXECUTE format('SELECT array_length(%I, 1) FROM tasks WHERE name = $1', column_name)
        INTO array_length
        USING task_name;

    RETURN array_length;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def get_array_len(name, column_name):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT get_array_length(
            %s,
            %s
        );

    '''

    task_data = (
        name,
        column_name
    )

    cursor.execute(create_table_query, task_data)
    res = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return res


def update_task_status_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION update_task_status(
    task_name VARCHAR(255),
    new_status VARCHAR(255)
        )
        RETURNS VOID AS
    $$
    BEGIN
        UPDATE tasks SET status = new_status WHERE name = task_name;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def update_task_status(task_name, new_status):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT update_task_status(
            %s,
            %s
        );

    '''

    task_data = (
        task_name,
        new_status
    )

    cursor.execute(create_table_query, task_data)
    conn.commit()
    cursor.close()
    conn.close()


def get_array_value_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION get_array_values(
    task_name VARCHAR(255),
    column_name VARCHAR(255)
        )
        RETURNS TEXT[] AS
    $$
    DECLARE
        array_values TEXT[];
    BEGIN
        EXECUTE format('SELECT %I FROM tasks WHERE name = $1', column_name)
            INTO array_values
            USING task_name;

        RETURN array_values;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def get_array_values(name, column_name):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT get_array_values(
            %s,
            %s
        );

    '''

    task_data = (
        name,
        column_name
    )

    cursor.execute(create_table_query, task_data)
    res = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return res


def get_task_data_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    
    CREATE OR REPLACE FUNCTION get_task_data(
        p_task_name VARCHAR(255)
        )
        RETURNS TABLE
            (
                task_name        VARCHAR(255),
                task_description TEXT,
                task_ams_files         TEXT[],
                task_apparat_files       TEXT[],
                task_afy_files       TEXT[],
                task_materials_files       TEXT[],
                task_status      VARCHAR(255),
                task_time        TIMESTAMP,
                checkers_id      INTEGER,
                worker_lists     INTEGER[]
            )
    AS
    $$
    BEGIN
        RETURN QUERY
            SELECT name         AS task_name,
                description     AS task_description,
                ams_files       AS task_ams_files,
                afy_files       AS task_afy_files,
                apparat_files   AS task_apparat_files,
                materials_files AS task_materials_files,
                status          AS task_status,
                time            AS task_time,
                checker_id      AS checkers_id,
                worker_list     AS worker_lists
        FROM tasks
        WHERE name = p_task_name;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def get_task_data(task_name):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT get_task_data(
            %s
        );

    '''

    task_data = (
        task_name,
    )

    cursor.execute(create_table_query, task_data)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res


def get_task_name_by_worker_id_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION get_task_names_by_worker(worker_id INTEGER)
    RETURNS VARCHAR(255)[] AS
    $$
    DECLARE
        task_names VARCHAR(255)[];
    BEGIN
        SELECT ARRAY(
                   SELECT name
                   FROM tasks
                   WHERE worker_id = ANY (worker_list)
               )
        INTO task_names;

        RETURN task_names;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def get_task_names_by_worker_id(worker_id):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT get_task_names_by_worker(
            %s
        );

    '''

    task_data = (
        worker_id,
    )

    cursor.execute(create_table_query, task_data)
    res = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return res


def insert_executor_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION insert_executor(p_telegram_id bigint)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO executors (telegram_id)
        VALUES (p_telegram_id);
    END;
    $$ LANGUAGE plpgsql;
    '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def insert_executor(telegram_id):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT insert_executor(
            %s
        );

    '''

    task_data = (
        telegram_id,
    )

    cursor.execute(create_table_query, task_data)
    conn.commit()
    cursor.close()
    conn.close()


def update_quest_list_trigger_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION update_quest_list()
    RETURNS TRIGGER AS
    $$
    BEGIN
        IF NEW.worker_list IS NOT NULL THEN
            UPDATE executors
            SET quest_list = array_append(quest_list, tasks.name)
            FROM tasks
            WHERE tasks.name = NEW.name
                AND executors.telegram_id = ANY (NEW.worker_list);
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER task_worker_list_trigger
        AFTER UPDATE OF worker_list
        ON tasks
        FOR EACH ROW
    EXECUTE FUNCTION update_quest_list();
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def find_task_by_worker_and_status_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION find_tasks_by_status_and_worker(
        search_int INT,
        search_status VARCHAR(255)
    )
        RETURNS TABLE (name VARCHAR(255)) AS
    $$
    BEGIN
        RETURN QUERY EXECUTE format('
            SELECT name
            FROM tasks
            WHERE status = $1 AND $2 = ANY(worker_list)'
        ) USING search_status, search_int;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def search_by_status_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION find_tasks_by_status(
        search_status VARCHAR(255)
    )
    RETURNS TABLE (task_name VARCHAR(255)) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT tasks.name AS task_name
        FROM tasks
       WHERE tasks.status = search_status;
    END;
    $$ LANGUAGE plpgsql;

    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

def search_by_status(status):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT find_tasks_by_status(
        %s
    );
    '''

    task_data = (
        status,
    )

    cursor.execute(create_table_query, task_data)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def find_tasks_by_checker_and_status_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    
    CREATE OR REPLACE FUNCTION find_tasks_by_checker_and_status(
        p_checker_id INTEGER,
        p_status VARCHAR(255)
        )
        RETURNS TABLE
            (
                task_name        VARCHAR(255),
                task_description TEXT,
                task_ams_files         TEXT[],
                task_apparat_files       TEXT[],
                task_afy_files       TEXT[],
                task_materials_files       TEXT[],
                task_status      VARCHAR(255),
                task_time        TIMESTAMP,
                checkers_id      INTEGER,
                worker_lists     INTEGER[]
            )
    AS
    $$
    BEGIN
        RETURN QUERY
        SELECT name        AS task_name,
               description AS task_description,
               ams_files           AS task_ams_files,
               apparat_files AS task_apparat_files,
               afy_files   AS task_afy_files,
               materials_files AS task_materials_files,
               status      AS task_status,
               time        AS task_time,
               checker_id  AS checkers_id,
               worker_list AS worker_lists
    FROM tasks
    WHERE tasks.checker_id = p_checker_id
    AND tasks.status = p_status;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def find_tasks_by_checker_and_status(checker_id, status):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT find_tasks_by_checker_and_status(
        %s,
        %s
    );
    '''

    task_data = (
        checker_id,
        status
    )

    cursor.execute(create_table_query, task_data)
    res = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return res


def find_task_by_worker_and_status(tg_id, status):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT find_tasks_by_checker_and_status(
        %s,
        %s
    );
    '''

    task_data = (
        tg_id,
        status
    )

    cursor.execute(create_table_query, task_data)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res


def get_task_by_name_function():
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    CREATE OR REPLACE FUNCTION get_task_by_name(
        task_name VARCHAR(255)
    )
        RETURNS SETOF tasks AS
    $$
    BEGIN
        RETURN QUERY
        SELECT *
        FROM tasks
        WHERE name = task_name;
    END;
    $$ LANGUAGE plpgsql;
    '''

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


def get_task_by_name(task_name):
    conn = connect()
    cursor = conn.cursor()

    create_table_query = '''
    SELECT get_task_by_name(
        %s
    );
    '''

    task_data = (
        task_name,
    )

    cursor.execute(create_table_query, task_data)
    res = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return res


def get_task_where_menya_net(id):
    conn = connect()
    cursor = conn.cursor()

    sql_query = """
    SELECT name
    FROM tasks
    WHERE status = 'active'
      AND NOT %s = ANY(worker_list);
    """

    cursor.execute(sql_query, (id,))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def database_init():
    create_executors_table()
    create_checkers_table()
    create_tasks_table()
    create_add_task_function()
    update_task_files_function()
    update_task_status_function()
    update_task_worker_list_function()
    get_array_len_function()
    get_array_value_function()
    get_task_data_function()
    get_task_name_by_worker_id_function()
    update_quest_list_trigger_function()
    find_task_by_worker_and_status_function()
    find_tasks_by_checker_and_status_function()
    insert_executor_function()
    get_task_by_name_function()

    print('Таблицы созданы')


# if __name__ == '__main__':
#     update_task_worker_list_function()