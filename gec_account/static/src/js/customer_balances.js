odoo.define('gec_account.customerBalances', function (require) {
    "use strict";

    var core = require('web.core');
    var QWeb = core.qweb;

    var Widget = require('web.Widget');
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
            console.log(this.data);
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
