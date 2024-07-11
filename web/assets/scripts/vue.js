const { createApp, ref } = Vue
import { headerComponent } from "./components/headerComponent.js";
import { footerComponent } from "./components/footerComponent.js";

const App = createApp({
    setup() {
        let dataBansExpandedRows = ref();
        const dataBansList = ref()
        let dataPlayersExpandedRows = ref();
        const dataPlayersList = ref()

        return {
            dataBansExpandedRows,
            dataBansList,
            dataPlayersExpandedRows,
            dataPlayersList
        }
    },
    methods: {
        async getConfigBans() {
            let response = await fetch('../assets/json/bans.json')
            this.dataBansList = await response.json()
        },
        async getConfigPlayers() {
            let response = await fetch('../assets/json/players.json')
            this.dataPlayersList = await response.json()
        },
        saveText(event) {

            navigator.clipboard.writeText('/' + event.target.innerText)

            let message = document.createElement('div');
            message.className = "air-message air-message_copy";
            message.innerHTML = "<span>Команда успешно скопирована.</span>";
            const blockInner = document.getElementById("app")
            blockInner.prepend(message);


            event.target.classList.add('content__command_active')
            setTimeout(() => {
                event.target.classList.remove('content__command_active')
                message.remove()
            }, 2000);
        }
    },
    mounted() {
        this.getConfigBans()
        this.getConfigPlayers()
    }
})

App.use(PrimeVue.Config, {
    theme: {
        preset: PrimeVue.Themes.Aura,
        options: {
            darkModeSelector: 'light',
        }
    }
});

App.component('p-datatable', PrimeVue.DataTable)
App.component('p-column', PrimeVue.Column)
App.component('app-header', headerComponent)
App.component('app-footer', footerComponent)
App.mount('#app')