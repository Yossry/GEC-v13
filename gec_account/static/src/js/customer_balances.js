odoo.define('gec_account.customerBalances', function (require) {
    "use strict";

    var core = require('web.core');
    var QWeb = core.qweb;

    var Widget = require('web.Widget');
    var Context = require('web.Context');
    var data_manager = require('web.data_manager');
    var widget_registry = require('web.widget_registry');
    var config = require('web.config');


    var _t = core._t;

    var customerBalances = Widget.extend({
        template: 'gec_account.journalItems',
        events: _.extend({}, Widget.prototype.events, {
            'click .fa-info-circle': '_onClickButton',
        }),

        init: function (parent, params) {
            this.data = params.data;
            this._super(parent);
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._setPopOver();
            });
        },

        updateState: function (state) {
            this.$el.popover('dispose');
            var candidate = state.data[this.getParent().currentRow];
            if (candidate) {
                this.data = candidate.data;
                this.renderElement();
                this._setPopOver();
            }
        },

        _setPopOver: function () {
            var self = this;
            this.data.debug = config.isDebug();
            var $content = $(QWeb.render('gec_account.journalItemsDetailPopOver', {
                data: this.data,

            }));

            var $journalItemsButton = $content.find('.action_open_journal_items');
            $journalItemsButton.on('click', function(ev) {

                ev.stopPropagation();
                data_manager.load_action('gec_account.action_account_moves_line_partner').then(function (action) {
                    // Change action context to choose a specific date and product(s)
                    // As grid_anchor is set to now() by default in the data, we need
                    // to load the action first, change the context then launch it via do_action
                    // additional_context cannot replace a context value, only add new
                    //
                    // in case of kit product, the forecast view show the kit's components
                    console.log('SELF =>',self.data.account_id)
                    self._rpc({
                        model: 'account.move.line',
                        method: 'search',
                        args: [[['partner_id','=',self.data.partner_id.data.id]]]
                    }).then(function (res) {
                        console.log('ACTION',action)
                        console.log('RES',res)
//                        var additional_context = {};
//                        additional_context.grid_anchor = self.data.delivery_date_grid;
//                        additional_context.search_default_warehouse_id = [self.data.warehouse_id.data.id];
//                        action.context = new Context(action.context, additional_context);
                        action.domain = [
                            ['partner_id', '=', self.data.partner_id.data.id],
                            ['account_id', '=', self.data.account_id.data.id]

                        ];
                        self.do_action(action);
                    });
                });
            });

            var options = {
                content: $content,
                html: true,
                placement: 'right',
                title: _t('Apuntes del asociado'),
                trigger: 'focus',
                delay: {'show': 0, 'hide': 100 },
            };
            this.$el.popover(options);
        },

        _onClickButton: function () {
            this.$el.find('.fa-info-circle').prop('special_click', true);
        },


    });

    widget_registry.add('customer_balances', customerBalances);

    return customerBalances;
});
