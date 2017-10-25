<template>
    <div class="dashboard">
        <!-- <h1 class="title">SenseNub</h1> -->

        <div id="background">
            <section id="white"></section>
            <section id="scroller" v-bind:style="{ left: '-' + temperature.current * 10 + '%' }"></section>
        </div>

        <smallgraph :item="temperature"></smallgraph>
        <smallgraph :item="humidity"></smallgraph>
        <smallgraph :item="pressure"></smallgraph>

        <!-- <div class="graph">
            <div v-for="value, key in data" class="bar" v-bind:style="{ height: (parseFloat(value) * 10) + 'px', left: (key * 7) + 'px' }">
            </div>
            <h1>Temperature</h1>
            <h2>{{ temperature }}°C</h2>
        </div> -->
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
                    min: 0,
                    max: 40,
                    percentage: 50,
                    name: 'Temperature',
                },
                humidity: {
                    current: 30,
                    min: 0,
                    max: 60,
                    percentage: 50,
                    name: 'Humidity',
                },
                pressure: {
                    current: 1000,
                    min: 0,
                    max: 1500,
                    percentage: 50,
                    name: 'Pressure',
                },
                data: [],
                test: 0
            }
        },
        created () {
            for (var i = 0; i < 100; i++) { this.data.push(Math.floor((Math.random() * 50) + 1)); }

            this.pubnub.load();
        },
        mounted () {
            var that = this;

            this.$pubnub.subscribe({ channels: ['test-channel'] });

            this.$pubnub.addListener({
                message: function(message) {
                    var data = message.message;
                    // that.temperature.current = Math.floor((Math.random() * 40) + 1);

                    // TEMPERATURE
                    that.temperature.current = Math.round(data.temperature * 100) / 100;
                    that.temperature.percentage = (that.temperature.current / that.temperature.max) * 100;
                    if (that.temperature.current > that.temperature.max) { that.temperature.max = that.temperature.current }

                    // HUMIDITY
                    that.humidity.current = Math.round(data.humidity * 100) / 100;
                    that.humidity.percentage = (that.humidity.current / that.humidity.max) * 100;
                    if (that.humidity.current > that.humidity.max) { that.humidity.max = that.humidity.current }
                    
                    // PRESSURE
                    that.pressure.current = Math.round(data.pressure * 100) / 100;
                    that.pressure.percentage = (that.pressure.current / that.pressure.max) * 100;
                    if (that.pressure.current > that.pressure.max) { that.pressure.max = that.pressure.current }

                    // that.data.push(temp + that.test);                    
                    // if (that.data.length > 100) that.data.shift();
                }
            });
        }
    }
</script>