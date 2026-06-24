from django.shortcuts import render
from leads.models import Lead
from contacts.models import Contact
from deals.models import Deal

def dashboard_view(request):
    context = {
        'total_leads': Lead.objects.count(),
        'total_contacts': Contact.objects.count(),
        'total_deals': Deal.objects.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)