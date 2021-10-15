import yaml


class CUSTOMYAMLDUMPER(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

    def increase_indent(self, flow=False, indentless=False):
        return super(CUSTOMYAMLDUMPER, self).increase_indent(flow, False)
