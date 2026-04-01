from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Show columns from one or more database tables using Django database settings"

    def add_arguments(self, parser):
        parser.add_argument(
            "tables",
            nargs="*",
            help="List of table names. Example: python manage.py showcolumns garment auth_user"
        )

    def handle(self, *args, **options):
        input_tables = options["tables"]

        if not input_tables:
            self.stdout.write(self.style.WARNING("No table names provided."))
            self.stdout.write("Example:")
            self.stdout.write("  python manage.py showcolumns garment")
            self.stdout.write("  python manage.py showcolumns garment auth_user")
            return

        existing_tables = connection.introspection.table_names()

        with connection.cursor() as cursor:
            for table in input_tables:
                self.stdout.write(f"column {table}:")

                if table not in existing_tables:
                    self.stdout.write(self.style.ERROR(f"- Table '{table}' does not exist"))
                    self.stdout.write("")
                    continue

                try:
                    cursor.execute(f"SHOW COLUMNS FROM `{table}`")
                    columns = [row[0] for row in cursor.fetchall()]

                    for col in columns:
                        self.stdout.write(f"- {col}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"- Error: {e}"))

                self.stdout.write("")