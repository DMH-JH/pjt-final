from django import forms
from django.template import loader
from django.utils.safestring import mark_safe


class starWidget(forms.TextInput):
    input_type = 'rating'
    template_name = "widgets/star_rate.html"

    class Media:
        css = {
            'all': [
                'widgets/rateit/rateit.css',
            ],
        }
        js = [
            "//code.jquery.com/jquery-3.4.1.min.js",
            'widgets/rateit/jquery.rateit.min.js',
        ]

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.update({
            'min': 0,
            'max': 5,
            'step': 1,
        })
        return attrs

    # def __init__(self, attrs=None, wrapper_class='simplemde-box', options=''):
    #     # 템플릿을 출력할 때 wrapper_class와 options 변수를 넘겨주기 위해 가져온다.
    #     self.wrapper_class = wrapper_class
    #     self.options = options

    #     super(starWidget, self).__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['...'] = '...'
        return context
    

    # def render(self, name, value, attrs=None, renderer=None):
    #     context = {
    #         'widget': {
    #             'name': name,
    #             'value': value,
    #             'wrapper_class': self.wrapper_class,
    #             'options': self.options,
    #         }
    #     }

    #     # 템플릿을 렌더링한다.
    #     template = loader.get_template(self.template_name).render(context)

    #     # 템플릿 파일의 문자열을 이스케이프하고 반환한다.
    #     return mark_safe(template)