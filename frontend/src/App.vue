<template>
  <div class="app-container">
    <h1>RPA数据看板</h1>
    
    <!-- 筛选器 -->
    <div class="filter-container">
      <a-select v-model:value="selectedCategory" placeholder="选择类别" style="width: 200px; margin-right: 10px;">
        <a-option value="">全部分类</a-option>
        <a-option v-for="category in categories" :key="category" :value="category">
          {{ category }}
        </a-option>
      </a-select>
      <a-button type="primary" @click="fetchData">刷新数据</a-button>
      <a-button @click="analyzeData" style="margin-left: 10px;">AI分析</a-button>
    </div>
    
    <!-- 图表区域 -->
    <div class="chart-container">
      <div class="chart-item">
        <h3>数据趋势</h3>
        <div ref="trendChart" class="chart"></div>
      </div>
      <div class="chart-item">
        <h3>分类占比</h3>
        <div ref="pieChart" class="chart"></div>
      </div>
    </div>
    
    <!-- 数据表格 -->
    <div class="table-container">
      <a-table :columns="columns" :data-source="tableData" row-key="id">
        <template #headerCell="{ column }">
          <div>{{ column.title }}</div>
        </template>
      </a-table>
    </div>
    
    <!-- AI分析结果 -->
    <div v-if="aiAnalysis" class="ai-container">
      <h3>AI智能分析</h3>
      <div class="ai-content">{{ aiAnalysis }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import * as echarts from 'echarts'

export default {
  name: 'App',
  data() {
    return {
      selectedCategory: '',
      categories: [],
      data: [],
      tableData: [],
      trendChart: null,
      pieChart: null,
      aiAnalysis: ''
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://localhost:3000/api/data')
        this.data = response.data
        this.updateCategories()
        this.updateTableData()
        this.renderCharts()
      } catch (error) {
        console.error('获取数据失败:', error)
      }
    },
    updateCategories() {
      const categorySet = new Set(this.data.map(item => item.category))
      this.categories = Array.from(categorySet)
    },
    updateTableData() {
      this.tableData = this.selectedCategory
        ? this.data.filter(item => item.category === this.selectedCategory)
        : this.data
    },
    renderCharts() {
      this.renderTrendChart()
      this.renderPieChart()
    },
    renderTrendChart() {
      if (!this.trendChart) {
        this.trendChart = echarts.init(this.$refs.trendChart)
      }
      
      const filteredData = this.selectedCategory
        ? this.data.filter(item => item.category === this.selectedCategory)
        : this.data
      
      const sortedData = filteredData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
      
      const option = {
        xAxis: {
          type: 'category',
          data: sortedData.map(item => item.timestamp)
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: sortedData.map(item => item.value),
          type: 'line',
          smooth: true
        }]
      }
      
      this.trendChart.setOption(option)
    },
    renderPieChart() {
      if (!this.pieChart) {
        this.pieChart = echarts.init(this.$refs.pieChart)
      }
      
      const categoryData = {}
      this.data.forEach(item => {
        if (categoryData[item.category]) {
          categoryData[item.category] += item.value
        } else {
          categoryData[item.category] = item.value
        }
      })
      
      const option = {
        series: [{
          type: 'pie',
          radius: '60%',
          data: Object.entries(categoryData).map(([name, value]) => ({ name, value }))
        }]
      }
      
      this.pieChart.setOption(option)
    },
    async analyzeData() {
      try {
        const response = await axios.post('http://localhost:3000/api/analyze', { data: this.data })
        const analysis = response.data
        this.aiAnalysis = `
          分析摘要：${analysis.summary}\n\n
          关键洞察：\n          ${analysis.insights.map(insight => `- ${insight}`).join('\n')}\n\n
          建议：\n          ${analysis.recommendations.map(rec => `- ${rec}`).join('\n')}
        `
      } catch (error) {
        console.error('AI分析失败:', error)
        this.aiAnalysis = 'AI分析失败，请稍后重试'
      }
    }
  },
  watch: {
    selectedCategory() {
      this.updateTableData()
      this.renderCharts()
    }
  },
  beforeUnmount() {
    if (this.trendChart) {
      this.trendChart.dispose()
    }
    if (this.pieChart) {
      this.pieChart.dispose()
    }
  }
}
</script>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.filter-container {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.chart-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.chart-item {
  flex: 1;
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
}

.chart {
  height: 300px;
}

.table-container {
  margin-bottom: 30px;
}

.ai-container {
  background: #e6f7ff;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
}

.ai-content {
  margin-top: 10px;
  line-height: 1.6;
}
</style>