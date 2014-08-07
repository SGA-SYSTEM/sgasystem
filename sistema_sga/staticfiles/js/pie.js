function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

$(function () {
    var chart;       
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'categoryPieChart'
            },title: {
                text: 'Category'
            },tooltip: {
                formatter: function() {
                    return '<b>'+ this.point.name +'</b>: '+ numberWithCommas(this.y.toFixed(2));
                }
            },exporting: {
                enabled: false
            },plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: true,
                            formatter: function() {
                                return '<b>'+ this.point.name +'</b>: '+ Math.round(this.percentage) +' %';
                            }
                        }
                    }
                },series: [{
                    type: 'pie',
                    data: [
                        {% for cat in categories %}
                        [
                            '{{ cat.name }}', 
                            {% if cat.amount > 0 %}
                                {{ cat.amount }}
                            {% else %}
                                0
                            {% endif %}
                        ],
                        {% endfor %}
                    ]
                }]
            });
        });
    });
});