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
        data() {
            return {
                temperature: {
                    current: '-',
                    name: 'Temperature',
                    color: '255, 122, 122',
                    abbr: '°C',
                },
                humidity: {
                    current: '-',
                    name: 'Humidity',
                    color: '111, 111, 255',
                    abbr: '%',
                },
                pressure: {
                    current: '-',
                    name: 'Pressure',
                    color: '76, 177, 76',
                    abbr: 'mb',
                },

                viewing: [],                
                chartdata: [],

                data: null,
            }
        },
        mounted() {
            var that = this;
            this.pubnub.load();
            this.$pubnub.subscribe({ channels: ['constant-data', 'hourly-data'] });
            this.$pubnub.addListener({
                message: function(message) {
                    that.data = message.message;

                    that.temperature.current = Math.round(that.data.temperature * 100) / 100;
                    that.humidity.current = Math.round(that.data.humidity * 100) / 100;
                    that.pressure.current = Math.round(that.data.pressure * 100) / 100;
                    
                    // if (data.channel == 'constant-data') { that.renderChart(that.viewing) }
                }
            });
        },
        watch: {
            data() { console.log(this.data); }
        },
        computed: {

        },
        methods: {

        },
    }
</script>