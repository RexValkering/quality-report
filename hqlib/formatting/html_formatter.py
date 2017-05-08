"""
Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import logging
import pkg_resources
import yattag
from typing import List, Dict, Iterable, Optional, Tuple, Union

from . import base_formatter
from ..report import QualityReport, Section
from ..domain import Metric, DomainObject


class HTMLFormatter(base_formatter.Formatter):
    """ Format the report in HTML. """

    def __init__(self, latest_software_version: str='0', current_software_version: str='0') -> None:
        self.__latest_software_version = latest_software_version
        self.__current_software_version = current_software_version
        super().__init__()

    def prefix(self, report: QualityReport) -> str:
        """ Return a HTML formatted version of the report prefix. """
        parameters = dict(
            title=report.title(),
            date=report.date().strftime('%d-%m-%y %H:%M'),
            current_version=self.__current_software_version,
            new_version_available=self.__new_release_text())
        parameters['section_menu'] = self.__section_navigation_menu(report)
        parameters['domain_object_classes'] = self.__domain_object_classes(report)
        parameters['metric_classes'] = self.__metric_classes(report)
        parameters['metric_sources'] = self.__metric_sources(report)
        parameters['requirements'] = self.__requirements(report)

        prefix = self.__get_html_fragment('prefix')
        return prefix.format(**parameters)

    @staticmethod
    def __get_html_fragment(name: str) -> str:
        """ Read and return a HTML fragment from the html folder. """
        fragment = pkg_resources.resource_string(__name__, 'html/{name}.html'.format(name=name))
        return fragment.decode('utf-8')

    def section(self, report: QualityReport, section: Section) -> str:
        """ Return a HTML formatted version of the section. """
        subtitle = self.__format_subtitle(section.subtitle())
        extra = '<div id="meta_metrics_history_relative_graph"></div>\n' \
                '<div id="meta_metrics_history_absolute_graph"></div>' if section.id_prefix() == 'MM' else ''
        parameters = dict(title=section.title(), id=section.id_prefix(), subtitle=subtitle, extra=extra)
        return self.__get_html_fragment('section').format(**parameters)

    def metric(self, metric: Metric) -> str:
        """ Return a HTML formatted version of the metric. """
        return ''  # pragma: no cover

    @staticmethod
    def __section_navigation_menu(report: QualityReport) -> str:
        """ Return the menu for jumping to specific sections. """
        menu_items = []

        menu_item_template = '<li><a class="link_section_{section_id}" href="#section_{section_id}">{menu_label}</a>' \
                             '</li>'

        def add_menu_item(section: Section, title: str) -> None:
            """ Add a menu item that links to the specified section. """
            menu_items.append(menu_item_template.format(section_id=section.id_prefix(), menu_label=title))

        def add_menu_items(sections: Iterable[Section]) -> None:
            """ Add a header with menu items that link to the specified sections. """
            for each_section in sections:
                add_menu_item(each_section, each_section.title() + ' ' + each_section.subtitle())

        # First, group related sections
        sections: Dict[str, List[Section]] = {}
        titles: List[str] = []
        for section in report.sections():
            title = section.title()
            sections.setdefault(title, []).append(section)
            if title not in titles:
                titles.append(title)
        # Next, create the menu items
        for title in titles:
            if len(sections[title]) == 1:
                section = sections[title][0]
                add_menu_item(section, section.title())
            else:
                add_menu_items(sections[title])
        # Finally, return the HTML as one string
        return '\n'.join(menu_items)

    @staticmethod
    def postfix() -> str:
        """ Return a HTML formatted version of the report postfix. """
        return HTMLFormatter.__get_html_fragment('postfix')

    @staticmethod
    def __format_subtitle(subtitle: str) -> str:
        """ Return a HTML formatted subtitle. """
        template = ' <small>{sub}</small>'
        return template.format(sub=subtitle) if subtitle else ''

    @staticmethod
    def __metric_classes(report: QualityReport) -> str:
        """ Return a HTML table of the metrics the software can measure. """
        row = '  <tr><td>{icon}</td><td>{name} (<code><small>{id}</small></code>)</td><td>{norm}</td></tr>'
        icon_span = '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>'
        result = list()
        result.append('<table class="table table-striped first-col-centered">\n  <tr><th>In dit rapport?</th>'
                      '<th>Metriek (<code><small>Identifier</small></code>)</th><th>Norm</th></tr>')
        for metric_class in report.metric_classes():
            name = metric_class.name
            identifier = metric_class.__name__
            icon = icon_span if metric_class in report.included_metric_classes() else ''
            try:
                norm = metric_class.norm_template.format(**metric_class.norm_template_default_values())
            except ValueError:
                logging.error('Metric class %s had faulty norm template', metric_class.__name__)
                raise
            result.append(row.format(icon=icon, name=name, id=identifier, norm=norm))
        result.append('</table>')
        return '\n'.join(result)

    @staticmethod
    def __metric_sources(report: QualityReport) -> str:
        """ Return a HTML table of the metric sources the software can collect data from. """
        row = '  <tr><td>{icon}</td><td>{name} (<code><small>{id}</small></code>)</td><td>{ins}</td></tr>'
        icon_span = '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>'
        anchor = '<a href="{url}" target="_blank">{url}</a>'
        result = list()
        result.append('<table class="table table-striped first-col-centered">\n  <tr><th>In dit rapport?</th>'
                      '<th>Metriekbron (<code><small>Identifier</small></code>)</th><th>Instanties</th></tr>')
        for metric_source_class in report.metric_source_classes():
            name = metric_source_class.metric_source_name
            identifier = metric_source_class.__name__
            icon = icon_span if metric_source_class in report.included_metric_source_classes() else ''
            instances = report.project().metric_source(metric_source_class)
            instances = instances if isinstance(instances, list) else [instances]
            instances = '<br>'.join([anchor.format(url=instance.url()) for instance in instances if instance.url()])
            result.append(row.format(icon=icon, name=name, id=identifier, ins=instances))
        result.append('</table>')
        return '\n'.join(result)

    @staticmethod
    def __requirements(report: QualityReport) -> str:
        """ Return a HTML table of the requirements. """
        row = '  <tr><td>{icon}</td><td>{name} (<code><small>{id}</small></code>)</td><td>{metrics}</td></tr>'
        icon_span = '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>'
        result = list()
        result.append('<table class="table table-striped first-col-centered">\n  <tr><th>In dit rapport?</th>'
                      '<th>Eis (<code><small>Identifier</small></code>)</th><th>Metrieken</th></tr>')
        for requirement_class in report.requirement_classes():
            name = requirement_class.name()
            identifier = requirement_class.__name__
            metrics = ', '.join(metric_class.name for metric_class in requirement_class.metric_classes())
            icon = icon_span if requirement_class in report.included_requirement_classes() else ''
            result.append(row.format(icon=icon, name=name, id=identifier, metrics=metrics))
        result.append('</table>')
        return '\n'.join(result)

    @staticmethod
    def __domain_object_classes(report: QualityReport) -> str:
        """ Return a HTML table of the domain objects. """
        row = '  <tr><td>{icon}</td><td>{name} (<code><small>{id}</small></code>)</td><td>{default_requirements}</td>' \
              '<td>{optional_requirements}</td></tr>'
        icon_span = '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>'
        result = list()
        result.append('<table class="table table-striped first-col-centered">\n  <tr><th>In dit rapport?</th>'
                      '<th>Domeinobject (<code><small>Identifier</small></code>)</th><th>Default eisen</th>'
                      '<th>Optionele eisen</th></tr>')
        for domain_object_class in report.domain_object_classes():
            name = identifier = domain_object_class.__name__
            default_requirements = ', '.join(req.name() for req in domain_object_class.default_requirements())
            optional_requirements = ', '.join(req.name() for req in domain_object_class.optional_requirements())
            icon = icon_span if domain_object_class in report.included_domain_object_classes() else ''
            result.append(row.format(icon=icon, name=name, id=identifier, default_requirements=default_requirements,
                                     optional_requirements=optional_requirements))
        result.append('</table>')
        return '\n'.join(result)

    def __new_release_text(self) -> str:
        """ Return a line of text if there is a new version of the software available. """
        latest = self.__latest_software_version
        current = self.__current_software_version
        return ' Versie {ver} is beschikbaar.'.format(ver=latest) if latest > current else ''


class DashboardFormatter(object):  # pylint: disable=too-few-public-methods
    """ Return a HTML formatted dashboard for the quality report. """
    @classmethod
    def process(cls, report: QualityReport) -> str:
        """ Return a HTML formatted dashboard. """
        doc, tag, text = yattag.Doc().tagtext()
        with tag('table', klass="table table-condensed table-bordered"):
            with tag('thead'):
                doc.asis(cls.__dashboard_headers(report))
            with tag('tbody'):
                doc.asis(cls.__dashboard_rows(report))
        return yattag.indent(doc.getvalue())

    @staticmethod
    def __dashboard_headers(report: QualityReport) -> str:
        """ Return the headers of the dashboard. """
        doc, tag, text, line = yattag.Doc().ttl()
        with tag('tr', style="color: white; font-weight: bold; background-color: #2F95CF;"):
            for section_type, colspan in report.dashboard()[0]:
                line('th', section_type, colspan=colspan, style="text-align: center;")
        return doc.getvalue()

    @classmethod
    def __dashboard_rows(cls, report: QualityReport) -> str:
        """ Return the rows of the dashboard. """
        doc, tag, text, line = yattag.Doc().ttl()
        for row in report.dashboard()[1]:
            with tag('tr'):
                for cell in row:
                    colspan, rowspan = cell[2] if len(cell) == 3 else (1, 1)
                    with tag('td', colspan=colspan, rowspan=rowspan, align='center', bgcolor=cell[1]):
                        section_id = cell[0].short_name() if isinstance(cell[0], DomainObject) else cell[0].upper()
                        section = report.get_section(section_id)
                        title = section.title() if section else '???'
                        line('div', '', klass="link_section_{}".format(section_id), title=title)
                        line('div', '', id="section_summary_chart_{}".format(section_id))
        return doc.getvalue()
