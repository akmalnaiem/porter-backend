import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from trains.models import Train



BATCH_SIZE = 6000


class Command(BaseCommand):
    help = 'Import trains from trains.json file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            required=True,
            help='Path to trains.json file'
        )

    
    def handle(self, *args, **options):
        file_path = options['path']
        json_path = Path(file_path)

        if not json_path.exists():
            raise CommandError(f"File not found: {file_path}")
        
        self.stdout.write(self.style.WARNING('Strating Train import...'))

        # ---------------- Load JSON ----------------

        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                payload = json.load(file)

        except json.JSONDecodeError:
            raise CommandError("Invalid JSON file format")
        
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")
        
        # ---------------- Validate API response ----------------

        if not payload.get('success', True):
            raise CommandError("Data source returned success=False")
        
        data = payload.get('data', [])
        if not data:
            raise CommandError("Train data not found")
        
        # ---------------- Import logic ----------------

        batch = []
        total_create = 0
        skipped = 0

        for item in data:

            #basic validation
            if not isinstance(item, list) or len(item) < 2:
                skipped +=1
                continue

            train_number = str(item[0]).strip()
            train_name = str(item[1]).strip()

            if not train_number or not train_name:
                skipped +=1
                continue

            batch.append(
                Train(
                    train_number=train_number,
                    train_name=train_name
                )
            )

            #batch insert
            if len(batch) >= BATCH_SIZE:
                with transaction.atomic():
                    Train.objects.bulk_create(
                        batch,
                        ignore_conflicts=True
                    )

                total_create += len(batch)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Inserted {total_create} trains...'
                    )
                )
                batch = []
        
        # final batch insert
        if batch:
            with transaction.atomic():
                Train.objects.bulk_create(
                    batch,
                    ignore_conflicts=True
                )
            
            total_create += len(batch)

        self.stdout.write(
            self.style.SUCCESS(
                f"""
                    Import completed successfully 🎉
                    Total inserted : {total_create}
                    Total skipped  : {skipped}
                """
            )
        ) 