#
# FILENAME.
#       cnt_notion.py - Count Notion Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides functions to access Notion.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2025/9/3
#       Updated on 2025/9/3
#

from notion_client import Client

br = breakpoint

# Query the database
# The response is paginated, so we need to loop through all pages
# https://pypi.org/project/notion-client/


def query(notion, db_id):
    results = []
    has_more = True
    start_cursor = None

    db = notion.databases.retrieve(
        database_id=db_id, start_cursor=start_cursor, page_size=100
    )
    data_source_id = db["data_sources"][0]["id"]

    while has_more:
        response = notion.data_sources.query(
            data_source_id=data_source_id, start_cursor=start_cursor, page_size=100
        )
        results.extend(response["results"])
        has_more = response["has_more"]
        start_cursor = response.get("next_cursor")

    return results
