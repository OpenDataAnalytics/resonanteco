import Vue from "vue";
import Vuetify from "vuetify";
import AsyncComputed from "vue-async-computed";
import vMousetrap from "vue-utilities/v-mousetrap";
import snackbarService from "vue-utilities/snackbar-service";
import promptService from "vue-utilities/prompt-service";
import vueNumeralFilterInstaller from "vue-numeral-filter";
import Girder, { RestClient } from "@girder/components/src";
import NotificationBus from "@girder/components/src/utils/notifications";
import ResonantGeo from "resonantgeo";

import App from "@/App.vue";
import router from "@/router";
import store from "@/store";
import { API_URL } from "@/constants";
import girder from "@/girder";

import "vuetify/dist/vuetify.min.css";
import vuetify from "./plugins/vuetify";

Vue.use(AsyncComputed);
Vue.use(Vuetify);
Vue.use(Girder);
Vue.use(snackbarService(vuetify));
Vue.use(promptService(vuetify));
Vue.use(vMousetrap);
Vue.use(vueNumeralFilterInstaller);
Vue.use(ResonantGeo);

girder.rest = new RestClient({ apiRoot: API_URL });
const notificationBus = new NotificationBus(girder.rest);
notificationBus.connect();

Vue.config.productionTip = true;

girder.rest.fetchUser().then(() => {
  new Vue({
    router,
    store,
    render: h => h(App),
    vuetify,
    provide: { girderRest: girder.rest, notificationBus }
  })
    .$mount("#app")
    .$snackbarAttach()
    .$promptAttach();
});
