from django.db.models import Sum
from constants import AGG_FIELDS, EXTRA_AGG
from utils import to_minutes

def total_column(queryset, columns, format='decimal'):
    ret = []
    agg_columns = []   
    for cn in columns:
    
        if cn in AGG_FIELDS:
            total = queryset.aggregate(Sum(cn)).values()[0]
            
        elif cn in EXTRA_AGG:
            if cn == 'complex':
                total = queryset.filter(plane__tags__icontains='complex').aggregate(Sum('total')).values()[0]
                
            elif cn == 'hp':
                total = queryset.filter(plane__tags__icontains='high performance').aggregate(Sum('total')).values()[0]
    
            elif cn == 'turbine':
                total = queryset.filter(plane__tags__icontains='turbine').aggregate(Sum('total')).values()[0]
    
            elif cn == 't_pic':
                total = queryset.filter(plane__tags__icontains='turbine').aggregate(Sum('pic')).values()[0]
            
            elif cn == 'mt':
                total = queryset.filter(plane__tags__icontains='turbine').aggregate(Sum('total')).values()[0]
                
            elif cn == 'mt_pic':
                total = queryset.filter(plane__tags__icontains='turbine', plane__cat_class__in=[2,4]).aggregate(Sum('pic')).values()[0]
                
            elif cn == 'm_pic':
                total = queryset.filter(plane__cat_class__in=[2,4]).aggregate(Sum('pic')).values()[0]
            
            elif cn == 'multi':
                total = queryset.filter(plane__cat_class__in=[2,4]).aggregate(Sum('total')).values()[0]
            
            elif cn == 'sea':
                total = queryset.filter(plane__cat_class__in=[3,4]).aggregate(Sum('total')).values()[0]
                
            elif cn == 'sea_pic':
                total = queryset.filter(plane__cat_class__in=[3,4]).aggregate(Sum('pic')).values()[0]
                
            elif cn == 'mes':
                total = queryset.filter(plane__cat_class=4).aggregate(Sum('total')).values()[0]
            
            elif cn == 'mes_pic':
                total = queryset.filter(plane__cat_class=4).aggregate(Sum('pic')).values()[0]
                   
            elif cn == 'p2p':
                total = queryset.filter(route__p2p=True).aggregate(Sum('total')).values()[0]
                
            else:
                total = 99.9
                
        if cn in AGG_FIELDS or cn in EXTRA_AGG:
            agg_columns.append(cn)
            if not total:
                total = 0
                
            if cn in ['night_l','day_l','app']:
                ret.append(str(total))
            else:
                if format == "decimal":
                    ret.append( "%.1f" % total )
                else:
                    ret.append( to_minutes(total) )
                    
    return (ret, agg_columns)