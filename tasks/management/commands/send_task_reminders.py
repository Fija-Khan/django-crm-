from django.core.management.base import BaseCommand
from django.utils import timezone

from tasks.models import Task


class Command(BaseCommand):
    help = "Show reminders for pending tasks due today"

    def handle(self, *args, **options):

        today = timezone.localdate()

        tasks = Task.objects.filter(
            due_date=today
        ).exclude(
            status="done"
        )

        if not tasks.exists():
            self.stdout.write(
                self.style.SUCCESS(
                    "No pending tasks due today."
                )
            )
            return

        self.stdout.write(
            self.style.WARNING(
                f"Found {tasks.count()} task(s) due today:"
            )
        )

        for task in tasks:
            self.stdout.write(
                f"- {task.title} | "
                f"Assigned to: {task.assigned_to} | "
                f"Priority: {task.get_priority_display()} | "
                f"Status: {task.get_status_display()}"
            )