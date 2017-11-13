import Vue from 'vue'
import VueChart from 'vue-chart-js'
import App from './App'
import router from './router'
// import axios from 'axios'
// import VueAxios from 'vue-axios'

require('./assets/style.css')

Vue.config.productionTip = false
Vue.use(VueChart) //, VueAxios, axios)
Vue.use(require('vue-pubnub'), {
	subscribeKey: "sub-c-f4d521fc-b32a-11e7-8d4b-66b981d3b880", // Only the subscribeKey option is mandatory.
	publishKey: "pub-c-c74cc51d-96d1-4126-b62e-73da4542d67b",
	logVerbosity: true,
	ssl: true,
	presenceTimeout: 130
});

new Vue({
	el: '#app',
	router,
	template: '<App/>',
	components: { App }
})