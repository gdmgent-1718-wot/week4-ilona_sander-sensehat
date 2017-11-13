<template>
    <div class="dashboard">
        <div id="background">
            <section id="white"></section>
            <section id="scroller" v-bind:style="{ left: '-' + temperature.current * 10 + '%' }"></section>
        </div>

        <aside>
            <div v-bind:class="{ graphClick: true, selected: ((viewing == temperature) ? true : false) }" v-on:click="viewing = temperature">
                <smallgraph :item="temperature"></smallgraph>
            </div>

            <div v-bind:class="{ graphClick: true, selected: ((viewing == humidity) ? true : false) }" v-on:click="viewing = humidity">
                <smallgraph :item="humidity"></smallgraph>
            </div>
            
            <div v-bind:class="{ graphClick: true, selected: ((viewing == pressure) ? true : false) }" v-on:click="viewing = pressure">
                <smallgraph :item="pressure"></smallgraph>
            </div>
        </aside>

        <main>
            <h1>{{ viewing.name }}</h1>
            <div class="chart">
                <canvas id="chart"></canvas>
            </div>
        </main>
    </div>
</template>

<script>
    import smallgraph from './components/SmallGraph.vue';
    // import axios from 'axios';

    export default {
        name: 'dashboard',
        components: { smallgraph },
        data() {
            return {
                temperature: {
                    current: '-',
                    name: 'Temperature',
                    color: '255, 122, 122',
                    abbr: '°C',
                    data: []
                },
                humidity: {
                    current: '-',
                    name: 'Humidity',
                    color: '111, 111, 255',
                    abbr: '%',
                    data: []
                },
                pressure: {
                    current: '-',
                    name: 'Pressure',
                    color: '76, 177, 76',
                    abbr: 'mb',
                    data: []
                },

                labels: ["One hour ago", "Now"],
                viewing: [],
                data: null,
                myChart: null,
            }
        },
        watch: {
            viewing() {
                this.renderChart();
            }
        },
        mounted() {
            var that = this;
            for (var i = 2; i <= 12; i++) { this.labels.unshift(i + " hours ago"); }

            // PubNub Setup
            this.pubnub.load();
            this.$pubnub.subscribe({ channels: ['constant-data', 'hourly-data'] });

            // Get the latest readings
            this.$pubnub.history({ channel: 'constant-data', count: 1, },
            function (status, response) {
                var data = response.messages[0].entry;
                that.temperature.current = Math.round(data.temperature * 100) / 100;
                that.humidity.current = Math.round(data.humidity * 100) / 100;
                that.pressure.current = Math.round(data.pressure * 100) / 100;
                that.temperature.data[12] = that.temperature.current;
                that.humidity.data[12] = that.humidity.current;
                that.pressure.data[12] = that.pressure.current;
            });

            that.viewing = that.temperature;

            this.$pubnub.history({ channel: 'hourly-data', count: 13 },
            function (status, response) {
                // Fill in the big graphs
                for (var i = 0; i < response.messages.length; i++)
                {
                    that.temperature.data[i] = response.messages[i].entry.temperature;
                    that.humidity.data[i] = response.messages[i].entry.humidity;
                    that.pressure.data[i] = response.messages[i].entry.pressure;
                }

                // Add Listeners
                that.$pubnub.addListener({
                    message: function(message) {
                        that.data = message.message;

                        // Round numbers
                        that.temperature.current = Math.round(that.data.temperature * 100) / 100;
                        that.humidity.current = Math.round(that.data.humidity * 100) / 100;
                        that.pressure.current = Math.round(that.data.pressure * 100) / 100;

                        that.temperature.data[12] = that.temperature.current;
                        that.humidity.data[12] = that.humidity.current;
                        that.pressure.data[12] = that.pressure.current;
                        
                        // Re-render the chart after an hour
                        if (that.data.channel == 'hourly-data')
                        {
                            // Shift array of data
                            that.temperature.data.shift();
                            that.humidity.data.shift();
                            that.pressure.data.shift();

                            that.temperature.data[12] = that.temperature.current;
                            that.humidity.data[12] = that.humidity.current;
                            that.pressure.data[12] = that.pressure.current;
                        }
                    
                        that.updateChart();
                    }
                })

                that.renderChart();
            })

        },
        methods: {
            updateChart() {
                var currentData = this.myChart.data.datasets[0].data;

                switch(this.viewing.name)
                {
                    case "Temperature": this.myChart.data.datasets[0].data = this.temperature.data; break;                    
                    case "Humidity": this.myChart.data.datasets[0].data = this.humidity.data; break;                    
                    case "Pressure": this.myChart.data.datasets[0].data = this.pressure.data; break;                    
                }

                this.myChart.update();
            },
            renderChart() {
                if (this.myChart != null) { this.myChart.destroy(); }
                var that = this;
                var ctx = document.getElementById("chart").getContext('2d');
                this.myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: that.labels,
                        datasets: [{
                            label: that.viewing.abbr,
                            borderColor: 'rgb('+ that.viewing.color + ')',
                            backgroundColor: 'rgba('+ that.viewing.color + ', 0.1)',
                            data: that.viewing.data,
                        }]
                    },
                    options: {
                        maintainAspectRatio: false,
                        elements: { line: { tension: 0 }},
                        legend: { display: false },
                        scales: {
                            xAxes: [{ barPercentage: 1 }],
                            yAxes: [{ ticks: { beginAtZero: true } }],
                        }
                    }
                })
            }
        }
    }
</script>