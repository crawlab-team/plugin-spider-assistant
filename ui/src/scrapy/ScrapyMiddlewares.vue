<template>
  <cl-table
      class="scrapy-middlewares"
      :data="tableData"
      :columns="tableColumns"
      hide-footer
  />
</template>

<script lang="ts">
import {computed, defineComponent, h} from 'vue';
import {ClTag} from 'crawlab-ui';

export default defineComponent({
  name: 'ScrapyMiddlewares',
  props: {
    form: {
      type: Object,
    }
  },
  setup(props, {emit}) {
    const tableData = computed(() => {
      const {middlewares} = props.form;
      return middlewares || [];
    });

    const tableColumns = computed(() => {
      return [
        {
          key: 'name',
          label: 'Name',
          width: '240',
        },
        {
          key: 'methods',
          label: 'Methods',
          width: '800',
          value: (row) => {
            if (!row.methods) return [];
            return row.methods.map(m => h(ClTag, {
              label: m,
              clickable: true,
            }));
          },
        },
        {
          key: 'actions',
          label: 'Actions',
          icon: ['fa', 'tools'],
          width: '180',
          fixed: 'right',
          buttons: (row) => [
            {
              type: 'primary',
              size: 'mini',
              icon: ['fa', 'search'],
              tooltip: 'View',
              onClick: (row) => {
              }
            },
          ],
        },
      ];
    });

    return {
      tableData,
      tableColumns,
    };
  },
});
</script>

<style scoped>
.scrapy-middlewares >>> .el-table {
  border-top: none;
  border-left: none;
  border-right: none;
}

.scrapy-middlewares >>> .el-table .el-tag {
  margin-right: 10px;
}
</style>
