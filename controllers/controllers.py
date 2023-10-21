import base64
from odoo import http
from odoo.http import request
import json
from odoo.exceptions import AccessDenied
from odoo.service import db as odoo_db  # Import the db module from Odoo's service


class ChartController(http.Controller):

    @http.route('/charts', type='http', auth="user", website=True)
    def list_charts(self, **kwargs):
        # Fetch all the charts
        charts = request.env['chart.builder'].sudo().search([])
        return request.render('chart_app.list_charts_template', {'charts': charts})

    @http.route('/charts/<int:chart_id>', type='http', auth="user", website=True)
    def chart_detail(self, chart_id, **kwargs):
        chart = request.env['chart.builder'].sudo().browse(chart_id)
        return request.render('chart_app.chart_detail_template', {'chart': chart, 'chart_id': chart_id})
    
    @http.route('/admin/charts', type='http', auth="user")
    def list_charts_admin(self, **kwargs):
        # Fetch all the charts
        charts = http.request.env['chart.builder'].search([])
        return http.request.render('chart_app.chart_admin_list_template', {'charts': charts})

    @http.route('/admin/charts/<int:chart_id>', type='http', auth="user")
    def chart_detail_admin(self, chart_id, **kwargs):
        chart = http.request.env['chart.builder'].browse(chart_id)
        return http.request.render('chart_app.chart_admin_detail_template', {'chart': chart})

    
    @http.route('/charts/<int:chart_id>/csv', type='http', auth="none")
    def fetch_csv(self, chart_id):
        chart = request.env['chart.builder'].sudo().browse(chart_id)
        if not chart.csv_data_file or isinstance(chart.csv_data_file, bool):
            response_data = json.dumps({"error": "No CSV data found"})
        else:
            csv_data_decoded = base64.b64decode(chart.csv_data_file).decode('utf-8')
            response_data = json.dumps({"csv_data": csv_data_decoded})

        headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        return request.make_response(response_data, headers=headers)


    @http.route('/charts/<int:chart_id>/csv/downloads', type='http', auth="none")
    def download_csv(self, chart_id):
        chart = request.env['chart.builder'].sudo().browse(chart_id)
        if not chart.csv_data_file or isinstance(chart.csv_data_file, bool):
            return request.not_found("No CSV data found")
        else:
            csv_data_decoded = base64.b64decode(chart.csv_data_file)
            response_data = csv_data_decoded

        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename="{chart.csv_filename}"'
        }
        return request.make_response(response_data, headers=headers)



class CustomController(http.Controller):

    @http.route('/login', type='json', auth='none', methods=['POST'], csrf=False)
    def login(self, **post):

        if request.httprequest.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.httprequest.data.decode('utf-8'))
                db_name = data.get('db')  # Renamed variable to db_name to avoid conflict
                if not db_name:
                    return {'status': 'error', 'message': 'Database name is missing or invalid'}
                
                print('odoo_db.list_dbs()',odoo_db.list_dbs())
                # Check if database exists
                if db_name not in odoo_db.list_dbs():  # Use odoo_db.list_dbs() here
                    return {'status': 'error', 'message': 'Database not found'}
                
                login = data.get('login')
                password = data.get('password')
                try:
                    uid = request.session.authenticate(db_name, login, password)
                    if uid:
                        return {'status': 'success', 'message': 'Logged in successfully', 'session_id': request.session.sid}
                    else:
                        return {'status': 'error', 'message': 'Authentication failed'}
                except AccessDenied:
                    return {'status': 'error', 'message': 'Access Denied: Incorrect username or password'}
            except json.JSONDecodeError:
                return {'status': 'error', 'message': 'Invalid JSON payload'}
        else:
            return {'status': 'error', 'message': 'Authentication failed'}
