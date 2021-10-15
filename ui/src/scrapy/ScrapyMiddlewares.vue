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
import {useRoute, useRouter} from 'vue-router';
import {useStore} from 'vuex';

export default defineComponent({
  name: 'ScrapyMiddlewares',
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
.scrapy-middlewares >>> .el-table {
  border-top: none;
  border-left: none;
  border-right: none;
}

.scrapy-middlewares >>> .el-table .el-tag {
  margin-right: 10px;
}
</style>
