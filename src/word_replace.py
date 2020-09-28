
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

    def __init__(self, settings=None, sub_dir=None, temp_dir=None, output_dir=None):
        """"""
        self.settings = settings
        self.settings_list = []
        self.sub_dir = os.path.abspath(sub_dir or os.sep.join(['.', 'sub_doc']))
        self.temp_dir = os.path.abspath(temp_dir or os.sep.join(['.', 'template']))
        self.output_dir = os.path.abspath(output_dir or os.sep.join(['.', 'output']))

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
                        value = os.sep.join([self.sub_dir, dt.get('value', '')])
                    else:
                        value = dt.get('value', '')
                    st[dt['key']] = {'value_type': dt.get('value_type'), 'value': value}
                generate_name = os.sep.join([self.output_dir, out_name])

                single_temp_st[generate_name] = st

            template_name = os.sep.join([self.temp_dir, template_name])

            res.append([template_name, single_temp_st])
        return res

    def load(self):
        if self.settings:
            return self.load_settings(self.settings)
        else:
            res = []
            self.settings_list = os.listdir('./settings')
            for f in self.settings_list:
                if f.startswith('~'):
                    continue
                f_name = os.sep.join(['.', 'settings', f])
                res.extend(self.load_settings(f_name))
            return res


def pares(settings=None, sub_dir=None, temp_dir=None, output_dir=None):
    """"""
    settings_list = ParesSettings(settings, sub_dir, temp_dir, output_dir).load()
    for template_name, st in settings_list:
        # template_name = os.sep.join(['.', 'template', template_name])
        TemplateReplace(template_name, st).render()


if __name__ == '__main__':
    pares()

