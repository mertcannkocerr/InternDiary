from django.urls import path, include
from .views import (DiaryRecordsHomeView, RecordContentViewForIntern, SelectedInternRecordsViewForEmployee)

urlpatterns = [
    # /diaryRecords/
    path('', DiaryRecordsHomeView.as_view(), name='diary_records_home'),

    # /diaryRecords/[record.id] for intern user only
    path('<int:record_id>/', RecordContentViewForIntern.as_view(), name='record_content_intern'),

    path('selected_intern/<int:intern_id>', SelectedInternRecordsViewForEmployee.as_view(), name='records_of_given_intern'),

]