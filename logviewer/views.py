import csv
import os
import mimetypes
import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.servers.basehttp import FileWrapper

from django.http import HttpResponse

from logviewer.forms import RecordSearchForm
from logviewer.models import PhoneRecord

import logging

DOWNLOADS_PATH  = "/home/fritz/django-pbx-smdr-accounting"
REPORT_FILENAME = "report.txt"

def download_report (request):
    """Download existing .csv report to user's computer"""
    filename = DOWNLOADS_PATH + "/" + REPORT_FILENAME
    wrapper = FileWrapper (open (filename))
    content_type = mimetypes.guess_type (filename)[0]
    response = HttpResponse (wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize (filename)
    response['Content-Disposition'] = "attachment; filename=%s" % REPORT_FILENAME
    return response
    
def export (records):
    """Export all records to a tab-delimited .csv file"""
    recordWriter = csv.writer (open (REPORT_FILENAME, 'wb'), delimiter = '\t')

    for r in records:
        recordWriter.writerow (r.to_sequence ())
        
def search (request):
    form = RecordSearchForm ()
    records = None
    report_link = ''
    total_duration = 0
    start_date = None
    end_date = None
        
    logging.warn (request.method)
    if request.method == 'POST':
        form = RecordSearchForm (request.POST)
        if form.is_valid ():
            cd = form.cleaned_data
            start_date = cd['start_date']
            end_date = cd['end_date']
            records = PhoneRecord.objects.filter (
                start_time__gt=cd['start_date'],
                start_time__lt=cd['end_date'])
            records = records.filter (ext__in=[100, 107, 108, 113, 119, 8900]);

            if cd['ring'] is False:
                records = records.exclude (type__contains='RG')
            if cd['incoming'] is False:
                records = records.exclude (type__contains='IN')
            if cd['outgoing'] is False:
                records = records.exclude (type__contains='TL')
                records = records.exclude (type__contains='LOC')

            total_duration = datetime.timedelta()

            for one_record in records:
                rec = one_record.f()
                dur = rec['duration']
                total_duration += datetime.timedelta(0, dur.second, 0, 0, dur.minute, dur.hour, 0)
            
            logging.warn(total_duration)

            if 'export' in request.POST:
                export (records)
                report_link = "../report/"
    return render_to_response ('logviewer/records.html',
                               {'form': form, 'phone_records': records,
                                'report_link': report_link,
                                'duration': total_duration,
                                'start_date': start_date,
                                'end_date': end_date},
                                context_instance = RequestContext (request))

