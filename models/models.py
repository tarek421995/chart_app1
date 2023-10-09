import base64
from odoo import models, fields, api, _
import csv
from io import StringIO
import json

class ChartDataSource(models.Model):
    _name = 'chart.data.source'
    _description = 'Chart Data Sources'

    name = fields.Char(string='Data Source Name', required=True, help="A descriptive name for this data source.")
    model_id = fields.Many2one('ir.model', string='Data Source', help="Select the source of data for this entry")
    field_ids = fields.One2many('chart.data.source.field', 'data_source_id', string='Data Fields')
    chart_id = fields.Many2one('chart.builder', string='Related Chart', ondelete='cascade')

class ChartDataSourceField(models.Model):
    _name = 'chart.data.source.field'
    _description = 'Chart Data Source Fields'

    name = fields.Char(string='Field Description')
    field_id = fields.Many2one('ir.model.fields', string='Field Name', domain="[('model_id', '=', parent.model_id)]")
    data_source_id = fields.Many2one('chart.data.source', string='Data Source')

class ChartBuilder(models.Model):
    _name = 'chart.builder'
    _description = 'Chart Builder'

    name = fields.Char(string='Chart Name', required=True)
    data_source_ids = fields.Many2many('chart.data.source', 'chart_data_source_rel', 'chart_id', 'data_source_id', string='Data Sources')
    chart_data = fields.Text(string='Chart Data (JSON)', help="The data to be visualized in JSON format")
    js_code = fields.Text(string='JS Code for Chart', help="JS code to render the chart")

    csv_data_file = fields.Binary(string='CSV Data File')
    csv_filename = fields.Char(string='CSV Filename')

    thumbnail = fields.Binary()
    sequence = fields.Integer()
    group_ids = fields.Many2many('res.groups', default=lambda self: self.env.ref('base.group_user'))


    @api.depends('data_source_ids')
    def _compute_chart_data(self):
        for record in self:
            data_list = []
            for source in record.data_source_ids:
                model = source.model_id.model
                Model = self.env[model]
                for field in source.field_ids:
                    field_name = field.field_id.name
                    data_list.append({
                        'name': f"{source.name}_{field_name}",
                        'values': Model.search([]).mapped(field_name)
                    })

            record.chart_data = json.dumps(data_list)


    def button_execute_js(self):
        js_code = self.js_code  # Fetch JS code from the record.
        # Ideally, your JS code should be static and not fetched from the database.
        return {
            'type': 'ir.actions.client',
            'tag': 'execute_js',
            'params': {
                'js_code': js_code,
        },
}

    def extract_chart_data(self):
        """Extract the chart data from the models."""
        data_list = []
        for source in self.data_source_ids:
            model = source.model_id.model
            Model = self.env[model]
            for field in source.field_ids:
                field_name = field.field_id.name
                data_list.append({
                    'name': f"{source.name}_{field_name}",
                    'values': Model.search([]).mapped(field_name)
                })
        return data_list
    
    def export_data_source_csv(self):
        self.ensure_one()

        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)

        header = []
        fields_mapping = {}
        index_fields = {}
        row_counter = 0

        for data_source in self.data_source_ids:
            model_name = data_source.model_id.model
            for ds_field in data_source.field_ids:
                field_name = ds_field.field_id.name
                combined_name = f"{model_name}_{field_name}"
                header.append(combined_name)
                fields_mapping[combined_name] = ds_field.field_id
                if ds_field.name.lower() == 'index':
                    index_fields[model_name] = field_name

        writer.writerow(header)

        primary_model = self.data_source_ids[0].model_id.model
        primary_records = self.env[primary_model].search([])

        for primary_record in primary_records:
            row = []

            for combined_name, field in fields_mapping.items():
                model_name = field.model_id.model
                field_name = field.name
                field_type = field.ttype

                # If the current model has an 'index' field, use it to search for a matching record
                if model_name in index_fields:
                    index_value = getattr(primary_record, index_fields[primary_model])
                    records = self.env[model_name].search([(index_fields[model_name], '=', index_value.id if isinstance(index_value, models.BaseModel) else index_value)], limit=1)
                    record = records[0] if records else None
                else:
                    # Fallback to get records sequentially if no index field is found
                    records = self.env[model_name].search([])
                    record = records[row_counter] if len(records) > row_counter else None

                if record:
                    if field_type == 'many2one':
                        field_content = record[field_name].name if record[field_name] else ''
                    elif field_type in ['many2many', 'one2many']:
                        field_content = ', '.join([related.name for related in record[field_name][:5]])
                    else:
                        field_content = record[field_name]
                else:
                    field_content = ''

                row.append(field_content)

            writer.writerow(row)
            row_counter += 1

        output.seek(0)
        file_data = output.getvalue().encode()
        attachment_vals = {
            'name': 'chart_data_source_export.csv',
            'datas': base64.b64encode(file_data),
            'res_model': 'chart.builder',
            'res_id': self.id,
            'type': 'binary',
        }

        attachment = self.env['ir.attachment'].create(attachment_vals)
        self.csv_data_file = base64.b64encode(file_data)
        self.csv_filename = 'chart_data_source_export.csv'
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }



    # field_id = fields.Many2one('ir.model.fields', string='Data Field', domain="[('model_id', '=', model_id)]", help="Select the field (column) of data you want to visualize")