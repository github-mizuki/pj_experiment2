from django import forms
from .models import MainTask, SubTask, Log


class LogCreateForm(forms.ModelForm):

    class Meta:
        model = Log
        fields = ['matter', 'maintask']
        widgets = {
            'matter': forms.Textarea(attrs={'rows':2}),
            'maintask': forms.Select()
            }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(LogCreateForm, self).__init__(*args,**kwargs)
        self.fields['maintask'].queryset = MainTask.objects.filter(user_id=user.id, archive=False)
        self.fields['maintask'].empty_label = '未選択で投稿'

class LogCreateForm2(forms.ModelForm):

    class Meta:
        model = Log
        fields = ['matter',]
        widgets = {
            'matter': forms.Textarea(attrs={'rows':2})
            }

class LogUpdateForm(forms.ModelForm):

    class Meta:
        model = Log
        fields = ['maintask',]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(LogUpdateForm, self).__init__(*args,**kwargs)
        self.fields['maintask'].queryset = MainTask.objects.filter(user_id=user.id, archive=False)
        self.fields['maintask'].empty_label = '未選択にする'






class MainTaskCreateForm(forms.ModelForm):
    title = forms.CharField(label='件名')
    summary = forms.CharField(label='概要', widget=forms.Textarea(attrs={'rows':4}), required=False)
    deadline = forms.SplitDateTimeField(label="期限", widget=forms.SplitDateTimeWidget(date_attrs={"type":"date"}, time_attrs={"type":"time"}))
    color = forms.CharField(label='color')

    class Meta:
        model = MainTask
        fields = ['title', 'summary', 'deadline', 'color']

class MainTaskUpdateForm(forms.ModelForm):
    title = forms.CharField(label='件名')
    summary = forms.CharField(label='概要', widget=forms.Textarea(attrs={'rows':4}), required=False)
    deadline = forms.SplitDateTimeField(label="期限", widget=forms.SplitDateTimeWidget(date_attrs={"type":"date"}, time_attrs={"type":"time"}))
    color = forms.CharField(label='color')

    class Meta:
        model = MainTask
        fields = ['title', 'summary', 'deadline', 'color']


class SubTaskAddForm(forms.ModelForm):
    title = forms.CharField(label='件名')
    summary = forms.CharField(label='概要', widget=forms.Textarea(attrs={'rows':4}), required=False)
    deadline = forms.SplitDateTimeField(label="期限", widget=forms.SplitDateTimeWidget(date_attrs={"type":"date"}, time_attrs={"type":"time"}))

    class Meta:
        model = SubTask
        fields = ['title', 'summary', 'deadline']

class SubTaskCreateForm(forms.ModelForm):
    title = forms.CharField(label='件名')
    summary = forms.CharField(label='概要', widget=forms.Textarea(
        attrs={'rows': 4}), required=False)
    deadline = forms.SplitDateTimeField(label="期限", widget=forms.SplitDateTimeWidget(
        date_attrs={"type": "date"}, time_attrs={"type": "time"}))

    class Meta:
        model = SubTask
        fields = ['title', 'summary', 'deadline', 'maintask']
        widgets = {
            'maintask': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SubTaskCreateForm, self).__init__(*args, **kwargs)
        self.fields['maintask'].queryset = MainTask.objects.filter(user_id=user.id, archive=False)
        # self.fields['maintask'].empty_label = '未選択で投稿
        print(self.fields['maintask'])

class SubTaskUpdateForm(forms.ModelForm):
    title = forms.CharField(label='件名')
    summary = forms.CharField(label='概要', widget=forms.Textarea(attrs={'rows':4}), required=False)
    deadline = forms.SplitDateTimeField(label="期限", widget=forms.SplitDateTimeWidget(date_attrs={"type":"date"}, time_attrs={"type":"time"}))

    class Meta:
        model = SubTask
        fields = ['title', 'summary', 'deadline']