CREATE TABLE IF NOT EXISTS executors
(
    id          SERIAL PRIMARY KEY,
    telegram_id bigint,
    quest_list  text[]
);

CREATE TABLE IF NOT EXISTS checkers
(
    id         SERIAL PRIMARY KEY,
    quest_list text[]
);

CREATE TABLE IF NOT EXISTS tasks
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    fi2         TEXT[],
    files       TEXT[],
    status      VARCHAR(255),
    time        TIMESTAMP,
    checker_id  INTEGER,
    worker_list INTEGER[]
);

----------------------------------------------------------------------------------------------------------

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

select add_task(
               'Task Name342',
               'Task Description',
               'Pending',
               '2023-07-05 11:00:00',
               2
           );

----------------------------------------------------------------------------------------------------------

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


-- Добавление значений к массиву в столбце files для задачи с именем "Task Name"
SELECT update_task_files('Task Name4', 'files', ARRAY ['new_file112.txt', 'new_file24.txt']);

----------------------------------------------------------------------------------------------------------

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


-- Добавление значений к массиву в столбце worker_list для задачи с именем "Task Name"
SELECT update_task_worker_list('Task Name411', 'worker_list', ARRAY [21451, 555]);

----------------------------------------------------------------------------------------------------------

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

-- Получение длины массива в столбце files для задачи с именем "Task Name"
SELECT get_array_length('Task Name', 'files');

----------------------------------------------------------------------------------------------------------

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

-- Замена статуса задачи с именем "Task Name" на "Completed"
SELECT update_task_status('Task Name', 'Completed');

----------------------------------------------------------------------------------------------------------

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

-- Получение массива значений из столбца files для задачи с именем "Task Name"
SELECT get_array_values('Task Name', 'worker_list');

----------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_task_data(
    p_task_name VARCHAR(255)
)
    RETURNS TABLE
            (
                task_name        VARCHAR(255),
                task_description TEXT,
                task_fi2         TEXT[],
                task_files       TEXT[],
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
               fi2         AS task_fi2,
               files       AS task_files,
               status      AS task_status,
               time        AS task_time,
               checker_id  AS checkers_id,
               worker_list AS worker_lists
        FROM tasks
        WHERE name = p_task_name;
END;
$$ LANGUAGE plpgsql;

SELECT *
FROM get_task_data('Task Name');

----------------------------------------------------------------------------------------------------------

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

SELECT get_task_names_by_worker(2);

----------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION insert_executor(p_telegram_id bigint)
    RETURNS VOID AS
$$
BEGIN
    INSERT INTO executors (telegram_id)
    VALUES (p_telegram_id);
END;
$$ LANGUAGE plpgsql;


SELECT insert_executor(555);

----------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_quest_list()
    RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.worker_list IS NOT NULL THEN
        -- Добавление имени в quest_list таблицы executors
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

DROP TRIGGER IF EXISTS task_worker_list_trigger ON tasks;

