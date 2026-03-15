import json
from django.core.management.base import BaseCommand
from stations.models import Station
from django.conf import settings
import os


class Command(BaseCommand):

    help = "Import stations from JSON file"

    def handle(self, *args, **kwargs):

        # Check if stations already exist
        if Station.objects.exists():
            self.stdout.write(self.style.WARNING("Stations already imported"))
            return

        file_path = os.path.join(
            settings.BASE_DIR,
            "stations",
            "data",
            "stations.json"
        )

        with open("stations.json", "r", encoding="utf-8") as file:
            data = json.load(file)["stations"]

        stations = []

        for item in data:

            stations.append(
                Station(
                    stnCode=item["stnCode"],
                    stnName=item["stnName"],
                    stnCity=item["stnCity"]
                )
            )

        Station.objects.bulk_create(
            stations,
            batch_size=1000,
            ignore_conflicts=True
        )

        self.stdout.write(self.style.SUCCESS("Stations imported successfully"))
        