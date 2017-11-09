<template>
	<section>
        <div class="icon">
            <i v-if="item.abbr == '°C'" style="background-color: #ff7a7a; padding: 1.5vh 2.8vh;" class="fa fa-thermometer-half"></i>
            <i v-if="item.abbr == '%'" style="background-color: #6f6fff; padding: 1.8vh 2.8vh;" class="fa fa-tint"></i>
            <i v-if="item.abbr == 'mb'" style="background-color: #4cb14c; padding: 1.4vh 1.75vh;" class="fa fa-cube"></i>
        </div>
        <div class="info">
            <h1>{{ item.current }} {{ item.abbr }}</h1>
            <h2>{{ item.name }}</h2>
        </div>
    </section>
</template>

<script>
    export default {
    	name: 'smallgraph',
        props: ['item'],
        data() {
            return {
            }
        }
    }
</script>
