
const routes = [
  {
    path: '/user',
    component: () => import('layouts/UserLayout.vue'),
    children: [
      { path: '',       component: () => import('pages/user/MainPage.vue') },
      { path: 'help',   component: () => import('pages/user/HelpPage.vue') },
      { path: 'book',   component: () => import('pages/user/BookPage.vue') },
    ]
  },
  {
    path: "/login",
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LoginPage.vue') }
    ]
  },
  {
    path: "/airline",
    component: () => import('layouts/AirlineLayout.vue'),
    children: [
      { path: '',           component: () => import('pages/airline/MainPage.vue') },
      { path: 'aircrafts',  component: () => import('pages/airline/AircraftsPage.vue') },
      { path: 'flights',    component: () => import('pages/airline/FlightsPage.vue') },
    ]
  },
  {
    path: "/airport",
    component: () => import('layouts/AirportLayout.vue'),
    children: [
      { path: '',         component: () => import('pages/airport/MainPage.vue') },
      { path: 'flights',  component: () => import('pages/airport/FlightsPage.vue') },
      { path: 'books',    component: () => import('pages/airport/BooksPage.vue') },
    ]
  },
  {
    path: "/manage",
    component: () => import('layouts/ManageLayout.vue'),
    children: [
      { path: '',           component: () => import('pages/manage/MainPage.vue') },
      { path: 'users',      component: () => import('pages/manage/UsersPage.vue') },
      { path: 'airports',   component: () => import('pages/manage/AirportsPage.vue') },
      { path: 'airlines',   component: () => import('pages/manage/AirlinesPage.vue') },
    ]
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
