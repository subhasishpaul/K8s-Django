from django.db.models import Q
from functools import reduce
from ..models import Mobile
import datetime

def filter_mobiles(mobiles, paramDict):
    # paramDict = request.GET
    params = paramDict.keys()
    print("paramDict.keys()", params)

    # data filtering
    if any(x!='' for x in paramDict.values()):
        
        if paramDict['circle_id'] != '':
            circle_id = paramDict['circle_id']
            # data = Q(msisdn__icontains=circle_id)
            print("CIRCLE:",circle_id)

            mobiles = mobiles.filter(circle_id=circle_id) 

        # if paramDict['upc_date'] != '':
        #     upc_date = paramDict['upc_date']
        #     _upc_date = datetime.datetime.strptime(upc_date, '%m/%d/%Y')
        #     print("UPC DATE:",_upc_date)

        #     mobiles = mobiles.filter(upc_date__gte=_upc_date)        

        # filters records that contain any of the following keywords
        # if paramDict['keywords'] != '':
        #     kws = paramDict['keywords'].split()
        #     print(kws)
        #     q_lookups = [Q(msisdn__icontains=kw) for kw in kws] + \
        #                 [Q(name__icontains=kw) for kw in kws]
        #     filters = Q()
        #     filters |= reduce(lambda x, y: x | y, q_lookups)
        #     print("FILTERS:", filters)
        #     mobiles = mobiles.filter(filters)

    return mobiles


    def filter_mobiles_upc(mobiles, paramDict):
    # paramDict = request.GET
        params = paramDict.keys()
        print("paramDict.keys()", params)

        # data filtering
        if any(x!='' for x in paramDict.values()):
            
        
            if paramDict['upc_date'] != '':
                upc_date = paramDict['upc_date']
                _upc_date = datetime.datetime.strptime(upc_date, '%m/%d/%Y')
                print("UPC DATE:",_upc_date)

                mobiles = mobiles.filter(upc_date__gte=_upc_date)        

            # filters records that contain any of the following keywords
            # if paramDict['keywords'] != '':
            #     kws = paramDict['keywords'].split()
            #     print(kws)
            #     q_lookups = [Q(msisdn__icontains=kw) for kw in kws] + \
            #                 [Q(name__icontains=kw) for kw in kws]
            #     filters = Q()
            #     filters |= reduce(lambda x, y: x | y, q_lookups)
            #     print("FILTERS:", filters)
            #     mobiles = mobiles.filter(filters)

        return mobiles