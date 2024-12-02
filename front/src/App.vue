<script setup>
import Check from "./components/Check.vue"
import { ref } from "vue"

const inputEl = ref()
const requests = ref([])

async function analyze() {
  const response = await fetch("/check/", {"method": "POST", "body": inputEl.value.value})
  const jsonResponse = await response.json()
  requests.value.push(jsonResponse)
}
</script>

<template>
  <div class="title-section">
    <h1>ПРОВЕРКА ДОСТУПНОСТИ</h1>
  </div>

  <div class="subtitle-section">
    <h2>Автоматизированная проверка доступности веб-сайта для пользователей с нарушениями зрения</h2>
  </div>

  <div class="input-section">
    <input ref="inputEl" type="text" id="url-input" placeholder="Введите ссылку на веб-сайт" />
    <button @click="analyze()" id="analyze-btn">Анализировать</button>
  </div>
  <Check v-for="r in requests" :data="r"></Check>

</template>
