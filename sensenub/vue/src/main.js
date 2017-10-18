import Vue from 'vue'
import App from './App'
import router from './router'

require('./assets/style.css')

Vue.config.productionTip = false

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