# todo: build a financial data collection every 5 mins,
# output should be a dataframe with last days financial info
import logging
from os import path
from run_api import get_base_file_path


def read_list_of_companies():
    companies_list = []
    file_path = path.join(get_base_file_path(),
                          'test_scripts/scheduled_tasks/tracked_companies.txt')
    with open(file_path, 'r') as f:
        companies_list = [co.replace('\n', '') for co in list(f.readlines())]
    return companies_list


def run_collection():
    for company in read_list_of_companies():
        print(company)

        break


if __name__ == "__main__":
    run_collection()
