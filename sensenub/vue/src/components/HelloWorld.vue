<template>
    <div class="hello">
        <h2>Humidity</h2>
        <p v-if="data.length == 0">No data is available.</p>
        <p v-if="data.length > 0">Data recieved: {{ data.length }}</p>
        <div class="graph">
            <div v-for="value, key in data" class="bar" v-bind:style="{ height: (parseFloat(value) * 10) + 'px', left: (key * 7) + 'px' }">
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'HelloWorld',
        data () {
            return {
                data: []
            }
        },
        created () {
            for (var i = 0; i < 100; i++)
            {
                this.data.push(Math.floor((Math.random() * 50) + 1));
            }

            this.pubnub.load();
        },
        mounted () {
            var that = this;

            this.$pubnub.subscribe({ channels: ['test-channel'] });

            this.$pubnub.addListener({
                message: function(message) {
                    var data = message.message;

                    data.text = (data.text != null && data.text != '') ? data.text : '-No message-';
                    
                    that.data.push(data.text);                    
                    if (that.data.length > 100) that.data.shift();
                    console.log(that.data);
                }
            });
        }
    }
</script>