
<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex xs12>
        <h2 class="headline">Word predictor</h2>
        <v-text-field
          v-model="input"
          label="Enter text"
          auto-grow
          :value="input"
          :items="predictions"
          v-on:change="generate"
          v-on:input="generate"
        ></v-text-field>
      </v-flex>
      <v-flex xs6>
        <v-text-field
          type="number"
          v-model="c"
          label="How many different sentnences?"
          :value="c"
          v-on:change="generate"
          v-on:input="generate"
        ></v-text-field>
      </v-flex>
      <v-flex xs12>
        <template v-for="(item, index) in predictions">
          <v-list-tile :key="index" avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                <p v-html="item"></p>
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Predictor',
  data: () => ({
    input: 'ആ രീതിയിൽ',
    c: 4,
    predictions: []
  }),

  methods: {
    generate () {
      const start = this.input.trim()
      const wc = 2
      const api = `api/predict?start=${start}&w=${wc}&c=${this.c}`
      axios
        .get(api)
        .then(response => {
          this.predictions = response.data.predictions
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>
