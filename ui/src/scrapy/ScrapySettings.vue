<template>
  <cl-table
      class="scrapy-settings"
      :data="tableData"
      :columns="tableColumns"
      hide-footer
  />
</template>

<script lang="ts">
import {computed, defineComponent, h} from 'vue';
import {ClTag} from 'crawlab-ui';

export default defineComponent({
  name: 'ScrapySettings',
  props: {
    form: {
      type: Object,
    }
  },
  setup(props, {emit}) {
    const getType = ({type}) => {
      switch (type) {
        case 'str':
          return 'primary';
        case 'int':
        case 'float':
          return 'success';
        case 'bool':
          return 'danger';
        case 'dict':
        case 'list':
        case 'tuple':
          return 'warning';
        default:
          return 'info';
      }
    };

    const getValue = ({type, value}) => {
      switch (type) {
        case 'str':
          return h(ClTag, {
            label: value,
            type: getType({type}),
          });
        case 'int':
        case 'float':
          return h(ClTag, {
            label: value,
            type: getType({type}),
          });
        case 'bool':
          return h(ClTag, {
            label: value ? 'true' : 'false',
            type: value ? 'success' : 'danger',
          });
        case 'dict':
          return value.map(v => h(ClTag, {
            label: `${v.key.value}: ${v.value.value}`,
            type: getType({type}),
          }));
        case 'list':
        case 'tuple':
          return value.map(v => h(ClTag, {
            label: `${v.value}`,
            type: getType({type}),
          }));
        default:
          return value;
      }
    };

    const tableData = computed(() => {
      const {settings} = props.form;
      return settings || [];
    });

    const tableColumns = computed(() => {
      return [
        {
          key: 'name',
          label: 'Name',
          icon: ['fa', 'font'],
          width: '240',
        },
        {
          key: 'type',
          label: 'Type',
          icon: ['fa', 'list'],
          width: '160',
          value: (row) => h(ClTag, {
            label: row.type,
            type: getType(row),
          })
        },
        {
          key: 'value',
          label: 'Value',
          icon: ['fa', 'spider'],
          width: '600',
          value: (row) => getValue(row)
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
.scrapy-settings >>> .el-table {
  border-top: none;
  border-left: none;
  border-right: none;
}

.scrapy-settings >>> .el-table .el-tag {
  margin-right: 10px;
}
</style>
