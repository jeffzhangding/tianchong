
import os
from docxtpl import DocxTemplate
import pandas as pd


class TemplateReplace(object):

    def __init__(self, template_name, setting_dict):
        """"""
        self.settings_dict = setting_dict
        self.template_doc = DocxTemplate(template_name)
        self.tempalte_name = template_name

    def render(self):
        """"""
        for generate_name, settings in self.settings_dict.items():
            context = {}
            for name, v in settings.items():
                if v.get('value_type') == 'sub_doc':
                    context[name] = self.template_doc.new_subdoc(v['value'])
                else:
                    context[name] = v['value']
            self.template_doc.render(context)
            self.template_doc.save(generate_name)


class ParesSettings(object):

    def __init__(self, template=None):
        """"""
        self.tempate = template
        self.template_list = []

    def load_settings(self, f_name):
        """"""
        res = []
        df = pd.read_excel(f_name)
        # single_doc_df = df.groupby('template_doc')
        for template_name, single_temp_df in df.groupby('template_doc'):
            # df.to_dict('records')
            single_temp_st = {}
            for out_name, single_out_df in single_temp_df.groupby('output_doc'):
                st = {}
                for dt in single_temp_df.to_dict('records'):
                    if not dt['key']:
                        continue
                    if dt.get('value_type') == 'sub_doc':
                        value = os.sep.join(['.', 'sub_doc', dt.get('value', '')])
                    else:
                        value = dt.get('value', '')
                    st[dt['key']] = {'value_type': dt.get('value_type'), 'value': value}
                generate_name = os.sep.join(['.', 'output', out_name])

                single_temp_st[generate_name] = st

            template_name = os.sep.join(['.', 'template', template_name])

            res.append([template_name, single_temp_st])
        return res

    def load(self):
        if self.tempate:
            return self.load_settings(self.tempate)
        else:
            res = []
            self.template_list = os.listdir('./settings')
            for f in self.template_list:
                if f.startswith('~'):
                    continue
                f_name = os.sep.join(['.', 'settings', f])
                res.extend(self.load_settings(f_name))
            return res


def pares():
    """"""
    settings_list = ParesSettings().load()
    for template_name, st in settings_list:
        # template_name = os.sep.join(['.', 'template', template_name])
        TemplateReplace(template_name, st).render()


if __name__ == '__main__':
    pares()

