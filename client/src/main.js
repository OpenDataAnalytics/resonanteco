import Vue from "vue";
import Vuetify from "vuetify";
import AsyncComputed from "vue-async-computed";
import vMousetrap from "vue-utilities/v-mousetrap";
import snackbarService from "vue-utilities/snackbar-service";
import promptService from "vue-utilities/prompt-service";
import vueNumeralFilterInstaller from "vue-numeral-filter";
import vueNiceScrollbar from "vue-nice-scrollbar";
import Girder, { RestClient } from "@girder/components/src";
import ResonantGeo from "resonantgeo";

import App from "@/App.vue";
import router from "@/router";
import store from "@/store";
import { API_URL } from "@/constants";
import girder from "@/girder";

import "vuetify/dist/vuetify.min.css";

Vue.use(AsyncComputed);
Vue.use(Vuetify);
Vue.use(Girder);
Vue.use(snackbarService);
Vue.use(promptService);
Vue.use(vMousetrap);
Vue.use(vueNumeralFilterInstaller);
Vue.use(vueNiceScrollbar);

girder.rest = new RestClient({ apiRoot: API_URL });

Vue.config.productionTip = true;

Vue.use(ResonantGeo, {
  girder: girder.rest
});

girder.rest.fetchUser().then(() => {
  new Vue({
    router,
    store,
    render: h => h(App),
    provide: { girderRest: girder.rest }
  })
    .$mount("#app")
    .$snackbarAttach()
    .$promptAttach();
});
