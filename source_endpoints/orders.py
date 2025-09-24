from authenticate import get_square_client
from benedict import benedict
from pathlib import Path
from loguru import logger

from square.core.api_error import ApiError
import pandas as pd
import pendulum
import copy
import sqlalchemy


import math


def schema(df: pd.DataFrame):
    dtype_mapping = {
        "object": sqlalchemy.String,
        "int64": sqlalchemy.Integer,
        "float64": sqlalchemy.Float,
        "bool": sqlalchemy.Boolean,
        "datetime64[ns]": sqlalchemy.DateTime,
    }

    schema_dict = {}
    for column in df.columns:
        print(f"Column: {column}, DataType: {type(column)}")
        col_type = str(df[column].dtype)
        if col_type in "dtype_mapping":
            schema_dict[column] = dtype_mapping[col_type]
        else:
            schema_dict[column] = (
                sqlalchemy.String
            )  # Default to String for unknown types

    return schema_dict


def get_data(config: benedict):
    print("IN FUNC")
    # df = pd.DataFrame()
    client = get_square_client()
    engine = sqlalchemy.create_engine(
        "postgresql://postgres:password@localhost:5432/postgres"
    )

    try:
        # while start_at < pendulum.now():
        data = []
        response = client.orders.search(**config)
        for order in response.orders:
            data.append(order.model_dump())
        df = pd.json_normalize(data, max_level=3)

        schema_dict = schema(df)
        # print(f"Column: {cols}, DataType: {type(cols)}")
        # df = pd.concat([df, tmp])
        # print(tmp)
        print(schema_dict)
        # print(df)
        df.to_sql(
            name="orders",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            dtype=schema_dict,
        )

        # tmp = None
        # config.query["filter"].date_time_filter.created_at.start_at = df[
        #     "created_at"
        # ].max()
        # start_at = pendulum.parse(df["created_at"].max())
    except ApiError as e:
        for error in e.errors:
            logger.error(f"Error: {error.category} - {error.code} - {error.detail}")

    return df


if __name__ == "__main__":
    path = Path(__file__).parent / "config" / "orders.yml"

    config = benedict.from_yaml(path)

    logger.info(
        f"Ingesting Data from {config.pop('name')} API \n for information see API documentation at: {config.pop('api_url')}"
    )

    config.query[
        "filter"
    ].date_time_filter.created_at.end_at = pendulum.now().to_rfc3339_string()
    start_at = pendulum.parse(
        config.query["filter"].date_time_filter.created_at.start_at
    )
    config_list = []

    for i in range((pendulum.now() - start_at).days):
        for hours_offset in [0, 12]:  # Start of day and halfway through
            updated_value = start_at.add(days=i, hours=hours_offset).to_rfc3339_string()

            config_copy = copy.deepcopy(config)
            config_copy.query[
                "filter"
            ].date_time_filter.created_at.start_at = updated_value
            config_list.append(config_copy)

    buckets_no = 28
    items_per_bucket = math.ceil(len(config_list) / buckets_no)

    # print("ims : ",items_per_bucket)

    buckets = []
    for i in range(buckets_no):
        buckets.append(config_list[items_per_bucket * i : items_per_bucket * (i + 1)])

    for bucket in buckets:
        for config in bucket:
            get_data(config)
        # with Pool(len(bucket)) as p:
        # print(p.map(get_data, bucket))
