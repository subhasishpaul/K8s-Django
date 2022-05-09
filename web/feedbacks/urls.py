from django.urls import path
from feedbacks import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='feedbacks/change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),

    # Home
    path('', views.index, name='index'),

    path('register', views.register, name='register'),
    path('user_details', views.UserListView.as_view(), name='user_details'),
    path('searchuser/', views.SearchUserView.as_view(), name='searchuser'),

    # plot UPC generated
    path('selcircle/', views.SearchByCirclePlot, name='selcircle'),
    path('plot/', views.plot, name='plot'),
 
    # plot feedback done
    path('feedback/', views.SearchByCircleFeedPlot, name='feedback'),
    path('feed_plot/', views.feedplot, name='feedplot'),

    # circle-wise search
    path('searchbycircle/', views.SearchByCircle, name='searchbycircle'),
    path('search_results3/', views.SearchResultsView3.as_view(), name='search_results3'),
    path('csv_circle_wise/', views.export_csv_circle_wise, name='csv_circle_wise'),
    
    # search by ssa
    path('searchbyssa', views.SearchBySsa, name='searchbyssa'),
    path('ajax/load-ssas/', views.load_ssas, name='ajax_load_ssas'),
    path('search_results4/', views.SearchResultsView4.as_view(), name='search_results4'),
    path('csv_ssa_wise/', views.export_csv_ssa_wise, name='csv_ssa_wise'),

    # search by msisdn sequence
    path('searchsingle/', views.HomePageView2.as_view(), name='searchsingle'),    
    path('search_results2/', views.SearchResultsView2.as_view(), name='search_results2'),
    # path('csv/', views.export_csv_single, name='csv'),
    

    path('mobiles/', views.MobileListView.as_view(), name='mobiles'),

    path('mobile/<int:pk>', views.MobileDetailView, name='mobile_detail'),
    # path('feedback_form/<int:pk>', views.FeedbackUpdateView, name='feedback'),
    # path('exportfulldata/', views.export_full_data, name='export_full_data'),

    
       
    # path('searchfilter/', views.search_filter, name='searchfilter'),
 
    
    # path('filter1/', views.all_mobiles, name='filter1'),
    # path('show/', views.Show_data, name='show'),
    
    # path('xls/', views.export_users_xls, name='xls'),
    
    # search by upc_date range
    # path('searchbyupc/', views.HomePageView.as_view(), name='searchbyupc'),
    # path('search_results/', views.SearchResultsView.as_view(), name='search_results'),
    # path('export_csv_upc_range/', views.export_csv_upc_range, name='export_csv_upc_range'),

]