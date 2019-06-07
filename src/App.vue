<template>
  <v-app light>
    <v-navigation-drawer fixed v-model="drawer" app>
      <h1>{{appName}}</h1>
      <v-divider></v-divider>
      <v-list dense class="pt-0">
        <v-list-tile v-for="item in items" :key="item.title" :href="item.href">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>

          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar color="primary">
      <v-toolbar-side-icon @click.stop="drawer = !drawer" class="white--text"></v-toolbar-side-icon>
      <v-toolbar-title href="/" class="white--text">{{appName}}</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-content id="content">
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'app',
  data: () => ({
    appName: 'Malayalam word predictor',
    items: [
      { title: 'Predictor', icon: 'apps', href: '/' },
      { title: 'About', icon: 'question_answer', href: '/about' },
      { title: 'Code', icon: 'code', href: 'https://gitlab.com/smc/mlpredict' },
      { title: 'Api', icon: 'code', href: '/api' }
    ],
    drawer: null
  })
}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, "Lato", "Manjari", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#content {
  margin-top: 20px;
}
</style>
