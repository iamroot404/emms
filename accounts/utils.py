from django.db.models import Q
from . models import Account
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
 

def paginateStaff(request, staff, results):
    page = request.GET.get('page')
    paginator = Paginator(staff, results)

    try:
        staff = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        staff = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        staff = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)


    return custom_range, staff

def searchStaff(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

  

    staff = Account.objects.distinct().filter(
        Q(staff_number__icontains=search_query) | 
        Q(first_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone_number__icontains=search_query)
    ).exclude(is_superadmin=True)


    return staff, search_query