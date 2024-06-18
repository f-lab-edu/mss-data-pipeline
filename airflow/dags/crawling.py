from crawler.load_to_s3 import load_to_s3
from etl.goods_info import process_goods_info
from etl.goods_review import process_goods_review

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG
from airflow.utils.dates import days_ago

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

default_args = {"retries": 1}

with DAG(
    "crawling_dag",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args=default_args,
    description="DAG tutorial",
    schedule_interval="0 15 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["crawling"],
) as dag:
    dag.doc_md = __doc__

    def crawl_html():
        # load_to_s3()
        pass

    def process_goods_info_(**kwargs):
        date = kwargs["execution_date"]
        print(date)
        process_goods_info(date)

    def process_goods_review_(**kwargs):
        date = kwargs["execution_date"]
        print(date)
        process_goods_review(date)

    crawl_task = PythonOperator(
        task_id="crawl_raw_html", python_callable=crawl_html, provide_context=True
    )

    info_process_task = PythonOperator(
        task_id="process_goods_info_html",
        python_callable=process_goods_info_,
        provide_context=True,
    )

    review_process_task = PythonOperator(
        task_id="process_goods_review_html",
        python_callable=process_goods_review_,
        provide_context=True,
    )

    crawl_task >> [info_process_task, review_process_task]
