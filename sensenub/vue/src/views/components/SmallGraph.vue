<template>
	<section class="section_third circle_graph">
        <h1>{{ item.name }}</h1>
        <h2>{{ item.current }} mb</h2>
        <div class="small_graph">
            <div class="bar min" v-bind:style="{ opacity: 1-(item.percentage)/100, width: item.percentage + '%' }"></div>
            <div class="bar max" v-bind:style="{ opacity: item.percentage/100, width: item.percentage + '%' }"></div>
        </div>
        <h4>Min: {{ item.min }} mb</h4>
        <h3>Max: {{ item.max }} mb</h3>
    </section>
</template>

<script>
    export default {
    	name: 'smallgraph',
        props: ['item'],
        data() {
            return {
            }
        },
        mounted() {
            console.log(this.item);
        }
    }
</script>
