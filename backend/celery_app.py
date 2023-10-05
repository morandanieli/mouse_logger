import os

from celery import Celery
import plot_mouse

# Initialize Celery
celery = Celery(
    'worker',
    broker='redis://redis:6379',
    backend='redis://redis:6379'
)


@celery.task()
def func1(session_id, output_filename, db_name):
    plot_mouse.generate_image_request(session_id, output_filename, db_name)
    return os.path.basename(output_filename)