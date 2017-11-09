<template>
    <div class="dashboard">
        <!-- <h1 class="title">SenseNub</h1> -->

        <div id="background">
            <section id="white"></section>
            <section id="scroller" v-bind:style="{ left: '-' + temperature.current * 10 + '%' }"></section>
        </div>

        <aside>
            <div class="graphClick" v-on:click="viewing = temperature"><smallgraph :item="temperature"></smallgraph></div>
            <div class="graphClick" v-on:click="viewing = humidity"><smallgraph :item="humidity"></smallgraph></div>
            <div class="graphClick" v-on:click="viewing = pressure"><smallgraph :item="pressure"></smallgraph></div>
        </aside>

        <main>
            <h1>{{ viewing.name }}</h1>
            <div class="chart"><canvas id="chart"></canvas></div>
        </main>
    </div>
</template>

<script>
    import smallgraph from './components/SmallGraph.vue';

    export default {
        name: 'dashboard',
        components: { smallgraph },
        data () {
            return {
                temperature: {
                    current: 20,
                    name: 'Temperature',
                    color: '255, 122, 122',
                    abbr: '°C',
                },
                humidity: {
                    current: 30,
                    name: 'Humidity',
                    color: '111, 111, 255',
                    abbr: '%',
                },
                pressure: {
                    current: 1000,
                    name: 'Pressure',
                    color: '76, 177, 76',
                    abbr: 'mb',
                },
                viewing: [],                
                chartdata: [],
                data: [],
                myChart: null,
            }
        },
        created () {
            for (var i = 0; i < 100; i++) { this.data.push(Math.floor((Math.random() * 50) + 1)); }
            this.pubnub.load();
        },
        watch: {
            viewing() {
                this.myChart.destroy();
                this.renderChart(this.viewing);
            },
            chartdata() {
                this.myChart.destroy();
                this.renderChart(this.viewing);
            },
        },
        computed: {
            chartdata: function() {
                return this.data;
            }
        },
        methods: {
            renderChart: function(viewing) {
                var that = this;
                this.$pubnub.history({
                    channel: 'constant-data',
                    count: 12,
                },
                function (status, response) {
                    // Fill in the big graphs
                    for (var i = 0; i < response.messages.length; i++)
                    {
                        switch (viewing.name)
                        {
                            case 'Temperature':
                                that.chartdata[i] = response.messages[i].entry.temperature;
                                break;
                            case 'Humidity':
                                that.chartdata[i] = response.messages[i].entry.humidity;
                                break;
                            case 'Pressure':
                                that.chartdata[i] = response.messages[i].entry.pressure;
                                break;
                        }
                    }

                    // add the new data
                    that.chartdata[12] = viewing.current;
                    console.log(that.chartdata);

                    // make labels
                    var labels = ["One hour ago", "Now"];
                    for (var i = 2; i <= 12; i++) { labels.unshift(i + " hours ago"); }

                    var ctx = document.getElementById("chart").getContext('2d');
                    that.myChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: viewing.abbr,
                                borderColor: 'rgb('+ viewing.color + ')',
                                backgroundColor: 'rgba('+ viewing.color + ', 0.1)',
                                data: that.chartdata
                            }]
                        },
                        options: {
                            maintainAspectRatio: false,
                            elements: { line: { tension: 0 }},
                            legend: { display: false },
                            scales: {
                                xAxes: [{ barPercentage: 1 }],
                                yAxes: [{ ticks: { beginAtZero: true } }]
                            }
                        }
                    });  
                })
            }
        },
        mounted () {
            var that = this;
            this.viewing = this.temperature;

            this.$pubnub.subscribe({ channels: ['constant-data', 'hourly-data'] });
            this.$pubnub.addListener({
                message: function(message) {
                    var data = message.message;

                    that.temperature.current = Math.round(data.temperature * 100) / 100;
                    that.humidity.current = Math.round(data.humidity * 100) / 100;
                    that.pressure.current = Math.round(data.pressure * 100) / 100;
                    
                    // TODO: SWITCH CONSTANT WITH HOURLY
                    if (data.channel == 'constant-data')
                    {
                        that.renderChart(that.viewing) // re-render
                    }
                }
            });

            this.renderChart(this.viewing);
        }
    }
</script>