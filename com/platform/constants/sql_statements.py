from com.platform.constants.placeholders import Placeholder
from com.platform.constants.common_variables import CommonVariables


class SqlStatements:

    """Immutable module which holds all platform bigquery sql statements (only getter enabled)"""

    # Restrict new variable creation and modification
    def __setattr__(self, name, value):
        raise AttributeError(f"Cannot create or set class or instance attribute '{name}'")


    # Statements
    REF_SELECT_STATEMENT = f"SELECT * FROM {CommonVariables.REF_TABLE_IDN} WHERE id = {Placeholder.PROCESS_ID.value} ORDER BY last_modified_utc DESC LIMIT 1;"