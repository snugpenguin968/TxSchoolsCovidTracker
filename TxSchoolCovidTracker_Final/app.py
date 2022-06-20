from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for,Response
import re
import pandas as pd
csv_file_src='Texas-school-data_tgt.csv'
from dateutil.parser import parse
import cgi
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pylab as plt
import matplotlib.patches as mpatches
# Used for calculating regressions

app = Flask(__name__)

name=''
startdate=''
enddate=''
school_v=''
df_new2=pd.read_csv(csv_file_src)
ticks=[]
y=[]
prev_ticks=[]
prev_y=[]
new_ticks=[]
new_y=[]

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/hello', methods=['POST'])
def hello():
   global name
   global startdate
   global enddate
   global school_v
   name  = request.form.get('School').upper()
   school_v= request.form.get('schoolType')
   startdate=request.form.get('from')
   enddate=request.form.get('to')

#### start with case in table format

   file_out_v = 'html_table.csv'
   fileout=open(file_out_v, "w")
   finding =['Weekly Report Date,District Name,Campus  ,Student Cases\n']
   fileout.writelines(finding)
   count_v=0
   ln =[]
   line =[]

   if name:
       csv_f=open(csv_file_src,"r")
       for line in csv_f:
         ln = line.split (',')

         if (( name + " " + school_v in line) and \
            (datetime.strptime(str(ln[0]),"%Y-%m-%d")) >= (datetime.strptime(startdate,"%m/%d/%Y")) and \
            (datetime.strptime(str(ln[0]),"%Y-%m-%d")) <= (datetime.strptime(enddate,"%m/%d/%Y"))):
           print (" school found..."+ line)
           count_v =+ 1

           if (len(ln) >= 8 & count_v < 1 ):
             finding = str(ln[0]) + ","+ str(ln[1]) +  ", "+ str(ln[3]) + ", "+ str(ln[5]) +"\n"
           elif (len(ln) >= 8 & count_v > 1 ):
             finding.append ( str(ln[0]) + ","+ str(ln[1]) +  ", "+ str(ln[3]) + ", "+ str(ln[5]))
           fileout.writelines(finding)

       fileout.close()
       csv_f.close()
       a=pd.read_csv(file_out_v)
#       return render_template('hello.html', tables=[a.to_html(index=False)], titles=[''])         

#### start with graphic result section

   startdate=startdate.split('/')
   enddate=enddate.split('/')
   startdate=startdate[2]+'-'+startdate[0]+'-'+startdate[1]
   enddate=enddate[2]+'-'+enddate[0]+'-'+enddate[1]
   school_v= request.form.get('schoolType')
   df_new2.index=df_new2['report_date']
   global ticks
   global y
   global prev_ticks
   global prev_y
   global new_ticks
   global new_y
   if school_v=='D':
    ticks=df_new2.loc[(df_new2['District_Name']==(name+' ISD TOTAL'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))].index
    y=df_new2.loc[(df_new2['District_Name']==(name+ ' ISD TOTAL'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))]['Student_Cases'].tolist()
    prev_ticks=df_new2.loc[(df_new2['District_Name']==(name+ ' ISD TOTAL'))&(df_new2.index<startdate)].index
    prev_y=df_new2.loc[(df_new2['District_Name']==(name+ ' ISD TOTAL'))&(df_new2.index<startdate)]['Student_Cases'].tolist()
    new_ticks=df_new2.loc[(df_new2['District_Name']==(name+ ' ISD TOTAL'))&(df_new2.index>enddate)].index
    new_y=df_new2.loc[(df_new2['District_Name']==(name+ ' ISD TOTAL'))&(df_new2.index>enddate)]['Student_Cases'].tolist()

   elif school_v=='H S':
     ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' H S'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))].index
     y=df_new2.loc[(df_new2['Campus'].str.contains(name+' H S'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))]['Student_Cases'].tolist()
     prev_ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' H S'))&(df_new2.index<startdate)].index
     prev_y=df_new2.loc[(df_new2['Campus'].str.contains(name+' H S'))&(df_new2.index<startdate)]['Student_Cases'].tolist()
     new_ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' H S'))&(df_new2.index>enddate)].index
     new_y=df_new2.loc[(df_new2['Campus'].str.contains(name+' H S'))&(df_new2.index>enddate)]['Student_Cases'].tolist()
   elif school_v=='J H':
     ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' J H'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))].index
     y=df_new2.loc[(df_new2['Campus'].str.contains(name+' J H'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))]['Student_Cases'].tolist()
     prev_ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' J H'))&(df_new2.index<startdate)].index
     prev_y=df_new2.loc[(df_new2['Campus'].str.contains(name+' J H'))&(df_new2.index<startdate)]['Student_Cases'].tolist()
     new_ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' J H'))&(df_new2.index>enddate)].index
     new_y=df_new2.loc[(df_new2['Campus'].str.contains(name+' J H'))&(df_new2.index>enddate)]['Student_Cases'].tolist()
   elif school_v=='MIDDLE':
     ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' MIDDLE'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))].index
     y=df_new2.loc[(df_new2['Campus'].str.contains(name+' MIDDLE'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))]['Student_Cases'].tolist()
     prev_ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' MIDDLE'))&(df_new2.index<startdate)].index
     prev_y=df_new2.loc[(df_new2['Campus'].str.contains(name+' MIDDLE'))&(df_new2.index<startdate)]['Student_Cases'].tolist()
     new_ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' MIDDLE'))&(df_new2.index>enddate)].index
     new_y=df_new2.loc[(df_new2['Campus'].str.contains(name+' MIDDLE'))&(df_new2.index>enddate)]['Student_Cases'].tolist()
   else:
     ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' EL'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))].index
     y=df_new2.loc[(df_new2['Campus'].str.contains(name+' EL'))&(((df_new2.index)>=startdate)&((df_new2.index)<=enddate))]['Student_Cases'].tolist()
     prev_ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' EL'))&(df_new2.index<startdate)].index
     prev_y=df_new2.loc[(df_new2['Campus'].str.contains(name+' EL'))&(df_new2.index<startdate)]['Student_Cases'].tolist()
     new_ticks=df_new2.loc[(df_new2['Campus'].str.contains(name+' EL'))&(df_new2.index>enddate)].index
     new_y=df_new2.loc[(df_new2['Campus'].str.contains(name+' EL'))&(df_new2.index>enddate)]['Student_Cases'].tolist()
   ticks=sorted(ticks)
   new_ticks=sorted(new_ticks)
   prev_ticks=sorted(prev_ticks)

   if len(y)>0:
     return render_template('results.html', school_v=name + " " + school_v, dt_rng_v=startdate + " to " + enddate, tables=[a.to_html(index=False,classes='mystyle',max_rows=30,justify='center' )], titles=[''])
     #return render_template('results.html',name=y)
     print ("after  call...")
     a.close()

   return redirect(url_for('index'))
    


@app.route('/plot.png')
def plot_png():
  fig = create_figure()
  output = io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(), mimetype='image/png')
def create_figure():
  fig = Figure()
  fig.set_figheight(20)
  fig.set_figwidth(40)
  fig.set_frameon(False)
  fig.suptitle('Covid Cases for the Search',fontsize=40,fontweight='bold')
  axis = fig.add_subplot(1, 1, 1,facecolor='#F2F2F2')
  axis.set_xlabel('Date',fontsize=30,labelpad=50)
  axis.set_ylabel('Number of Cases',fontsize=30,rotation=0,labelpad=175)
  axis.tick_params(axis='both',labelsize=20)
  if len(ticks)>16:
    axis.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    new_ticks=[pd.to_datetime(date,format='%Y-%m-%d').date() for date in ticks]
    axis.plot(new_ticks,y,marker='o')
  else:
    axis.plot(ticks,y,marker='o')
  return fig
  
@app.route('/plot2.png')
def plot_png2():
  fig2=create_figure2()
  output2=io.BytesIO()
  FigureCanvas(fig2).print_png(output2)
  return Response(output2.getvalue(),mimetype='image/png')
def create_figure2():
  print(prev_ticks,prev_y,new_ticks,new_y,flush=True)
  fig = Figure()
  fig.set_figheight(20)
  fig.set_figwidth(40)
  fig.set_frameon(False)
  fig.suptitle('Covid Cases in Context',fontsize=40,fontweight='bold')
  axis = fig.add_subplot(1, 1, 1,facecolor='#F2F2F2')
  axis.set_xlabel('Date',fontsize=30,labelpad=50)
  axis.set_ylabel('Number of Cases',fontsize=30,rotation=0,labelpad=175)
  axis.tick_params(axis='both',labelsize=20)

  red_patch=mpatches.Patch(color='red',label='Your Search')
  fig.legend(handles=[red_patch],fontsize=40)
  axis.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
  axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
  
  datetime_ticks=[pd.to_datetime(date,format='%Y-%m-%d').date() for date in ticks]
  new_datetime_ticks=[pd.to_datetime(date,format='%Y-%m-%d').date() for date in new_ticks]    
  prev_datetime_ticks=[pd.to_datetime(date,format='%Y-%m-%d').date() for date in prev_ticks]

  if len(prev_datetime_ticks)==0:
    axis.plot(datetime_ticks,y,c='r',marker='o')
    axis.plot([datetime_ticks[-1],new_datetime_ticks[0]],[y[-1],new_y[0]],color='blue',marker='o')
    axis.plot(new_datetime_ticks,new_y,c='blue',marker='o')
  elif len(new_datetime_ticks)==0:
    axis.plot(prev_datetime_ticks,prev_y,c='blue',marker='o')
    axis.plot([prev_datetime_ticks[-1],datetime_ticks[0]],[prev_y[-1],y[0]],color='blue',marker='o')
    axis.plot(datetime_ticks,y,c='r',marker='o')

  else:
    axis.plot(prev_datetime_ticks,prev_y,c='blue',marker='o')
    axis.plot([prev_datetime_ticks[-1],datetime_ticks[0]],[prev_y[-1],y[0]],color='blue',marker='o')
    axis.plot(datetime_ticks,y,c='r',marker='o')
    axis.plot([datetime_ticks[-1],new_datetime_ticks[0]],[y[-1],new_y[0]],color='blue',marker='o')
    axis.plot(new_datetime_ticks,new_y,c='blue',marker='o')
  fig.autofmt_xdate(rotation=30)
  return fig

   
   

if __name__ == '__main__':
   app.run(debug=True)
