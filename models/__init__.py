# -*- coding: utf-8 -*-

from . import models


# def export_data_source_csv(self):
        # self.ensure_one()

        # output = StringIO()
        # writer = csv.writer(output, quoting=csv.QUOTE_ALL)

        # header = []
        # fields_mapping = {}
        # index_fields = {}
        # row_counter = 0

        # for data_source in self.data_source_ids:
        #     model_name = data_source.model_id.model
        #     for ds_field in data_source.field_ids:
        #         field_name = ds_field.field_id.name
        #         combined_name = f"{model_name}_{field_name}"
        #         header.append(combined_name)
        #         fields_mapping[combined_name] = ds_field.field_id
        #         if ds_field.name.lower() == 'index':
        #             index_fields[model_name] = field_name

        # writer.writerow(header)

        # primary_model = self.data_source_ids[0].model_id.model
        # primary_records = self.env[primary_model].search([])

        # for primary_record in primary_records:
        #     row = []

        #     for combined_name, field in fields_mapping.items():
        #         model_name = field.model_id.model
        #         field_name = field.name
        #         field_type = field.ttype

        #         # If the current model has an 'index' field, use it to search for a matching record
        #         if model_name in index_fields:
        #             index_value = getattr(primary_record, index_fields[primary_model])
        #             records = self.env[model_name].search([(index_fields[model_name], '=', index_value.id if isinstance(index_value, models.BaseModel) else index_value)], limit=1)
        #             record = records[0] if records else None
        #         else:
        #             # Fallback to get records sequentially if no index field is found
        #             records = self.env[model_name].search([])
        #             record = records[row_counter] if len(records) > row_counter else None

        #         if record:
        #             if field_type == 'many2one':
        #                 field_content = record[field_name].name if record[field_name] else ''
        #             elif field_type in ['many2many', 'one2many']:
        #                 field_content = ', '.join([related.name for related in record[field_name][:5]])
        #             else:
        #                 field_content = record[field_name]
        #         else:
        #             field_content = ''

        #         row.append(field_content)

        #     writer.writerow(row)
        #     row_counter += 1

        # output.seek(0)
        # file_data = output.getvalue().encode()
        # attachment_vals = {
        #     'name': 'chart_data_source_export.csv',
        #     'datas': base64.b64encode(file_data),
        #     'res_model': 'chart.builder',
        #     'res_id': self.id,
        #     'type': 'binary',
        # }

        # attachment = self.env['ir.attachment'].create(attachment_vals)

        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': f'/web/content/{attachment.id}?download=true',
        #     'target': 'self',
        # }

