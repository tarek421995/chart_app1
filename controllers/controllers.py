import base64
from odoo import http
from odoo.http import request
import json

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
