from datetime import datetime

class StaticVariables:

    """Module which holds common static variables (only getter enabled)"""

    __RUNTIME: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    __LOG_FILE_NAME_PLACEHOLDER: str = r"{}_PLATFORM_{}.log"


    @staticmethod
    def get_class_fields():

        return {
            str(attr).replace("_StaticVariables__", ""): getattr(StaticVariables, attr)
                for attr in dir(StaticVariables)
                    if not callable(getattr(StaticVariables, attr)) and not attr.startswith("__")
        }
