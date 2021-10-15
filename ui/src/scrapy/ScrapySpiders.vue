<template>
  <cl-table
      class="scrapy-spiders"
      :data="tableData"
      :columns="tableColumns"
      hide-footer
  />
</template>

<script lang="ts">
import {computed, defineComponent, h} from 'vue';
import {ClNavLink} from 'crawlab-ui';
import {useRoute, useRouter} from 'vue-router';
import {useStore} from 'vuex';

export default defineComponent({
  name: 'ScrapySpiders',
  props: {
    form: {
      type: Object,
      default: () => {
        return [];
      },
    },
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
      const {spiders} = props.form;
      return spiders || [];
    });

    const tableColumns = computed(() => {
      return [
        {
          key: 'name',
          label: 'Name',
          icon: ['fa', 'font'],
          width: '160',
        },
        {
          key: 'type',
          label: 'Type',
          icon: ['fa', 'spider'],
          width: '160',
        },
        {
          key: 'filepath',
          label: 'File Path',
          icon: ['fa', 'file'],
          width: '600',
          value: (row) => h(ClNavLink, {
            label: row.filepath,
            onClick: () => {
              gotoFile(row.filepath);
            }
          })
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
.scrapy-spiders >>> .el-table {
  border-top: none;
  border-left: none;
  border-right: none;
}
</style>
