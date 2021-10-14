<template>
  <cl-form class="scrapy-overview">
    <cl-form-item :span="2" label="Settings">
      <cl-tag v-for="(d, $index) in settings" :key="$index" :label="d"/>
    </cl-form-item>
    <cl-form-item :span="2" label="Deploy">
      <cl-tag v-for="(d, $index) in deploy" :key="$index" :label="d"/>
    </cl-form-item>
    <cl-form-item :span="2" label="Spiders">
      <cl-tag :label="getCount('spiders')" clickable @click="onGoto('spiders')"/>
    </cl-form-item>
    <cl-form-item :span="2" label="Items" clickable @click="onGoto('items')">
      <cl-tag :label="getCount('items')"/>
    </cl-form-item>
    <cl-form-item :span="2" label="Middlewares" clickable @click="onGoto('middlewares')">
      <cl-tag :label="getCount('middlewares')"/>
    </cl-form-item>
    <cl-form-item :span="2" label="Settings" clickable @click="onGoto('settings')">
      <cl-tag :label="getCount('settings')"/>
    </cl-form-item>
  </cl-form>
</template>

<script lang="ts">
import {computed, defineComponent} from 'vue';

export default defineComponent({
  name: 'ScrapyOverview',
  props: {
    form: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },
  emit: [
    'goto',
  ],
  setup(props, {emit}) {
    const settings = computed(() => {
      const {cfg} = props.form;
      const {settings} = cfg || {};
      if (!settings) return [];
      const arr = [];
      for (const key in settings) {
        const value = settings[key];
        arr.push(`${key}: ${value}`);
      }
      return arr;
    });

    const deploy = computed(() => {
      const {cfg} = props.form;
      const {deploy} = cfg || {};
      if (!deploy) return [];
      const arr = [];
      for (const key in deploy) {
        const value = deploy[key];
        arr.push(`${key}: ${value}`);
      }
      return arr;
    });

    const getCount = (key) => {
      const d = props.form[key];
      if (!d) {
        return '0';
      }
      return (d.length || 0).toString();
    };

    const onGoto = (key) => {
      emit('goto', key);
    };

    return {
      settings,
      deploy,
      getCount,
      onGoto,
    };
  },
});
</script>

<style scoped>
.scrapy-overview {
  margin: 10px 0;
}
</style>
