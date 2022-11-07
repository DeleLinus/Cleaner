# import necessary modules
import json
import re
import pandas as pd
import numpy as np


def parse_and_extract(file_path):
    """
    gets and reads the raw data

    Parameters
    ----------
    file_path : str
        the file to be read

    Returns
    -------
    json_data : list
         array of paths to all json file present
         in the specified folder path
    """
    # read-in the file
    with open(file_path) as f:
        json_data = json.load(f)

    return json_data


def review_tokenizer(json_object):
    """
    splits junks of reviews details into their separate
    entities

    Parameters
    ----------
    json_object : dict
        key:value pair with review entities as values

    Returns
    -------
    review_date_author_list : list
        list of each review entity/review tokens
    """

    review_date_author_list = []  # holds individual review entity
    base_split_pattern = r"Verified\sPurchase"

    for _, val in json_object.items():
        for val_element in val:
            # extract each reviews with their date and author
            each_review = re.split(base_split_pattern, val_element)

            if len(each_review) > 1 and each_review[-1] == "":
                # avoid the invalid empty str at the -1 index
                each_review = each_review[:-1]
                review_date_author_list += each_review
            else:
                review_date_author_list += each_review

    return review_date_author_list


def extract_date_review(tokens):
    """
    - extract date and post
    - create dataframe
    - store data


    Parameters
    ----------
    tokens : list
        list of each review entity/review tokens

    Returns
    -------
    df : pandas.DataFrame
        dataframe with dates and posts as columns
    """
    post_gen_list = []  # holds the posts
    dates_gen_list = []  # holds the date corresponding to each post

    date_pattern = r'\d{2}[/-]\d{2}[/-]\d{4}'

    for review_descr in tokens:
        date_values = re.findall(date_pattern, review_descr)
        post_values = re.split(date_pattern, review_descr)

        # check whether a date is found
        if len(date_values) == 0:
            date_values = [np.nan]
        dates_gen_list += date_values
        post_gen_list.append(post_values[0])

    df = pd.DataFrame({"dates": dates_gen_list, "posts": post_gen_list})

    # store the data
    df.to_csv("transformed_output_data.csv", index=False)
    return df


if __name__ == "__main__":
    file_name = 'jumia_search_output.txt'
    post_and_dates_list = review_tokenizer(parse_and_extract(file_name))
    df = extract_date_review(post_and_dates_list)

    print(df)
