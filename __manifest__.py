# -*- coding: utf-8 -*-
{
    'name': "chart_app",

    'summary': """
        Enhance your business analytics with advanced charts""",

    'description': """
        Chart App - Advanced Analytics for Your Business

        Features:
        - Intuitive chart generation
        - Integration with major Odoo modules
        - Customizable views for your specific business needs
        - User-friendly interface
        
        Benefit from insightful data visualization tools and elevate your decision-making process with Chart App.
    """,

    'author': "Tarek Eissa",
    'maintainer': "Tarek Eissa",
    'contributors': [""],
    'website': "https://www.yourcompany.com",
    
    'category': 'Analytics',
    'version': '1.0',

    'license': "Other proprietary",
    'depends': ['base', 'website','spreadsheet_dashboard', 'base_setup', 'portal', 'web', 'web_editor'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/chart_list.xml',
        'views/chart_detial.xml',
        # 'views/chart_builder_view.xml',
        # 'views/assets_backend.xml',
        # 'chart_app/static/src/xml/custom_chart.xml',
        # 'views/spreadsheet_dashboard.group.view.form.xml'
        # 'views/spreadsheet_dashboard.xml',
    ],
    'qweb': [
        'static/src/xml/custom_chart.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'chart_app/static/src/js/execute_js.js',
        ],
    },


    'demo': [
        'demo/demo.xml',
    ],

    'images': [
        'static/description/main_screenshot.png',
        'static/src/img/pngwing.com.png'
    ],

    'application': True,
    'installable': True,
}
