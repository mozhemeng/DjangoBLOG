from django import forms


class EmailForm(forms.Form):
    name = forms.CharField(label='您的姓名', max_length=25)
    to = forms.EmailField(label='对方地址')
    # 加上widget=forms.Textarea以扩展为<textarea>标签，加上required=False可以不用必须输入
    comment = forms.CharField(label='附加留言', widget=forms.Textarea, required=False)

