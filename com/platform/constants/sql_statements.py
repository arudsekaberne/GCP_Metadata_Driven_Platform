from com.platform.constants.placeholders import Placeholder
from com.platform.constants.common_variables import CommonVariables


class SqlStatements:

    """Immutable module which holds all platform bigquery sql statements (only getter enabled)"""

    # Restrict new variable creation and modification
    def __setattr__(self, name, value):
        raise AttributeError(f"Cannot create or set class or instance attribute '{name}'")


    # Collector statements
    REF_SELECT_STATEMENT = f"""
        SELECT * FROM {CommonVariables.REF_TABLE_IDN}
        WHERE process_id = {Placeholder.PROCESS_ID.value}
        ORDER BY last_modified_utc DESC LIMIT 1;        
    """

    REF_LOG_INSERT_STATEMENT = f"""
        INSERT INTO {CommonVariables.REF_LOG_TABLE_IDN} (batch_id, batch_code, process_id, batch_date, batch_sequence, status, start_timestamp)
        VALUES (
            (SELECT CASE WHEN MAX(batch_id) IS NULL THEN 1 ELSE MAX(batch_id) + 1 END FROM {CommonVariables.REF_LOG_TABLE_IDN}),
            CONCAT({Placeholder.PROCESS_ID.value}, '_', FORMAT_DATE('%Y%m%d', CURRENT_DATE()), '_', (SELECT CASE WHEN MAX(batch_sequence) IS NULL THEN 1 ELSE MAX(batch_sequence) + 1 END FROM {CommonVariables.REF_LOG_TABLE_IDN} WHERE process_id = {Placeholder.PROCESS_ID.value} AND batch_date = '{Placeholder.BATCH_DATE.value}')),
            {Placeholder.PROCESS_ID.value},
            CURRENT_DATE(),
            (SELECT CASE WHEN MAX(batch_sequence) IS NULL THEN 1 ELSE MAX(batch_sequence) + 1 END FROM {CommonVariables.REF_LOG_TABLE_IDN} WHERE process_id = {Placeholder.PROCESS_ID.value} AND batch_date = '{Placeholder.BATCH_DATE.value}'),
            'INPROGRESS', CURRENT_TIMESTAMP()
        );
    """

    REF_LOG_UPDATE_STATEMENT = f"""
        UPDATE {CommonVariables.REF_LOG_TABLE_IDN}
            SET
                end_timestamp = CURRENT_TIMESTAMP(),
                time_taken = CURRENT_TIMESTAMP() - start_timestamp,
                status = "{Placeholder.LOG_STATUS.value}",
                error_message = "{Placeholder.LOG_ERROR_MSG.value}"
        WHERE
            process_id = {Placeholder.PROCESS_ID.value} AND
            batch_sequence = (
                SELECT MAX(batch_sequence) FROM {CommonVariables.REF_LOG_TABLE_IDN}
                WHERE process_id = {Placeholder.PROCESS_ID.value} AND batch_date = '{Placeholder.BATCH_DATE.value}'
            );
    """