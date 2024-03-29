#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################

'''
'''

################################################################################
# Imports


import argparse
import logging
import textwrap

from datetime import datetime
from jinja2 import Environment, PackageLoader
from lxml import etree

from .soap import SOAP_HTTP_Transport, SOAPVersion
from .utils import (
    capitalize,
    find_xsd_namespaces,
    get_get_type,
    open_document,
    remove_namespace,
    url_component,
    url_regex,
    url_template,
    use,
)
from .wsdl import get_wsdl_classes, get_by_name
from .xsd2py import schema_to_py, schema_name

try:
    from logging import NullHandler
except ImportError:
    from .compat import NullHandler


################################################################################
# Constants


TEMPLATE_PACKAGE = 'soapbox.templates'


################################################################################
# Globals


logger = logging.getLogger('soapbox')
logger.addHandler(NullHandler())


################################################################################
# Helpers


def get_rendering_environment():
    '''
    '''
    pkg = TEMPLATE_PACKAGE.split('.')
    env = Environment(
        extensions=['jinja2.ext.loopcontrols'],
        loader=PackageLoader(*pkg),
    )
    env.filters['capitalize'] = capitalize
    env.filters['remove_namespace'] = remove_namespace
    env.filters['url_component'] = url_component
    env.filters['url_regex'] = url_regex
    env.filters['url_template'] = url_template
    env.filters['use'] = use
    env.globals['SOAPTransport'] = SOAP_HTTP_Transport
    env.globals['get_by_name'] = get_by_name
    env.globals['schema_name'] = schema_name
    env.globals['generation_dt'] = datetime.now()
    return env


def generate_code_from_wsdl(xml, target):
    '''
    '''
    env = get_rendering_environment()
    xmlelement = etree.fromstring(xml)
    XSD_NAMESPACE = find_xsd_namespaces(xmlelement.nsmap)
    env.filters['type'] = get_get_type(XSD_NAMESPACE)

    wsdl = get_wsdl_classes(SOAPVersion.SOAP11.BINDING_NAMESPACE)
    definitions = wsdl.Definitions.parse_xmlelement(xmlelement)
    schema = definitions.types.schema
    xsd_namespace = find_xsd_namespaces(xmlelement.nsmap)
    schemaxml = schema_to_py(schema, xsd_namespace)

    tpl = env.get_template('wsdl')
    return tpl.render(
        definitions=definitions,
        schema=schemaxml,
        is_server=bool(target == 'server'),
    )


################################################################################
# Program


def parse_arguments():
    '''
    '''
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Generates Python code from a WSDL document.
            Code can be generated for a simple HTTP client or a server running
            the Django web framework.
        '''))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--client', help='Generate code for a client.', action='store_true')
    group.add_argument('-s', '--server', help='Generate code for a server.', action='store_true')
    parser.add_argument('wsdl', help='The path to a WSDL document.')
    return parser.parse_args()


def main():
    '''
    '''
    opt = parse_arguments()

    if opt.client:
        logger.info('Generating client code for WSDL document \'%s\'...' % opt.wsdl)
        xml = open_document(opt.wsdl)
        print generate_code_from_wsdl(xml, 'client')

    elif opt.server:
        logger.info('Generating server code for WSDL document \'%s\'...' % opt.wsdl)
        xml = open_document(opt.wsdl)
        print generate_code_from_wsdl(xml, 'server')


if __name__ == '__main__':

    main()