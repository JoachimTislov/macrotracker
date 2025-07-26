<script setup lang="ts">
import { reactive } from 'vue'

const props = defineProps<{
  series: number[]
  labels: string[]
}>()

const macros = reactive({
  series: props.series,
  options: {
    labels: props.labels,
    chart: {
      type: 'donut'
    },
    tooltip: {
      enabled: false
    },
    plotOptions: {
      pie: {
        donut: {
          size: '70%',
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: 'clamp(0.8rem, 1vw, 1.5rem)',
              color: undefined
            },
            value: {
              show: true,
              formatter: function (val: string) {
                const valueInt = parseInt(val)
                const index = props.series.indexOf(valueInt)
                if (index === 0) {
                  return Math.round(valueInt) + ' kcal'
                } else {
                  return Math.round(valueInt) + ' g'
                }
              },
              fontSize: 'clamp(1rem, 2vw, 1.5rem)',
              color: 'white'
            },
            total: {
              show: false,
              label: 'Total',
              color: '#FFFFFF',
              fontSize: '18px'
            }
          }
        }
      }
    },
    legend: {
      show: true,
      position: 'bottom',
      labels: {
        fontSize: '1px',
        colors: 'white'
      }
    }
  }
})
</script>

<template>
  <apexchart :options="macros.options" :series="macros.series"></apexchart>
</template>
