{
    'name': 'school',
    'version': '1.0',
    'category': 'servicios',
    'author': 'Adrian',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/programa_view.xml',
        'views/inscripcion.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1,
}