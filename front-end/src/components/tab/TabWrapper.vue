<template>
  <div class="tabs">
    <ul class="tabs__header">
      <li v-for="title in tabTitles" :key="title" @click="selectedTab = title">
        {{ title }}
      </li>
    </ul>
    <slot />
  </div>
</template>

<script>
import { ref, provide } from 'vue';

export default {
  setup(props, { slots }) {
    const tabTitles = ref(slots.default().map((tab) => tab.props.title));
    const selectedTab = ref(tabTitles.value[0]);

    provide("selectedTab", selectedTab);

    return {
      selectedTab,
      tabTitles,
    };
  },
};
</script>

<style>
.tabs {
  margin: 0 auto;
}

.tabs__header {
  margin-bottom: 10px;
  list-style: none;
  padding: 0;
  display: flex;
}

.tabs__header li {
  width: 80px;
  text-align: center;
  padding: 10px 20px;
  margin-right: 10px;
  background-color: #ddd;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.4s all ease-out;
}
</style>