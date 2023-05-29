import sys, os
import pandas as pd
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Aspire.settings')

import django

django.setup()

from admin_panel.models import Tag


def save_tag_from_row(tag_row):
    tag = Tag()
    tag.name = tag_row[0]

    tag.save()
    print("Added a tag with id", tag_row[0])


if __name__ == "__main__":
    META_DATA_DICT = [
        {
            "file_location":"initial_data/tags.csv",
            "model": Tag,
            "model_name": "Tag",
            "function": save_tag_from_row
        },
    ]

    for model in META_DATA_DICT:
        try:
            print(f"Adding initial data for {model.get('model_name')}")
            df = pd.read_csv(model.get("file_location"))
            print(df)
            df = df.apply(lambda x: model.get('function')(x), axis=1)
        except FileNotFoundError:
            print("File not found")