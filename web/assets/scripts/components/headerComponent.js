export const headerComponent = {
    template: `
      <header class="header">
        <div class="container">
          <div class="header__wrapper">
            <span class="header__name-mobile">Добрый король и<br/>весёлые сыроежки</span>
            <button class="header__btn-mobile" @click="onClickMobileMenu"></button>
            <nav class="header__menu">

              <template v-for="item in headerMenu">
                <a :href="item.to" :target="[item.blank ? '_blank' : '']" class="header__menu-item" :class="{'has-special-icon': item.special}">
                  <span class="header__menu-item-icon">
                      <img v-if="item.icon" :src="item.icon" class="custom-icon" />
                      <svg v-else width="24px" height="24px" viewBox="0 0 20 20" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                          <g id="Dribbble-Light-Preview" transform="translate(-420.000000, -6319.000000)" fill="currentColor">
                            <g id="icons" transform="translate(56.000000, 160.000000)">
                              <path d="M376,6169 L380,6169 L380,6165 L376,6165 L376,6169 Z M368,6169 L372,6169 L372,6165 L368,6165 L368,6169 Z M382,6177 L378,6177 L378,6171 L376,6171 L376,6169 L372,6169 L372,6171 L370,6171 L370,6177 L366,6177 L366,6161 L382,6161 L382,6177 Z M372,6177 L376,6177 L376,6175 L372,6175 L372,6177 Z M364,6179 L384,6179 L384,6159 L364,6159 L364,6179 Z" id="emoji_minecraft_square-[#409]"></path>
                            </g>
                          </g>
                        </g>
                      </svg>
                  </span>{{ item.name }}
                </a>
              </template>

            </nav>
          </div>
        </div>
      </header>
    `,
    data: () => ({
        headerMenu: [
            {
                to: '/',
                name: 'Главная',
                blank: false
            },
            {
                to: '/wonders.html',
                name: 'Чудеса',
                blank: false
            },
            {
                to: '/rules.html',
                name: 'Правила',
                blank: false
            },
            {
                to: '/players.html',
                name: 'Игроки',
                blank: false
            },
            {
                to: '/bans.html',
                name: 'Баны',
                blank: false
            },
			{
                to: '/sitemap.html',
                name: 'Библиотека',
                blank: false
            },
            {
                to: 'http://t.me/OTRYAD_GODZILLA',
                name: 'Телеграм',
                blank: true,
                icon: 'assets/images/icons/telegram_logo.svg',
                special: true
            },
        ],
        onClickMobileMenu: (event) => {
            if(event.target.classList.contains('header__btn-mobile_active')) {
                event.target.classList.remove('header__btn-mobile_active')
                document.getElementsByClassName('header__menu')[0].classList.remove('header__menu_active')
            } else {
                event.target.classList.add('header__btn-mobile_active')
                document.getElementsByClassName('header__menu')[0].classList.add('header__menu_active')
            }
        }
    })
}