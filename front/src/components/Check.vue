<script setup>
import { onMounted, ref } from "vue"

const props = defineProps(["data"])
const showDetails = ref(false)
const indicator = ref()

function updateIndicator(value) {
    value = Math.max(0, Math.min(value, 100));
    
    indicator.value.style.width = value + '%';

    const red = 255 - Math.floor((value / 100) * 255);  
    const green = Math.floor((value / 100) * 255);      
    indicator.value.style.backgroundColor = `rgb(${red}, ${green}, 0)`;

    valueText.innerText = value + ' / 100';
}

onMounted(() => {
    updateIndicator(props.data.total)
})
</script>

<template>
<main class="tab-content result-tab">
    <div class="result-section">
        <h2><strong>Результат проверки</strong></h2>
        <p>Выявлено проблем {{ props.data.defiances.length }}/5</p>
    </div>
    <div class="result-section"></div>

    <div class="score-container">
        <div class="issues" v-if="props.data.defiances.length > 0">
            <h3>Выявленные проблемы</h3>
            <ul>
                <li v-for="text in props.data.defiances">{{ text }}</li>
            </ul>
        </div>
        <div class="issues" v-else>
            <h3>Проблем нету!</h3>
        </div>
        <div class="score">
            <h3>Общая оценка</h3>
            <div class="indicator-container">
                <div ref="indicator" class="indicator"></div>
                <div class="value-text">{{ Math.floor(props.data.total * 100) / 100 }}</div>
            </div> 
        </div>
    </div>
    <div class="score-container">
      <div class="report-container">
          <a :href="'/files/' + props.data['file']" class="report-link">Скачать отчёт в DOCX</a>
      </div>
      <div class="report-container">
        <label class="toggle-label toggle-button" @click="showDetails = !showDetails">Подробная оценка</label>
        <div class="details" v-show="showDetails">
          <div class="table">
            <div class="circle-container">
                <div class="label">Масштабирование</div>
                <div class="circle" :style="{'--percent': props.data['Zoom']}"></div>
            </div>
            <div class="circle-container">
                <div class="label">Описание картинок</div>
                <div class="circle" :style="{'--percent': props.data['Alt']}"></div>
            </div>
            <div class="circle-container">
                <div class="label">Контраст текста</div>
                <div class="circle" :style="{'--percent': props.data['Contrast']}"></div>
            </div>
            <div class="circle-container">
                <div class="label">Описание кнопок</div>
                <div class="circle" :style="{'--percent': props.data['Buttons']}"></div>
            </div>
            <div class="circle-container">
                <div class="label">PDF Документы</div>
                <div class="circle" :style="{'--percent': props.data['Document']}"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
</main></template>
