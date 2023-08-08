<template>
  <div class="tabs">
    <ul class="tabs__header">
      <li v-for="title in tabTitles" :key="title" :class="{ 'active': selectedTab === title }" @click="selectedTab = title">
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
  list-style: none;
  padding: 0;
  display: flex;
  border-bottom: 1px solid blue;
}

.tabs__header li {
  width: 80px;
  text-align: center;
  padding: 8px 18px;
  cursor: pointer;
  margin: 0;
  transition: 0.4s all ease-out;

  &.active {
    border-bottom: 3px solid blue;
  }
}
</style>