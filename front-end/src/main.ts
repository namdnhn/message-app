import './assets/main.css';

import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

const app = createApp(App);

axios.defaults.baseURL = 'http://localhost:8000';

app.mount('#app');
