<template>
  AssistantDetail
</template>

<script lang="ts">
import {defineComponent, onMounted} from 'vue';
import {useRequest} from 'crawlab-ui';
import {useRoute} from 'vue-router';

const {
  get,
} = useRequest();

const endpoint = '/plugin-proxy/spider-assistant';

export default defineComponent({
  name: 'AssistantDetail',
  setup(props, {emit}) {
    const route = useRoute();

    const getScrapy = async () => {
      const id = route.params.id;
      if (!id) return;
      const res = await get(`${endpoint}/scrapy/${id}`);
      console.debug(res);
    };

    onMounted(getScrapy);

    return {
    };
  },
});
</script>

<style scoped>

</style>
