import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import seaborn as sns

import numpy as np
from numpy.random import rand
import math
 
# from matplotlib import ft2font
import base64
from io import BytesIO
from matplotlib import rcParams
rcParams['axes.titlepad'] = 30

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(data2, name, d1, d2, title, xlabel, ylabel):
    # print(data2)
    plt.switch_backend('AGG')
    sns.set_style("darkgrid")
    plt.figure(figsize=(10,6))
    
    plt.title(title +" between " + d1 + " and " + d2 + " in " + name, color='red',fontsize=14)
    
    # ax=sns.countplot(x='SSA', hue='reason_for_PO', data=data2)
    # plt.pie(data2['feedback'], labels=data2['SSA'],autopct='%1.1f%%')

    if data2.shape[1] == 3 and name=='EZ circles':
        # palette = {'Bad network': 'red', 'High tariff':'yellow', 'No 4G': 'blue', 'Others':'C2'} #
        palette = {
            'Billing issues': '#7E2E84', 'Value Added Services':'#FFFF00', 'Poor network coverage':'#0000FF', \
            'High tariff':'#058C42', 'Low data speed':'#16DB65', 'Absence of 4G':'#AF1B3F', \
            'Poor customer care':'#FF0000', 'Recharge issues':'#D14081', 'Others':'#FF4000'
        }
        ax=sns.barplot(x='CIRCLE', y='feedback', hue='reason_for_PO', data=data2, palette = palette)     # palette = "Blues"
        # ax=sns.countplot(x='circle',  y='msisdn', hue='reason_for_PO', data=data2)

    elif data2.shape[1] == 3 and name.find('BSNL') != -1:
        ax=sns.barplot(x='SSA', y='feedback', hue='reason_for_PO', data=data2)
               
        # df =data2.groupby(['ssa', 'reason_for_PO']).agg(Total =("msisdn",'count'))
        # df =df.reset_index()
        # # print(df)
        # ax[0][0]=sns.barplot(x='ssa', y='Total', hue='reason_for_PO', data=df)
             
    elif data2.shape[1] ==2 and name=='EZ circles':
        # print("ENTERED")
        ax=sns.barplot(x='CIRCLE', y='Count', data=data2)    
        
    elif data2.shape[1] == 2 and name.find('BSNL') != -1:
        ax=sns.barplot(x='SSA', y='feedback', data=data2)

    else:
        # print("Check number of columns returned- should be 2 or 3")
        pass
      
    
    for p in ax.patches:
        height = p.get_height()
        if math.isnan(height): 
            continue
        else:
            # print("Height: ", height)
            ax.text(p.get_x()+p.get_width()/2., height + 0.1, height, ha="center")

    # ax.set_ylim(0, max(data2['Count']) * 1.1)
    # ax.set_ylim(0, 10)
    plt.xticks(rotation=45, fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlabel(xlabel, fontsize = 10, weight = 'bold')
    
    plt.ylabel(ylabel, fontsize=10)
    plt.legend(loc='upper center')
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_plot_upc(data2, name, d1, d2, title, xlabel, ylabel):
    
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    
    plt.title(title +" between " + d1 + " and " + d2 + " in " + name, color='green',fontsize=14)
    
    # print(data2.shape[1])
    
    if data2.shape[1] ==2 and name=='EZ circles':
        ax=sns.barplot(x='CIRCLE', y='Total UPC generated', data=data2, ci=None,orient='v',)  
        if ax.patches:
            for p in ax.patches:
                height = p.get_height()
                if math.isnan(height): 
                    continue
                else:
                    # print("Height: ", height)
                    ax.text(p.get_x()+p.get_width()/2., height + 0.1, height, ha="center")

            ax.set_ylim(0, max(data2['Total UPC generated']) * 1.1)
        else:
            pass

        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)

        plt.xlabel(xlabel, fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
        plt.legend(loc='upper center')

    elif data2.shape[1] == 2 and name.find('BSNL') != -1:
        # ax=sns.barplot(x='SSA', y='Total UPC generated', data=data2)
        plt.pie(data2['Total UPC generated'], labels=data2['SSA'],autopct='%1.1f%%', pctdistance=0.5,)
        # plt.legend(loc='lower right')

    else:
        # print("Check number of columns returned- should be 2")   
        pass
    
    
    plt.tight_layout()
    graph = get_graph()
    return graph