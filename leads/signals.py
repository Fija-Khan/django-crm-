from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Lead, LeadActivity


@receiver(pre_save, sender=Lead)
def log_lead_status_change(sender, instance, **kwargs):
    if instance.pk:
        old = Lead.objects.get(pk=instance.pk)
        if old.status != instance.status:
            LeadActivity.objects.create(
                lead=instance,
                old_status=old.status,
                new_status=instance.status,
                changed_by=instance.assigned_to
            )



