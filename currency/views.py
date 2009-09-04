from annoying.decorators import render_to
from is_shared import is_shared

from django.db.models import Q

from plane.models import Plane
from currency.currbox import CurrBox

@render_to('currency.html')
def currency(request, username):
    shared, display_user = is_shared(request, username)
    
    from FAA import FAA_Currency
    
    currency = FAA_Currency(display_user)
    
    type_ratings = Plane.objects.filter(user=display_user).filter( Q(tags__icontains="type rating") | Q(tags__icontains="landing currency")).values_list('type', flat=True).order_by().distinct()
    cat_classes = Plane.objects.filter(user=display_user).values_list('cat_class', flat=True).order_by().distinct()
    tailwheels = Plane.objects.filter(user=display_user).filter( Q(tags__icontains="tailwheel")).values_list('cat_class', flat=True).order_by().distinct()
    
    
    medi_currbox = CurrBox(method="medical")
    medi_currbox.first = currency.first_class()
    medi_currbox.second = currency.second_class()
    medi_currbox.third = currency.third_class()
    medi_currbox.medi_issued = currency.medical_class
    
    #medi_currbox.render()
    
    cat_classes_out = []
    for item in cat_classes:
        currbox = CurrBox(cat_class=item, method="landings")
        
        currbox.day = currency.landing(night=False, cat_class=item)
        currbox.night = currency.landing(night=True, cat_class=item)
        
        cat_classes_out.append(currbox)
     
    tailwheels_out = []   
    for item in tailwheels:
        currbox = CurrBox(cat_class=item, method="landings", tail=True)
        
        currbox.day = currency.landing(night=False, cat_class=item, tail=True)
        currbox.night = currency.landing(night=True, cat_class=item, tail=True)
        
        tailwheels_out.append(currbox)
    
    types_out = []
    for item in type_ratings:
        currbox = CurrBox(tr=item, method="landings")
        
        currbox.day = currency.landing(night=False, tr=item)
        currbox.night = currency.landing(night=True, tr=item)
        
        types_out.append(currbox)
        
    
    
    #assert False
    #import pdb; pdb.set_trace()
    
    return locals()
