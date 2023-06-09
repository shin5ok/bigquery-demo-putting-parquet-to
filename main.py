import pyarrow.parquet as pq
import numpy as np
import pyarrow as pa
import pandas as pd
import pyarrow
import json
import sys, os
import click
from datetime import datetime as dt
from google.cloud import bigquery
import re
import gendata

debug = 'DEBUG' in os.environ

@click.group()
def cli() -> None:
    pass

@cli.command()
@click.option("--file", "-f")
@click.option("--number", "-n", default=10)
@click.option("--json_path", "-j")
def generate(file, number, json_path):
    if not file:
        file = dt.now().strftime("%Y%m%dT%H%M%S") + ".parquet"
    record = gendata.get(number, json_path)
    df = pd.read_json(record, orient ='index')
    print(df)
    dprint(df.to_json())
    df.to_parquet(file)
    print()
    print(file, "has been generated.")

@cli.command()
@click.option("--table_id", "-t", required=True)
@click.option("--file", "-f", required=True)
def put(file, table_id):
    client = bigquery.Client()

    # schema = [
    #     bigquery.SchemaField("id", "STRING"),
    #     bigquery.SchemaField("name", "STRING"),
    #     bigquery.SchemaField("update_at", "TIMESTAMP"),
    #     bigquery.SchemaField("attr", "RECORD", mode="NULLABLE", 
    #             fields= [
    #                bigquery.SchemaField("user_name", "STRING"),
    #                bigquery.SchemaField("email", "STRING"),
    #                bigquery.SchemaField("address", "STRING"),
    #             ]
    #         )
    # ]
    ## Manual specified schema
    # job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.PARQUET, schema=schema)

    # Auto generated schema
    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.PARQUET, autodetect=True)

    if re.match("^gs://", file):
        uri = file
        load_job = client.load_table_from_uri(
            uri, table_id, job_config=job_config
        )
        load_job.result()
    else:
        fp = open(file, mode="rb")
        load_job = client.load_table_from_file(
            fp, table_id, job_config=job_config
        )
        load_job.result()
    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))

def dprint(data):
    if debug:
        print(data)

if __name__ == '__main__':
    cli()
