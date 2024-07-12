export const footerComponent = {
    template: `
      <footer class="footer">
        <div class="container">
          <div class="footer__wrapper">
            <div class="footer__col">
              <img src="` + window.location.protocol + '//' + window.location.host + '/' + `assets/images/logo.png" alt="" class="footer__logo">
            </div>
            <div class="footer__col">
              <span class="footer__info footer__text">
                Данный проект является некоммерческим и не связан с Mojang AB. 
              </span>
              <span class="footer__copyright footer__text">© 2024 Добрый король и веселые сыроежки.<br />Все права защищены.</span>
            </div>
            <div class="footer__col">
              <nav class="footer__menu">
                <a v-for="item in footerMenu" :href="item.to" class="footer__menu-item">{{ item.name }}</a>
              </nav>
            </div>
            <div class="footer__col">
              <div class="footer__social">
                <a href="https://discord.gg/wjSQsGW8rD" target="_blank" class="footer__social-item"><i class="pi pi-discord"></i></a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    `,
    data: () => ({
        footerMenu: [
            {
                to: '/',
                name: 'Карта Мира'
            },
            {
                to: '/rules.html',
                name: 'Правила'
            },
            {
                to: '/players.html',
                name: 'Игроки'
            },
            {
                to: '/bans.html',
                name: 'Баны'
            },
			{
                to: '/sitemap.html',
                name: 'Оглавление сайта'
            },
        ]
    })
}