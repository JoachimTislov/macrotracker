<script setup lang="ts">
const props = defineProps<{
  series: number[]
  label: string
}>()

const progressChartOptions = {
  chart: {
    foreColor: '#fff'
  },
  plotOptions: {
    radialBar: {
      hollow: {
        margin: 0,
        size: '65%',
        background: '#293450'
      },
      dataLabels: {
        showOn: 'always',
        name: {
          offsetY: -10,
          fontSize: 'clamp(0.5rem, 1.1vw, 1.15rem)'
        },
        value: {
          offsetY: 2,
          fontSize: 'clamp(1rem, 1vw, 1.5rem)',
          padding: '20px'
        }
      }
    },
    track: {
      dropShadow: {
        enabled: true,
        top: 2,
        left: 0,
        blur: 4,
        opacity: 0.15
      }
    }
  },
  labels: [props.label]
}
</script>

<template>
  <apexchart type="radialBar" :series="series" :options="progressChartOptions"> </apexchart>
</template>
