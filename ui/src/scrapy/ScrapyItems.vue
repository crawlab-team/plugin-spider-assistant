<template>
  <cl-table
      class="scrapy-items"
      :data="tableData"
      :columns="tableColumns"
      hide-footer
  />
</template>

<script lang="ts">
import {computed, defineComponent, h} from 'vue';
import {ClTag} from 'crawlab-ui';
import {useRoute, useRouter} from 'vue-router';
import {useStore} from 'vuex';

export default defineComponent({
  name: 'ScrapyItems',
  props: {
    form: {
      type: Object,
    }
  },
  setup(props, {emit}) {
    const router = useRouter();

    const route = useRoute();

    const id = computed(() => route.params.id);

    const store = useStore();

    const gotoFile = (filepath) => {
      store.commit(`spider/setDefaultFilePaths`, [filepath]);
      router.push({
        path: `/spiders/${id.value}/files`,
      });
    };

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

    const tableData = computed(() => {
      const {items} = props.form;
      return items || [];
    });

    const tableColumns = computed(() => {
      return [
        {
          key: 'name',
          label: 'Name',
          width: '200',
        },
        {
          key: 'fields',
          label: 'Fields',
          width: '800',
          value: (row) => {
            if (!row.fields) return [];
            return row.fields.map(f => h(ClTag, {
              label: f.name,
              clickable: true,
              type: getType(f),
              tooltip: f.type ? `Field Type: ${f.type}` : '',
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
              onClick: () => {
                gotoFile(row.filepath);
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
.scrapy-items >>> .el-table {
  border-top: none;
  border-left: none;
  border-right: none;
}

.scrapy-items >>> .el-table .el-tag {
  margin-right: 10px;
}
</style>
