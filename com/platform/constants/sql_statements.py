from com.platform.constants.placeholders import Placeholder
from com.platform.constants.common_variables import CommonVariables
from com.platform.constants.table_schema import LogStatus


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

    CHK_SELECT_STATEMENT = f"""
        SELECT * FROM {CommonVariables.CHK_TABLE_IDN}
        WHERE
            process_id = {Placeholder.PROCESS_ID.value} AND
            checkpoint_sequence >= {Placeholder.START_SEQUENCE.value} AND
            {Placeholder.END_SEQUENCE.value}
            is_active
        ORDER BY checkpoint_sequence ASC;        
    """

    REF_LOG_INSERT_STATEMENT = f"""
        INSERT INTO {CommonVariables.REF_LOG_TABLE_IDN} (batch_id, process_id, batch_date, batch_sequence, status, start_timestamp)
        VALUES (
            (SELECT CASE WHEN MAX(batch_id) IS NULL THEN 1 ELSE MAX(batch_id) + 1 END FROM {CommonVariables.REF_LOG_TABLE_IDN}),
            {Placeholder.PROCESS_ID.value},
            CURRENT_DATE(),
            (SELECT CASE WHEN MAX(batch_sequence) IS NULL THEN 1 ELSE MAX(batch_sequence) + 1 END FROM {CommonVariables.REF_LOG_TABLE_IDN} WHERE process_id = {Placeholder.PROCESS_ID.value} AND batch_date = '{Placeholder.BATCH_DATE.value}'),
            '{LogStatus.PROGRESS.value}',
            CURRENT_TIMESTAMP()
        );
    """

    REF_LOG_UPDATE_STATEMENT = f"""
        UPDATE {CommonVariables.REF_LOG_TABLE_IDN}
            SET
                end_timestamp = CURRENT_TIMESTAMP(),
                time_taken = CURRENT_TIMESTAMP() - start_timestamp,
                status = "{Placeholder.LOG_STATUS.value}",
                error_message = {Placeholder.LOG_MSG.value}
        WHERE
            process_id = {Placeholder.PROCESS_ID.value} AND
            batch_sequence = (
                SELECT MAX(batch_sequence) FROM {CommonVariables.REF_LOG_TABLE_IDN}
                WHERE process_id = {Placeholder.PROCESS_ID.value} AND batch_date = '{Placeholder.BATCH_DATE.value}'
            );
    """


    CHK_LOG_INSERT_STATEMENT = f"""
        INSERT INTO {CommonVariables.CHK_LOG_TABLE_IDN} (batch_id, process_id, batch_date, batch_sequence, checkpoint_sequence, status, start_timestamp)
        VALUES (
            (SELECT MAX(batch_id) FROM {CommonVariables.REF_LOG_TABLE_IDN} WHERE process_id = {Placeholder.PROCESS_ID.value}),
            {Placeholder.PROCESS_ID.value},
            CURRENT_DATE(),
            (SELECT MAX(batch_sequence) FROM {CommonVariables.REF_LOG_TABLE_IDN} WHERE process_id = {Placeholder.PROCESS_ID.value} AND batch_date = '{Placeholder.BATCH_DATE.value}'),
            {Placeholder.CHK_SEQUENCE_NO.value},
            '{LogStatus.PROGRESS.value}',
            CURRENT_TIMESTAMP()
        );
    """


    CHK_LOG_UPDATE_STATEMENT = f"""
        UPDATE {CommonVariables.CHK_LOG_TABLE_IDN}
            SET
                end_timestamp = CURRENT_TIMESTAMP(),
                time_taken = CURRENT_TIMESTAMP() - start_timestamp,
                status = "{Placeholder.LOG_STATUS.value}",
                log_message = {Placeholder.LOG_MSG.value}
        WHERE
            batch_id = (
                SELECT MAX(batch_id) FROM {CommonVariables.REF_LOG_TABLE_IDN}
                WHERE process_id = {Placeholder.PROCESS_ID.value}
            ) AND
            checkpoint_sequence = {Placeholder.CHK_SEQUENCE_NO.value};
    """