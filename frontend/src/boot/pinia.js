import { boot } from 'quasar/wrappers'
import store from 'src/stores/index'


// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(({ app /* , router, ... */ } ) => {
  // something to do
  app.use(store)
})
