from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.core.paginator import Paginator
# from django.conf import settings
from django.utils import timezone
from django.db.models import Q 
from datetime import datetime, timedelta
import csv
import json
from django.contrib import messages

from .forms import SsaForm, FeedbackModelForm, UserRegisterForm
from .models import Mobile, Circle, Ssa

import pandas as pd
import numpy as np
from .utils import get_plot, get_plot_upc
from django_pandas.io import read_frame

from django.contrib.auth.models import User


# Circle user creation
@login_required
@permission_required('is_superuser')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('user_details')
    else:
        form = UserRegisterForm()
        return render(request, 'feedbacks/register.html', {'form': form})


# registered user details
class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    # template_name = 'feedbacks/user_list.html'
    # paginate_by = 20


class SearchUserView(generic.ListView):
    model = User
    #template_name = 'feedbacks/mobile_list.html'

    def get_queryset(self):
        
        query = self.request.GET.get('usr')
        if len(query) == 0:          
            messages.warning(self.request, 'Please enter search string')
            return reverse('searchuser')
        else:
            object_list = User.objects.filter(
                Q(username__icontains = query) | Q(first_name__icontains = query) | Q(last_name__icontains = query) | Q(email__icontains = query)  
            )
        
            return object_list



# UPC REPORT

def SearchByCirclePlot(request):
    context = {}
    context['form'] = SearchForm({'report_type' : 'Chart'})
    if request.GET: 
        temp = request.GET['circle_id'] 
        # print(temp) 
    return render(request, 'feedbacks/sel_circle_plot.html', context)

def plot(request):

    cir_id = request.GET['circle_id'] 
    upc_start_dt = request.GET.get('d1')
    upc_end_dt = request.GET.get('d2')
    # converting string to datetime and adding 1 day
    upc_end_dt1 = datetime.strptime(upc_end_dt, "%Y-%m-%d") + timedelta(days=1)
    report_type = request.GET.get('report_type')
    
    Q3 = Q(upc_date__gte=upc_start_dt)
    Q2 = Q(upc_date__lte=upc_end_dt1)

    if int(cir_id) == 0:
        Q1 = Q(circle_id__in = [1,2,3,4,5,6,7,8,9])
    else:
        Q1 = Q(circle_id=cir_id)
    
    start_dt = datetime.strptime(upc_start_dt, "%Y-%m-%d")
    # print(start_dt.strftime("%d-%b-%Y"))
    start_dt = start_dt.strftime("%d-%b-%Y")
    end_dt = datetime.strptime(upc_end_dt, "%Y-%m-%d")
    end_dt = end_dt.strftime("%d-%b-%Y")
    
    if (int(cir_id) > 0):

        mob = Mobile.objects.filter(Q1 & Q2 & Q3)
        data = read_frame(mob)
        # print(data['ssa'])
        data2 = data.value_counts(['ssa']).reset_index(name='Total UPC generated')
        # print(data2)
        data2.rename(columns = {'ssa': 'SSA'}, inplace = True)
        qs = Circle.objects.filter(id=cir_id)
        for cir in qs:
            name1 = cir.name
        xlabel = "SSA Name"

    else:
        
        mob = Mobile.objects.filter(Q1 & Q2 & Q3) 
        data = read_frame(mob)
        # print(data.msisdn)
        data2 = data.value_counts(['circle']).reset_index(name='Total UPC generated')
        # print(data2)
        data2.rename(columns = {'circle': 'CIRCLE'}, inplace = True)
        name1 = "EZ circles"
        xlabel = "Circle Name"
    
    title = "Total UPC generated"
    ylabel = "UPC count"
    circle = []
    count = []

    for z in range(len(data2)):
        circle.append((data2.iloc[z,0]))
        count.append((data2.iloc[z,1]))
    
    if report_type == "Report":
        
        circnt = {}
        # circnt = {circle[i]: count[i] for i in range(len(circle))} 

        circnt = dict(zip(circle, count))
        # print(circnt)

        context = {
            # 'circle' : circle,
            'title' : title,
            'upc_start_dt' : start_dt,
            'upc_end_dt' : end_dt,
            'data' : circnt,
        }
        return render(request, 'feedbacks/report_upc.html', context)

    else:
        # print(data2)
        
        chart = get_plot_upc(data2, name1, start_dt, end_dt, title, xlabel, ylabel)
        
        sum = 0
        for i in range(len(count)):
            sum += count[i]
        if sum > 0:
            # x = [x.ssa for x in qs]
            context = {
                # 'df' : data1.to_html(),
                'chart' : chart,
                'upc_start_dt' : start_dt,
                'upc_end_dt' : end_dt,
            }
        else:
            context = {
                'chart' : None,
                'upc_start_dt' : start_dt,
                'upc_end_dt' : end_dt,
            }
        return render(request, 'feedbacks/chart.html', context)


# Feedback report

def SearchByCircleFeedPlot(request):
    context = {}
    context['form'] = SearchForm({
        'feed_status' : 'Completed', 
        'report_type' : 'Chart',
        'po_reason' : 'No'
        })
    return render(request, 'feedbacks/plot_feed.html', context)


def feedplot(request):
    cir_id = request.GET['circle_id'] 
    upc_start_dt = request.GET.get('d1')
    upc_end_dt = request.GET.get('d2')
    feed_status = request.GET.get('feed_status')
    report_type = request.GET.get('report_type')
    po_reason = request.GET.get('po_reason')

    start_dt = datetime.strptime(upc_start_dt, "%Y-%m-%d")    # string to date conversion
    # print(start_dt.strftime("%d-%b-%Y"))
    start_dt = start_dt.strftime("%d-%b-%Y")    # format change
    end_dt = datetime.strptime(upc_end_dt, "%Y-%m-%d")
    end_dt = end_dt.strftime("%d-%b-%Y")

    reasons = ['Billing issues', 'Value Added Services', 'Poor network coverage', 'High tariff', 'Low data speed', \
            'Absence of 4G', 'Poor customer care', 'Recharge issues', 'Others']

    
        
    if feed_status == 'Pending':                
        Q4 = (Q(feedback_date__isnull = True) |  Q(reason_for_PO__exact = '') |  Q(reason_for_PO__startswith = 'Not Answered'))
    
    else:        
        Q4 = (Q(feedback_date__isnull = False) & Q(reason_for_PO__in = reasons))

    upc_end_dt1 = datetime.strptime(upc_end_dt, "%Y-%m-%d") + timedelta(days=1)
    Q3 = Q(upc_date__gte=upc_start_dt)
    Q2 = Q(upc_date__lte=upc_end_dt1) 

    if int(cir_id) == 0:
        Q1 = Q(circle_id__in = [1,2,3,4,5,6,7,8,9])
    else:
        Q1 = Q(circle_id=cir_id)

    # print("Entered data: ", cir_id, po_reason, feed_status)

    if feed_status == 'Completed':
        title = "Customer Feedback completed"
        ylabel = "Feedback taken"
        xlabel = "SSA Name"
        
    else:
        title = "Customer Feedback pending"
        ylabel = "Feedback pending"
        xlabel = "SSA Name"
        
    
    if int(cir_id) == 0:
        xlabel= "Circle Name"
        name1 = "EZ circles"
    else:
        xlabel= "SSA name"
        qs = Circle.objects.filter(id=cir_id)
        for cir in qs:
            name1 = cir.name
    total = 0

    if int(cir_id) > 0 and feed_status == 'Completed' and po_reason=="Yes":        
           
        mob = Mobile.objects.filter(Q1 & Q2 & Q3 & Q4)
        data = read_frame(mob)
        # print(data)
        data2 = data.value_counts(['ssa','reason_for_PO']).reset_index(name='feedback')
        data2.rename(columns = {'ssa': 'SSA'}, inplace = True)
        total = data2.shape[0]
        
    elif (int(cir_id) > 0 and feed_status == 'Completed' and po_reason=="No") or \
        (int(cir_id) > 0 and feed_status == 'Pending'):

        mob = Mobile.objects.filter(Q1 & Q2 & Q3 & Q4)
        data = read_frame(mob)
        data2 = data.value_counts(['ssa']).reset_index(name='feedback')
        data2.rename(columns = {'ssa': 'SSA'}, inplace = True)
        data_dict = json.loads(data['ssa'].value_counts().to_json())
        total = len(data_dict)
        # print("Rows: ", total)
    
    elif (int(cir_id) == 0) and po_reason=="Yes" and feed_status == 'Completed':
        mob = Mobile.objects.filter(Q1 & Q2 & Q3 & Q4) 
        data = read_frame(mob)
        data2 = data.value_counts(['circle','reason_for_PO']).reset_index(name='feedback')
        data2.rename(columns = {'circle': 'CIRCLE'}, inplace = True)
        total = data2.shape[0]
        
    elif (int(cir_id) == 0) and (feed_status == 'Completed' and po_reason=="No") or (feed_status == 'Pending'):
        
        mob = Mobile.objects.filter(Q1 & Q2 & Q3 & Q4) 
        data = read_frame(mob)
        data2 = data.value_counts(['circle']).reset_index(name='Count')
        data2.rename(columns = {'circle': 'CIRCLE'}, inplace = True)
        data_dict = json.loads(data['circle'].value_counts().to_json())
        total = len(data_dict)
        # print("PENDING")
    
    else:
        # print("Check combination")
        pass

    # circle = []
    # reason = []
    # count = []
    
    # p = ''    
    # count_po = [0,0,0,0]    
    # q = 0

    # if  po_reason=="Yes" and feed_status=='Completed':

    #     for z in range(len(data2)):
    #         circle.append((data2.iloc[z,0]))

    #         p = data2.iloc[z,1]
    #         q = int(data2.iloc[z,2])
            
    #         if p == 'Others':
    #             count_po[0] += q
    #         elif p == 'Bad network':
    #             count_po[1] += q
    #         elif p == 'High tariff':
    #             count_po[2] += q
    #         elif p == 'No 4G':
    #             count_po[3] += q
    #         else:
    #             pass
            
    #         reason.append(p)             
    #         count.append(q)
        
    #     for j in range(len(reasons)):
        
    #         listOfSeries = [pd.Series([name1, reasons[j], count_po[j]], index=data2.columns )]
    #         data2 = data2.append(listOfSeries , ignore_index=True)            
        
    # else:
    #     # for z in range(len(data2)):
    #     #     circle.append((data2.iloc[z,0]))
    #     #     count.append((data2.iloc[z,1]))

    #     # listOfSeries = [pd.Series([name1, len(data)], index=data2.columns )]
    #     # data2 = data2.append(listOfSeries , ignore_index=True)
    #     # print(data2)
    #     pass
        
    
    # df = data2
    data_chart = data2

    if total > 0:
        if report_type == "Report":
            if po_reason=="Yes" and feed_status == 'Completed':
                if (int(cir_id) == 0):            
                    df = pd.crosstab(data['circle'], data['reason_for_PO'], values=data['msisdn'], aggfunc='count' , margins=True, \
                        margins_name="Total", rownames=['CIRCLE'], colnames=['PO-REASON'])   #.sort_values('CIRCLE',ascending=False)
                    # df = df.drop('PO-REASON',axis=1)
                    df = df.replace(np.nan, 0)
                    df = df.astype(int)
                
                    # pd.crosstab(a, [b, c], rownames=['a'], colnames=['b', 'c']) 

                else:            
                    df = pd.crosstab(data['ssa'], data['reason_for_PO'], values=data['msisdn'], aggfunc='count' , margins=True, margins_name="Total", rownames=['SSA'], colnames=['Feedback reason'])
                    df = df.replace(np.nan, 0)
                    df = df.astype(int) 
                      

                # print(df)   
                context = {                    
                    'title' : title,
                    'start_dt' : start_dt,
                    'end_dt' : end_dt,
                    'data2' : df.to_html(classes=["blueTableRow", "blueTable", "isi"])
                }

                return render(request, 'feedbacks/feed_report_yes.html', context)

            if feed_status == 'Pending' or (feed_status == 'Completed' and po_reason=="No"):
                
                context = {
                    'title' : title,
                    'upc_start_dt' : start_dt,
                    'upc_end_dt' : end_dt,            
                    'data_dict':data_dict,
                    # 'data2' : data2
                }
                
                return render(request, 'feedbacks/feed_report_no.html', context) 
            
        else:
            # print(data_chart)        
            chart = get_plot(data_chart, name1, start_dt, end_dt, title, xlabel, ylabel)
            
            # print("Total rows = ", total)
            
            if total > 0:
                # x = [x.ssa for x in qs]
                context = {
                    # 'df' : data1.to_html(),
                    'chart' : chart,
                    'upc_start_dt' : upc_start_dt,
                    'upc_end_dt' : upc_end_dt,
                }
            else:
                context = {
                    'chart' : None
                }
            return render(request, 'feedbacks/chart.html', context)
    else:
        context = {
            'title' : title,
            'start_dt' : start_dt,
            'end_dt' : end_dt,
        }
        return render(request, 'feedbacks/no_data.html', context)


# HOME PAGE

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    mob_count = Mobile.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'mob_count': mob_count,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# Viewing all MSISDN

class MobileListView(LoginRequiredMixin, generic.ListView):
    model = Mobile
    # template_name = 'feedbacks/mobile_list1.html'
    paginate_by = 20


# Mobile Detail view for taking feedback
import sys

@login_required
def MobileDetailView(request, pk):

    mobile = get_object_or_404(Mobile, pk=pk)
    mobile.user = str(request.user)

    if mobile.reason_for_PO == '' or mobile.reason_for_PO == 'Not Answered':

        if request.method == 'POST':
            
            form = FeedbackModelForm(request.POST)
            if form.is_valid():
                mobile.remarks = form.cleaned_data.get('remarks')       
                reason_for_PO = form.cleaned_data.get('reason_for_PO')
                mobile.reason_for_PO = dict(form.fields['reason_for_PO'].choices)[reason_for_PO]
                # print(mobile.reason_for_PO)
                
                mobile.feedback_date = timezone.localtime(timezone.now())
                mobile.called_counter += 1
                mobile.save()
                # return HttpResponse('<script type="text/javascript">window.opener.location.reload();window.close();</script>')
                messages.success(request, "Please close this window. Feedback updated successfully." )   # added
                # return HttpResponseRedirect(reverse('mobiles'))    # commented on 12-dec-2020
            # messages.error(request, "Error. Message not sent.")
        else:
            form = FeedbackModelForm()  

        # a = mobile1.remarks
        
        # print("REASON", b)

        context = {
            'form' : form,
            'mobile' : mobile,
        }

        return render(request, 'feedbacks/mobile_detail.html', context)
    
    else:
        # print(mobile.remarks)
        fd = mobile.feedback_date
        context = {
            'fd' : fd,
            'mobile' : mobile,
        }
        return render(request, 'feedbacks/feedback_taken_already.html', context)

# Search By Circle

from .forms import SearchForm

@login_required
def SearchByCircle(request):
    context = {}
    context['form'] = SearchForm({
        'feed_sts' : 'feed_pend',
        'port_sts' : 'port_pend',
        })
    return render(request, 'feedbacks/sel_circle.html', context)


class SearchResultsView3(generic.ListView, LoginRequiredMixin):
    model = Mobile
    paginate_by = 20
    template_name = 'feedbacks/mobile_list.html'

    def get_queryset(self):
        circle_id = self.request.GET.get('circle_id') 
        start_upc = self.request.GET.get('d1')
        end_upc = self.request.GET.get('d2')
        feed_sts = self.request.GET.get('feed_sts')
        port_sts = self.request.GET.get('port_sts')
                
        reasons = ['Billing issues', 'Value Added Services', 'Poor network coverage', 'High Tariff', 'Low data speed', \
            'Absence of 4G', 'Poor customer care', 'Recharge issues', 'Others']

        Q1 = Q(circle_id=circle_id)
        Q2 = Q(upc_date__gte=start_upc)
        end_upc1 = datetime.strptime(end_upc, "%Y-%m-%d") + timedelta(days=1)
        Q3 = Q(upc_date__lte=end_upc1)

        
        if feed_sts == 'feed_comp':  
            Q4 = (Q(feedback_date__isnull = False) & Q(reason_for_PO__in = reasons))
        else:
            Q4 = (Q(feedback_date__isnull = True) |  Q(reason_for_PO__exact = '') |  Q(reason_for_PO__startswith = 'Not Answered'))

        if port_sts == 'all':
            Q5 = (Q(port_status__startswith = 'Applied for Portout') | Q(port_status__isnull = True) | Q(port_status__startswith = 'Portout Completed'))

        elif port_sts == 'port_pend':        
            Q5 = (Q(port_status__startswith = 'Applied for Portout') | Q(port_status__isnull = True))

        else:
            Q5 = Q(port_status__startswith = 'Portout Completed')       
        
        if int(circle_id) > 0:
            object_list = Mobile.objects.filter( Q1 & Q2 & Q3 & Q4 & Q5)
        else:
            object_list = Mobile.objects.filter( Q2 & Q3 & Q4 & Q5)    
        return object_list


def export_csv_circle_wise(request):
    
    response = HttpResponse(content_type='text/csv')
    file_name = "report_circlewise_" + str(datetime.today()) + ".csv"
    response['Content-Disposition'] = 'attachment; filename = "' + file_name + '"'

    writer = csv.writer(response)
    writer.writerow(['MSISDN', 'ACCOUNT_NO', 'NAME', 'ADDRESS', 'SSA', 'CIRCLE', 'UPC DATE', 'UPC_EXPIRY_DATE','CONNECTION_TYPE', 'AVERAGE REVENUE',
        'PO_APPLY_DATE', 'PO_DATE', 'PORT_STATUS', 'CALLED_COUNTER', 'REASON FOR PO', 'REMARKS', 'FEEDBACK DATE', 'USER'])
    
    circle_id = request.GET.get('circle_id') 
    start_upc = request.GET.get('d1')
    end_upc = request.GET.get('d2')
    feed_sts = request.GET.get('feed_sts')
    port_sts = request.GET.get('port_sts')
            
    reasons = ['Billing issues', 'Value Added Services', 'Poor network coverage', 'High Tariff', 'Low data speed', \
        'Absence of 4G', 'Poor customer care', 'Recharge issues', 'Others']

    Q1 = Q(circle_id=circle_id)
    Q2 = Q(upc_date__gte=start_upc)
    end_upc1 = datetime.strptime(end_upc, "%Y-%m-%d") + timedelta(days=1)
    Q3 = Q(upc_date__lte=end_upc1)
    
    if feed_sts == 'feed_comp':  
        Q4 = (Q(feedback_date__isnull = False) & Q(reason_for_PO__in = reasons))
    else:
        Q4 = (Q(feedback_date__isnull = True) |  Q(reason_for_PO__exact = '') |  Q(reason_for_PO__startswith = 'Not Answered'))

    if port_sts == 'all':
        Q5 = (Q(port_status__startswith = 'Applied for Portout') | Q(port_status__isnull = True) | Q(port_status__startswith = 'Portout Completed'))

    elif port_sts == 'port_pend':        
        Q5 = (Q(port_status__startswith = 'Applied for Portout') | Q(port_status__isnull = True))

    else:
        Q5 = Q(port_status__startswith = 'Portout Completed')       
    
    if int(circle_id) > 0:
        object_list = Mobile.objects.filter( Q1 & Q2 & Q3 & Q4 & Q5)
    else:
        object_list = Mobile.objects.filter( Q2 & Q3 & Q4 & Q5)    
    
    mobiles = object_list.values_list(
        'msisdn',
        'account_no',
        'name',
        'address',
        'ssa__name',
        'circle__name',
        'upc_date',
        'upc_expiry_date',
        'connection_type',
        'avg_revenue',
        'portout_apply_date',
        'portout_date',
        'port_status',
        'called_counter',
        'reason_for_PO',
        'remarks',
        'feedback_date',
        'user'
    )
    # print(len(mobiles))

    if (len(mobiles) > 0):
        for mobile in mobiles:
            writer.writerow(mobile)

        return response

    else:
        return HttpResponseRedirect(reverse('filter1'))

# Search by SSA

@login_required
def SearchBySsa(request):
    if request.method == 'GET':    # when form is opened first time
        # print("inside GET form")
        form = SsaForm({
            'feed_sts' : 'feed_pend',
            'port_sts' : 'port_pend'
        })
    else:
        # print("inside else form")   # Not used this part
        form = SsaForm()   
        
    context = {
        'form' : form,
    }
    return render(request, 'feedbacks/sel_ssa.html', context)


def load_ssas(request):
    circle_id = request.GET.get('circle_id')
    # print("inside load ssas", circle_id)
    ssas = Ssa.objects.filter(circle_id=circle_id).order_by('name')
    return render(request, 'feedbacks/branch_dropdown_list_options.html', {'ssas': ssas})


class SearchResultsView4(generic.ListView, LoginRequiredMixin):
    model = Mobile
    paginate_by = 20
    template_name = 'feedbacks/mobile_list.html'

    def get_queryset(self): 
        
        circle_id = self.request.GET.get('circle') 
        ssa_id = self.request.GET.get('ssa')
        start_upc = self.request.GET.get('d1')
        end_upc = self.request.GET.get('d2')
        feed_sts = self.request.GET.get('feed_sts')
        port_sts = self.request.GET.get('port_sts')

        reasons = ['Billing issues', 'Value Added Services', 'Poor network coverage', 'High tariff', 'Low data speed', \
            'Absence of 4G', 'Poor customer care', 'Recharge issues', 'Others']

        if feed_sts == 'feed_comp':  
            Q5 = (Q(feedback_date__isnull = False) & Q(reason_for_PO__in = reasons))
        else:
            Q5 = (Q(feedback_date__isnull = True) |  Q(reason_for_PO__exact = '') |  Q(reason_for_PO__startswith = 'Not Answered'))

        if port_sts == 'all':
            Q6 = (Q(port_status__startswith = 'Applied for Portout') | Q(port_status__isnull = True) | Q(port_status__startswith = 'Portout Completed'))

        elif port_sts == 'port_pend':        
            Q6 = (Q(port_status__startswith = 'Applied for Portout') | Q(port_status__isnull = True))

        else:
            Q6 = Q(port_status__startswith = 'Portout Completed')

        Q1 = Q(circle_id=circle_id)
        Q2 = Q(ssa_id=ssa_id)
        Q3 = Q(upc_date__gte=start_upc)
        end_upc1 = datetime.strptime(end_upc, "%Y-%m-%d") + timedelta(days=1)
        Q4 = Q(upc_date__lte=end_upc1)

        object_list = Mobile.objects.filter( Q1 & Q2 & Q3 & Q4 & Q5 & Q6)
        
        return object_list


def export_csv_ssa_wise(request):
    
    circle_id = request.GET.get('circle') 
    ssa_id = request.GET.get('ssa')
    
    start_upc = request.GET.get('d1')
    end_upc = request.GET.get('d2')
    feed_sts = request.GET.get('feed_sts')
    port_sts = request.GET.get('port_sts')
    
    response = HttpResponse(content_type='text/csv')
    file_name = "report_ssawise_" + str(datetime.today()) + ".csv"
    # file_name = str(circle_id) + "_" + str(ssa_id) + "_" + str(datetime.today()) + ".csv"
    response['Content-Disposition'] = 'attachment; filename = "' + file_name + '"'

    writer = csv.writer(response)
    writer.writerow(['MSISDN', 'ACCOUNT_NO', 'NAME', 'ADDRESS', 'SSA', 'CIRCLE', 'UPC DATE', 'UPC_EXPIRY_DATE','CONNECTION_TYPE', 'AVERAGE REVENUE',
        'PO_APPLY_DATE', 'PO_DATE', 'PORT_STATUS', 'CALLED_COUNTER', 'REASON FOR PO', 'REMARKS', 'FEEDBACK DATE', 'USER'])
         
    reasons = ['Billing issues', 'Value Added Services', 'Poor network coverage', 'High tariff', 'Low data speed', \
            'Absence of 4G', 'Poor customer care', 'Recharge issues', 'Others']

    if feed_sts == 'feed_comp':  
        Q5 = (Q(feedback_date__isnull = False) & Q(reason_for_PO__in = reasons))
    else:
        Q5 = (Q(feedback_date__isnull = True) |  Q(reason_for_PO__exact = '') |  Q(reason_for_PO__startswith = 'Not Answered'))

    if port_sts == 'all':
        Q6 = (Q(port_status__startswith = 'Applied for Portout') | Q(port_status__isnull = True) | Q(port_status__startswith = 'Portout Completed'))

    elif port_sts == 'port_pend':        
        Q6 = (Q(port_status__startswith = 'Applied for Portout') | Q(port_status__isnull = True))

    else:
        Q6 = Q(port_status__startswith = 'Portout Completed')

      
    Q1 = Q(circle_id=circle_id)
    Q2 = Q(ssa_id=ssa_id)
    Q3 = Q(upc_date__gte=start_upc)
    end_upc1 = datetime.strptime(end_upc, "%Y-%m-%d") + timedelta(days=1)
    Q4 = Q(upc_date__lte=end_upc1)

    object_list = Mobile.objects.filter( Q1 & Q2 & Q3 & Q4 & Q5 & Q6)

    # if selected == 'yes':
    #     object_list = Mobile.objects.filter( Q1 & Q2 & Q3 & Q4 & Q5 ) 
    # else:
    #     object_list = Mobile.objects.filter( Q1 & Q2 & Q3 & Q4 & Q5)
    
    mobiles = object_list.values_list(
        'msisdn',
        'account_no',
        'name',
        'address',
        'ssa__name',
        'circle__name',
        'upc_date',
        'upc_expiry_date',
        'connection_type',
        'avg_revenue',
        'portout_apply_date',
        'portout_date',
        'port_status',
        'called_counter',
        'reason_for_PO',
        'remarks',
        'feedback_date',
        'user'
    )
    # print(len(mobiles))

    if (len(mobiles) > 0):
        for mobile in mobiles:
            writer.writerow(mobile)

        return response

    else:
        return HttpResponseRedirect(reverse('filter1'))


# Single MSISDN search

class HomePageView2(LoginRequiredMixin, generic.TemplateView):
    template_name = 'feedbacks/sel_msisdn_upc.html'

class SearchResultsView2(generic.ListView):
    model = Mobile
    paginate_by = 30
    template_name = 'feedbacks/mobile_list.html'

    def get_queryset(self):
        
        query = self.request.GET.get('q')
        if len(query) != 10:          
            messages.warning(self.request, 'Please enter 10-digit MSISDN.')
            return reverse('searchsingle')
        else:
            object_list = Mobile.objects.filter(
                Q(msisdn__iexact=query)  
            )
        
            return object_list



# def export_csv_single(request):
    
#     response = HttpResponse(content_type='text/csv')
#     file_name = "feedback_data" + str(datetime.today()) + ".csv"
#     response['Content-Disposition'] = 'attachment; filename = "' + file_name + '"'

#     writer = csv.writer(response)
#     writer.writerow(['MSISDN', 'NAME', 'ADDRESS', 'UPC DATE', 'SSA', 'REASON FOR PO', 'REMARKS', 'FEEDBACK DATE', 'USER'])  
#     query = request.GET.get('q')
#     object_list = Mobile.objects.filter(
#         Q(msisdn__icontains=query)  
#     )
#     mobiles = object_list.values_list(
#         'msisdn',
#         'name',
#         'address',
#         'upc_date',
#         'ssa__name',
#         'reason_for_PO',
#         'remarks',
#         'feedback_date',
#         'user'
#     )

#     if (len(mobiles) > 0):
#         for mobile in mobiles:
#             writer.writerow(mobile)

#         return response

#     else:
#         return HttpResponseRedirect(reverse('filter1'))

