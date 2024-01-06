from google.api_core.exceptions import GoogleAPIError

def main_execution():

    logger.title("Reference execution")
    
    reference_query = "SELECT * FROM {} WHERE id={};".format(static_variables.REFERENCE_TABLE, parse_args.process_id)
    reference_query_result: list = bigquery.select_query(reference_query)
    
    if len(reference_query_result) < 1:
        raise GoogleAPIError("There is no ID: {} found under the reference table `{}`, please check.".format(parse_args.process_id, static_variables.REFERENCE_TABLE))
    
    for each in reference_query_result:
        print(each)