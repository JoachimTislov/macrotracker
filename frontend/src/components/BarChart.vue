<script setup lang="ts">
import { reactive, watch } from 'vue'

const props = defineProps<{
  name: string
  data: number[]
}>()

const bar_chart_data = reactive({
  series: [
    {
      name: props.name,
      data: props.data
    }
  ],
  options: {
    chart: {
      type: 'bar',
      foreColor: '#fff'
    },
    xaxis: {
      categories: ['Calories', 'Protein', 'Carbohydrates', 'Fat', 'Sugar'],
      labels: {
        style: {
          fontSize: '12px'
        }
      }
    },
    plotOptions: {
      bar: {
        borderRadius: 8,
        borderRadiusApplication: 'end',
        horizontal: true
      }
    },
    tooltip: {
      theme: 'dark' // Tooltip theme set to dark
    },
    dataLabels: {
      enabled: true,
      total: {
        enabled: true,
        style: {
          color: '#373d3f',
          fontSize: '40px',
          fontFamily: undefined,
          fontWeight: 600
        }
      }
    },
    title: {
      style: {
        fontSize: '12px'
      },
      text: props.name,
      align: 'center'
    },
    toolbar: {
      enabled: false,
      show: false,
      menu: {
        item: {
          colors: ''
        }
      }
    }
  }
})

watch(
  () => props.data,
  (newData) => {
    bar_chart_data.series[0].data = newData
  }
),
  { deep: true }

watch(
  () => props.name,
  (newName) => {
    bar_chart_data.series[0].name = newName
    bar_chart_data.options.title.text = newName
  }
),
  { deep: true }
</script>

<template>
  <apexchart :options="bar_chart_data.options" :series="bar_chart_data.series"> </apexchart>
</template>
