
const routes = [
  {
    path: "/",
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '',       component: () => import('pages/LoginPage.vue') },
      { path: '/register', component: () => import('pages/RegisterPage.vue') }
    ]
  },
  {
    path: '/user',
    component: () => import('layouts/UserLayout.vue'),
    children: [
      { path: '',         component: () => import('pages/user/BookPage.vue') },
      { path: 'help',     component: () => import('pages/user/HelpPage.vue') },
      { path: 'flights',  component: () => import('pages/user/FlightsPage.vue') },
      { path: 'wallet',   component: () => import('pages/user/WalletPage.vue') },
      { path: 'info',     component: () => import('pages/user/InfoPage.vue') },
    ]
  },

  {
    path: "/airline",
    component: () => import('layouts/AirlineLayout.vue'),
    children: [
      { path: '',             component: () => import('pages/airline/FlightsPage.vue') },
      { path: 'aircrafts',    component: () => import('pages/airline/AircraftsPage.vue') },
      { path: 'flight_types', component: () => import('pages/airline/FlightTypesPage.vue') },
    ]
  },
  {
    path: "/airport",
    component: () => import('layouts/AirportLayout.vue'),
    children: [
      { path: '',         component: () => import('pages/airport/FlightsPage.vue') },
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
