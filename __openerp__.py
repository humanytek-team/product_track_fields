# -*- coding: utf-8 -*-
{
    'name': 'Campos adicionales en productos',
    'version': '1.1',
    'summary': 'En el catálogo de producto se agregan los campos "Fecha primera entrada", "Fecha última entrada", "Cantidad última entrada", "Tiempo de entrega promedio" y "Devoluciones", en la pestaña de información general.',
    'category': 'Product',
    'description': """
    En el catálogo de producto se agregan los campos "Fecha primera entrada", "Fecha última entrada", "Cantidad última entrada", "Tiempo de entrega promedio" y "Devoluciones", en la pestaña de información general.
    """,
    'author': 'Humanytek',
    'website': 'http://www.humanytek.com',
    'depends': ['product','common_models'],
    'data': [
        'product_template_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
