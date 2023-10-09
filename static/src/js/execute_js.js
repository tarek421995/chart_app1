odoo.define('chart_app.execute_js', function (require) {
    "use strict";
    
    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');

    var ExecuteJS = AbstractAction.extend({
        hasControlPanel: true,
        start: function () {
            this._super.apply(this, arguments);
            console.log('startong')
            if (this.params && this.params.js_code) {
                var js_code = this.params.js_code;
                console.log('js_code',js_code)
                try {
                    eval(js_code);
                } catch (e) {
                    console.error("Error executing JS Code:", e);
                }
            } else {
                console.error("JS Code or parameters not found");
            }
        }
    });

    core.action_registry.add('execute_js', ExecuteJS);
    
    return ExecuteJS;
});
