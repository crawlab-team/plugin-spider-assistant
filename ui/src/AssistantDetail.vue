<template>
  <div class="assistant-detail">
    <div class="top-bar">
      <cl-form
          :model="spiderData"
          :grid="3"
      >
        <cl-form-item :span="1" label="Spider Type">
          <el-select v-model="spiderData.type" disabled>
            <el-option v-for="op in typeOptions" :key="op.value" :label="op.label" :value="op.value"/>
          </el-select>
        </cl-form-item>
      </cl-form>
    </div>
    <div class="spider-content">
      <template v-if="spiderData.type === 'scrapy'">
        <Scrapy/>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import {useRequest} from 'crawlab-ui';
import {useRoute} from 'vue-router';
import Scrapy from './scrapy/Scrapy.vue';

const {
  get,
} = useRequest();

const endpoint = '/plugin-proxy/spider-assistant';

export default defineComponent({
  name: 'AssistantDetail',
  components: {Scrapy},
  setup(props, {emit}) {
    const route = useRoute();

    const spiderData = ref({});

    const typeOptions = ref([
      {value: '', label: 'General'},
      {value: 'scrapy', label: 'Scrapy'},
    ]);

    const getData = async () => {
      const id = route.params.id;
      if (!id) return;
      const res = await get(`${endpoint}/spiders/${id}`);
      const {data} = res;
      spiderData.value = data;
    };

    onMounted(getData);

    return {
      spiderData,
      typeOptions,
    };
  },
});
</script>

<style scoped>
.assistant-detail {
}

.assistant-detail .top-bar {
  padding: 10px 0;
  border-bottom: 1px solid #e6e6e6;
}

.assistant-detail .top-bar >>> .el-form-item {
  margin-bottom: 0;
}
</style>
